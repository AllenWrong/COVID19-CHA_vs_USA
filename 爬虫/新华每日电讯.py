import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
import json
import re
import os

class Spider():
    def __init__(self,keyword):
        
        self.log=self.init_info(keyword)
        self.filename=self.get_max_filename(keyword)
        
        self.keyword=keyword
        self.url="http://so.news.cn/was5/web/conwebsite/getNews"
        self.headers={
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36',
            'Referer':'http://www.xinhuanet.com/',
            
        }
        self.params={
            'siteId': '11148',
            'pageNo': '2',
            'pageSize': '10',
            'senior': '0',
            'titleInclude': '1',
            'condition': '1',
            'textInclude': '1',
            'sort': '1',
            'keyword': keyword,
            't': '1637493590751',
        }
        
        for page in tqdm(range(self.log['新华每日电讯'][keyword],500),ncols=90):
            self.params['pageNo']=page
            try:
                self.get_first_page()
            except:
                pass
            self.log['新华每日电讯'][keyword] += 1
            self.flush_log()
            
            
    def flush_log(self):
        file=open('../data/log','w')
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
        file=open('../data/log','r')
        t=file.read()
        js=json.loads(t)
        file.close()
        if not '新华每日电讯' in js:
            js['新华每日电讯']={keyword:1}
            
        return js
    
    def get_first_page(self):
        r=requests.get(self.url,headers=self.headers,params=self.params)
        r.encoding='utf-8'
        js=json.loads(r.text)
        for i in js['content']['result']:
            try:
                title=re.sub('[^\u4e00-\u9fa5，。？！]','',i['shortTitle'])
                date=i['releaseDate']
                url=i['originUrl'][0]
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
        r.encoding='utf-8'
        soup=BeautifulSoup(r.text,'lxml')
        content=soup.select('div.main-content-box')[0].text.strip()
        return content
            
            
Spider('核酸')