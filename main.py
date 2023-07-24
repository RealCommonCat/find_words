import re
import os
from cut import seg_sentence
from lda_ import lda_
from multiprocessing import Process
from bar import print_progress_bar
import time
from lda_ import lda_
from data_slice import slice_data 
from multiprocessing import Lock 
import multiprocessing
from compare_with_dict import compare_with_dict
SPLIT="@@@@@"
SPLIT_1="@@@@"
class Main():
    def read_data(self):
        print("开始读取数据")
        files=os.listdir("./data")
        outs=os.listdir("./out1")
        for file in files:
            file_d=open("./data/"+file,"r",encoding="utf-8")
            lines=file_d.readlines()
            if(file+".out1" in outs):
                self.data.append({"data":None,"name":lines[5],"file":file})
            else:
                lines_=""
                data_=[]
                for i in range(7,len(lines)):
                    line=lines[i]
                    if line=="\n":
                        continue
                    elif re.match(self.reg_date,line)==None:
                        lines_+=line
                    else:
                        data_.append(lines_)
                        lines_=""
                self.data.append({"data":data_,"name":lines[5],"file":file})
        print("开始切割数据")
        for i in range(len(self.data)):
            if(self.data[i]["file"]+".out1" in outs):
                print(f"读取到 {self.data[i]['file']} 切割记录 载入记录...")
            else:
                print(f"切割{self.data[i]['file']}")
                seg_sentence(self.data[i]["data"],open(self.out1+f"/{self.data[i]['file']}.out1","w",encoding="utf-8"),self.data[i]["file"])
    def read_out1(self,filepath):
        fd1=open(f"out1/{filepath}.out1","r",encoding="utf-8")
        return fd1.readlines()
    def lda__(self,queue,lines,name,file,idx,s):
        out=[]
        amount_blocks=int(len(lines)/(self.overlapping*self.analyse_window))
        for i in range(amount_blocks-1):
            out=out+lda_(lines[i*self.analyse_window:(i+1)*self.analyse_window])
            queue.put({
                "s":s,
                "type":"lda"
            })
        block=lines[len(lines)-len(lines)%self.analyse_window:]
        if(len(block)>0):
            out=out+[SPLIT]+lda_(block)
        queue.put({
            "type":"completed",
            "process_idx":idx,
            "data_idx":s,
            "data":out,
            "name":name,
            "file":file
        })
    def lda__multi(self,queue,lines_,name,file,s):
        ps=[]
        for i in range(self.amount):
            p=Process(target=self.lda__,args=(queue,lines_[i],name,file,i,s))
            ps.append(p)
        for p in ps:
            p.start()
            print(p)

    def get_processed_len(self,ps_):
        len_=0
        for p in ps_:
            len_+=len(p)
        return len_
    
    def print_completed_bar(self,condition,total):
        c0=0
        for c in condition["completed"]:
            c0+=c
        print_progress_bar(c0,total,prefix="LDA: ",suffix='Completed')
    def results_process(self):
        fs=os.listdir(self.out2)
        results=[]
        for f in fs:
            fd=open(self.out2+"/"+f,"r",encoding="utf-8")
            results.append({"file":f,"data":compare_with_dict(self.k,fd.read().split(SPLIT))})
            fd.close()
        for result in results:
            fd=open(self.out3+"/"+result["file"]+".out3","w",encoding="utf-8")
            for d in result["data"]:
                fd.write(str(d["idx"])+"\n")
                for i in range(len(d["words"])):
                    w=d["words"][i]
                    f_=d["floats"][i]
                    fd.write(w+SPLIT_1+str(f_)+SPLIT_1)
            fd.close()
    def __init__(self):   
        self.lock=Lock()
        self.data=[]
        self.out1="./out1"
        self.out2="./out2"
        self.out3="./out3"
        self.reg_date=r"\d{4}-\d{2}-\d{2}\s\d{1,2}:\d{2}:\d{2}"
        self.k=0.1
        self.analyse_window=1000
        self.overlapping=1
        self.process_lda=[]
        self.data_processed=[]
        self.amount=2
        self.queue=multiprocessing.Queue()
        self.read_data()
        self.condition={
            "remained_lda":[False for x in range(len(self.data))],
            "completed": [0 for x in range(len(self.data))]
        }
        self.outs_=[[] for x in range(len(self.data))]
        self.total=0
        for i in range(len(self.data)):
            self.data_processed.append({"data":slice_data(self.read_out1(self.data[i]["file"]),self.amount),"name":self.data[i]['name'],"file":self.data[i]["file"]})
        for d in self.data_processed:
            for d1 in d["data"]:
                self.total+=len(d1)
        print("开始运行LDA")
        out2_files=os.listdir(self.out2)
        self.completed_out2=[]
        for o in out2_files:
            self.completed_out2.append(out2_files[:-4])
        for i in range(len(self.data_processed)):
            if(self.data_processed[i]["file"] not in self.completed_out2):
                self.lda__multi(self.queue,self.data_processed[i]["data"],self.data_processed[i]["name"],self.data_processed[i]["file"],i)
            else:
                print(f"准备加载已完成的LDA文件{self.data_processed[i]['file']}")
        while(True):
            time.sleep(0.5)
            self.print_completed_bar(self.condition,self.total)
            m=self.queue.get()
            if(m["type"]=="lda"):
                self.condition["completed"][m["s"]]+=self.overlapping*self.analyse_window
            if(m["type"]=="completed"):
                self.outs_[m["data_idx"]].append(m)
                if(len(self.outs_[m["data_idx"]])>=self.amount):
                    self.condition["remained_lda"][m["data_idx"]]=True
                    print(f"正在写入LDA结果文件 {m['name']}")
                    fd=open(f"./out2/{m['file']}.out2","w",encoding="utf-8")
                    for i in range(self.amount):
                        for out_ in self.outs_[m["data_idx"]]:
                            if(out_["process_idx"]==i):
                                for o in out_["data"]:
                                    fd.write(o)
                    fd.close()
                k_=True
                for k in self.condition["remained_lda"]:
                    if ~k:
                        k_=False
                if(k_):
                  break
        print("LDA完成 准备进行数据整理")
        self.results_process()
if __name__ == '__main__':
    main=Main()