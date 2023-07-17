import os
def trans_line(line):
    return {"word":None,"weight":None}
#TODO
def trans_content(content):
    return [{"idx":None,"topics":[{"word":None,"weight":None}]}]
#TODO
core_dict=[]
fs=os.listdir("./core_dict")
for f_ in fs:
    f=open("./core_dict/{f_}","r",encoding="utf-8")
    for line in f.readlines():
        core_dict.append(line)
def compare_with_dict(name,file,k):
    out=[]
    fd=open("./out2/"+file+"@"+name+"@"+".out2","r",encoding="utf-8")
    contents=trans_content(fd.readlines())
    for i in range(len(contents)):
        out_=[]
        for topic in contents[i]["topics"]:
            j=0
            for i in range(len(topic)):
                if topic[i]["word"] in core_dict:
                    j+=topic[i]["weight"]
                    topic.remove(i)
                    #TODO
            if(j>k):
                out_.append(topic)
        if(len(out_)!=0):
            out.append({"idx":contents[i]["idx"]})
    return out    


   
