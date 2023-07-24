import os
import re
core_dict="./core_dict"
fs=os.listdir(core_dict)
core_dicts=[]
float_reg=r"(\d+(?:\.\d*)?|\.\d+)"
word_reg=r'"\w+"'
for f in fs:
    fd=open(f,"r",encoding="utf-8")
    print(f"读取核心词典{f}")
    for line in fd.readlines():
        core_dicts.append(line)
def compare_with_dict(k,blocks):
    data=[]
    for i in range(len(blocks)):
        block=blocks[i]
        floats=re.findall(float_reg,block)
        words=re.findall(word_reg,block)
        a=0.0
        try:
            for j in range(len(words)):
                if(words[j] in core_dicts):
                    a+=floats[j]
        except:
            continue
        if a>=k:
            data.append({
                "data":{
                    "words":words[i],
                    "floats":floats[i]
                },
                "idx":i
            })
    return data

        