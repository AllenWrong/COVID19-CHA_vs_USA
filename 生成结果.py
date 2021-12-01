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


def get_plot(d,n_components,filename,cloud_num_words=100):
	"""
	d:              DataFrame ->  文件数据索引后的
	n_components:   int       ->  主题数
	filename:       str       ->  文件名,例如 '国内,2021-1～2021-7,'  
	cloud_num_words int       ->  每张词云显示词的个数

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
	lda = LatentDirichletAllocation(n_components=n_components,learning_offset=50,max_iter=50)
	docres = lda.fit_transform(word_array)

	model=KMeans(n_clusters=n_components)
	classifier=model.fit_predict(docres)
	f,p_value = chi2(word_array,classifier)
	model=SelectKBest(chi2,k=400)
	new_word_array = model.fit_transform(word_array,classifier)
	words=words[model.get_support()]
	words=pd.Series(words.tolist())
	lda = LatentDirichletAllocation(n_components=n_components,learning_offset=50,max_iter=50)
	docres = lda.fit_transform(new_word_array)
	mask = imageio.imread('data/China.png')
	for t_index in range(n_components):

		index = lda.components_[t_index].argsort()[-cloud_num_words:]
		ws = words[index].tolist()
		i = lda.components_[t_index][index]
		#cloud=WordCloud(font_path='C:/Windows/simhei.ttf')   #window
		cloud = WordCloud(font_path='/system/library/fonts/Hiragino Sans GB.ttc',scale=10,mask=mask)  #mac
		s=cloud.fit_words(dict(zip(ws,i)))
		plt.figure(figsize=(20, 20))
		#plt.imshow(s)

		cloud.to_file(filename+'%s.png'%t_index)


def main(method,n_components,cloud_num_words=100):

	try:
		shutil.rmtree('Img')
	except:
		pass
	os.mkdir('Img')

	#method='年'
	df=pd.read_csv('data/useful_data.csv',encoding='gbk')
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

		d=df.loc[i[0]:i[1],:]
		date = i[0]+'~'+i[1]
		print('正在生成,' + date+',图像')
		get_plot(d,n_components,'Img/国内,%s,'%date)

if __name__=="__main__":

	main('年',5)