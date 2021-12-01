import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
import json
import re
import os
import time

class Spider():
    def __init__(self,keyword):
        self.web_name="人民网"
        self.log=self.init_info(keyword)
        self.filename=self.get_max_filename(keyword)
        
        self.keyword=keyword
        self.url="http://search.people.cn/search-platform/front/search"
        self.headers={
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36',
            #'Referer':'http://www.xinhuanet.com/',
            'Cookie':'__jsluid_h=d4f4332fb392a40cea16443f48a1f184; sso_c=0; sfr=1',
            'Origin':'http://search.people.cn',
            'Referer':'http://search.people.cn/s?keyword=%E6%A0%B8%E9%85%B8&st=0&_=1637496405242',
            'Content-Type':'application/json',
            
        }
        self.data={
            'endTime': 0,
            'hasContent': 'true',
            'hasTitle': 'true',
            'isFuzzy': 'true',
            'key': "核酸检测",   #修改关键词
            'limit': 10,
            'page': 2,
            'sortType': 2,
            'startTime': 0,
            'type': 0,
        }
        
        #for page in tqdm(range(self.log[self.web_name][keyword],500),ncols=90):
        for page in tqdm(range(1,500),ncols=90):
            self.data['page']=page
            try:
                self.get_first_page()
            except:
                pass
            self.log[self.web_name][keyword] += 1
            self.flush_log()
            
            
    def flush_log(self):
        file=open('log','w')
        file.write(json.dumps(self.log))
        file.close()
        
    def get_max_filename(self,keyword):
        MAX=0
        for i in os.listdir('../data/CHA/%s'%keyword):
            if i[0]=='.':
                continue
            if int(i.split('.')[0])>MAX:
                MAX = int(i.split('.')[0])+1
                
        return MAX
    
    def init_info(self,keyword):
        file=open('log','r')
        t=file.read()
        js=json.loads(t)
        file.close()
        if not self.web_name in js:
            js[self.web_name]={keyword:1}
            
        return js
    
    def get_first_page(self):
        r=requests.post(self.url,headers=self.headers,data=json.dumps(self.data))

        js=json.loads(r.text)
        for i in js['data']['records']:
            try:
                title=re.sub('[^\u4e00-\u9fa5，。？！]','',i['title'])
                date=i['displayTime']/1000
                date=time.localtime(date)
                date=time.strftime('%Y-%m-%d %H:%M:%d',date)
                url=i['url']
                content=self.get_content(url)
                content=re.sub('[^\u4e00-\u9fa5，。？！]','',content)

                file=open('../data/CHA/%s/%s.txt'%(self.keyword,self.filename),'w')
                file.write(title+'\n')
                file.write(date+'\n')
                file.write(content+'\n')
                file.close()
                self.filename += 1
            except:
                pass
        

    def get_content(self,url):
        
        r=requests.get(url,headers=self.headers)
        r.encoding='gbk'
        #print(r.text)
        soup=BeautifulSoup(r.text,'lxml')
        content=soup.select('div.rm_txt_con')[0].text.strip()
        return content
        
        
if __name__=="__main__":

    Spider('核酸')