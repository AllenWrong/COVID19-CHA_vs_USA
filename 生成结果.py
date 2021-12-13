import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_selection import chi2,SelectKBest
from sklearn.decomposition import LatentDirichletAllocation
import json
from matplotlib import pyplot as plt
from wordcloud import WordCloud
from sklearn.cluster import KMeans
import imageio
import shutil
import os
plt.rcParams['font.sans-serif']=['Arial Unicode Ms']

    


def get_stop_words(filename):
    file=open(filename,'r',encoding='gbk')
    stop_words = file.read().split('\n')
    file.close()
    return stop_words

def save_doc_title_matrix(n_components,data,filename,indexs):
	columns = ['主题%s'%i for i in range(1,n_components+1)]
	df = pd.DataFrame(data,columns=columns,index=indexs)

	df.to_excel(filename+'文档_主题矩阵.xlsx')

def save_title_word_matrix(n_components,data,filename,columns):
	indexs = ['主题%s'%i for i in range(1,n_components+1)]
	df = pd.DataFrame(data, columns=columns, index=indexs)

	df.to_excel(filename + '主题_词矩阵.xlsx')
	pass
def get_plot(d,n_components,filename,cloud_num_words=150,lang="CHA",method='半年',which_file=None):
	"""
	d:              DataFrame ->  文件数据索引后的
	n_components:   int       ->  主题数
	filename:       str       ->  文件名,例如 '国内,2021-1～2021-7,'  
	cloud_num_words int       ->  每张词云显示词的个数

	which_file : 记录着每个样本的文档名
	return 
	"""
	stop_words = get_stop_words('data/stop_words.txt')
	data=d['content'].values.tolist()
	classifier = d['class'].tolist()
	cotVector = CountVectorizer(stop_words=stop_words)
	vector=cotVector.fit_transform(data)
	word_array = vector.toarray()
	feature_name = cotVector.get_feature_names()
	feature_name[:10]
	words = pd.Series(feature_name)
	#print("LDA......")
	#lda = LatentDirichletAllocation(n_components=n_components,learning_offset=50,max_iter=50)
	#docres = lda.fit_transform(word_array)
	#print("LDA successful !!")
	print("正在进行聚类......")
	model=KMeans(n_clusters=n_components)
	#classifier=model.fit_predict(docres)
	classifier = model.fit_predict(word_array)
	print("聚类 successful !!")
	print("chi.....")
	f,p_value = chi2(word_array,classifier)
	model=SelectKBest(chi2,k=200)   #选取200个词
	print("chi successful !!")
	new_word_array = model.fit_transform(word_array,classifier)
	words=words[model.get_support()]
	words=pd.Series(words.tolist())
	print("LDA....")
	lda = LatentDirichletAllocation(n_components=n_components,learning_offset=50,max_iter=50)
	docres = lda.fit_transform(new_word_array)
	save_doc_title_matrix(n_components,docres,'word_features'+filename[3:],which_file)     #保存文档主题矩阵
	save_title_word_matrix(n_components,lda.components_,'word_features'+filename[3:],words.tolist())    #保存主题——词矩阵

	print("LDA successful !!!")
	mask = imageio.imread('data/China.png')
	print("正在绘制画像....")
	if lang=="ENG":
		mask = imageio.imread('data/USA.png')

	for t_index in range(n_components):

		index = lda.components_[t_index].argsort()[-cloud_num_words:]
		ws = words[index].tolist()
		i = lda.components_[t_index][index]
		#cloud=WordCloud(font_path='C:/Windows/simhei.ttf')   #window
		cloud = WordCloud(font_path='/system/library/fonts/Hiragino Sans GB.ttc',background_color="white",scale=10,mask=mask)  #mac
		s=cloud.fit_words(dict(zip(ws,i)))
		plt.figure(figsize=(12, 12))
		#plt.imshow(s)

		cloud.to_file(filename+'%s.png'%t_index)
	print("绘制成功....")

def main(method,n_components,lang="CHA",cloud_num_words=100):
	"""

	:param method:           str  -> 时间段，可选年，季，半年
	:param n_components:     int  -> 主题数
	:param lang:  			 str  -> 语言，可选CHA and ENG
	:param cloud_num_words:  int  -> 绘制词云显示的词的个数
	:return:  None
	"""

	#method='年'
	file = 'useful_data_CHA.csv'
	if lang=="ENG":
		file='useful_data_ENG.csv'
	df=pd.read_csv('data/%s'%file,encoding='gbk')
	df.loc[:,'date']=pd.to_datetime(df.date)
	df.set_index('date',inplace=True)
	slic = []
	if method=='季':
		slic.append(['2020-1','2020-4'])
		slic.append(['2020-4','2020-7'])
		slic.append(['2020-7','2020-10'])
		slic.append(['2020-10','2021-1'])
		slic.append(['2021-1','2021-4'])
		slic.append(['2021-4','2021-7'])
		slic.append(['2021-7','2021-12'])
	elif method=='半年':
		slic.append(['2020-1','2020-7'])
		slic.append(['2020-7','2021-1'])
		slic.append(['2021-1','2021-7'])
		slic.append(['2021-7','2021-12'])
	elif method=='年':
		slic.append(['2020-1','2021-1'])
		slic.append(['2021-1','2021-12'])

	for i in slic:

		d=df.loc[i[0]:i[1],['content','class']]

		which_file = df.loc[i[0]:i[1],'file'].tolist()
		date = i[0]+'~'+i[1]
		print('正在生成,' + date+',图像')
		get_plot(d,n_components,'Img/%s/%s,%s,'%(method,lang,date),lang=lang,method=method,which_file=which_file)

if __name__=="__main__":

	#main('季',3,lang="ENG")

	#main('半年', 3, lang="ENG")
	#main('年', 3, lang="ENG")
	#main('季', 3, lang="CHA")
	main('半年', 3, lang="CHA")
	#main('年', 3, lang="CHA")