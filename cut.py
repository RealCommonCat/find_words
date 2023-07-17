import jieba as jb
from bar import print_progress_bar
import re
def stopwordslist(filepath):
    stopwords = [line.strip() for line in open(filepath, 'r', encoding='utf-8').readlines()]
    return stopwords
stopwords = stopwordslist('stopWords/stop.txt') 
# 对句子进行分词
def seg_sentence(sentences,out,file):
    total=len(sentences)
    i=0
    for sentence in sentences:
        i+=1
        sentence_seged = jb.cut(sentence)
        outstr=''
        for word in sentence_seged:
            if word not in stopwords and word.__len__()>=1:
                if word != '\t':
                    outstr += word
                    outstr += " "
        out.write(outstr+"\n")
        print_progress_bar(i,total, prefix=f'{file} Progress:', suffix='Complete', length=50)

