import os
from jieba import posseg
from tqdm import tqdm
import pandas as pd
import json
path = 'data/CHA/'



def get_words(filename):

    file=open(filename,'r')
    data=file.read().split('\n')
    if len(data)!=3:
        return -1,-1
    text=data[2]
    date=data[1]
    try:
        pd.to_datetime(date)
    except:
        return -1,-1
    file.close()

    sentence_seged = posseg.cut(text)
    word=[]
    for x in sentence_seged:
        if x.flag=='n':
            word.append(x.word)
            
    return word,date

words =[]
date = []
classifier = []
c=0
for i in os.listdir(path):

    if i[0]=='.':
        continue

    print('\n'+i,end=':  ')
    for file in tqdm(os.listdir(path+i+'/')[:],ncols=120):
        if file[0]=='.':
            continue
        filename=path+i+'/'+file

        w,d=get_words(filename)
        if w==-1:
            continue
        if len(w)<20:
            continue
        w=' '.join(w)
        words.append(w)
        date.append(d)
        classifier.append(c)

    c += 1
df=pd.DataFrame({'date':date,'content':words,'class':classifier})
try:
    df.loc[:,'date']=pd.to_datetime(df.date)
except:
    pass
df.set_index('date',inplace=True)
df.to_csv('data/useful_data.csv',encoding='gbk')