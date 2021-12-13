# 数据科学大作业
 python, sklearn中美疫情分析

使用sklearn做LDA对中美疫情进行分析

主要运行模块 
> 生成结果.py
>> main(method,n_components,lang,cloud_num_words)
* :param method:           str  -> 时间段，可选年，季，半年
* :param n_components:     int  -> 主题数
* :param lang:  			 str  -> 语言，可选CHA and ENG
* :param cloud_num_words:  int  -> 绘制词云显示的词的个数
* :return:  None 

## 生成的图像文件保存在Img
* 目录为
```
Img
|   半年
    |   lang,start_time~end_time,theme.png
|   季
    |   lang,start_time~end_time,theme.png
|   年
    |   lang,start_time~end_time,theme.png
```
> 其中lang为语言，start_time 和 end_time分别表示起始时间和终止时间，them为主题
> 比如说有三个主题，文件名如下
> * CHA,2020-1~2021-1,0.png
> * CHA,2020-1~2021-1,1.png
> * CHA,2020-1~2021-1,2.png
> * ENG,2020-1~2021-1,0.png
> * ENG,2020-1~2021-1,1.png
> * ENG,2020-1~2021-1,2.png

**安装依赖包：**
> pip install streamlit
> 

其他的依赖包，按照类似的方式安装即可。

### 运行程序

在项目根目录下运行如下命令：

``streamlit run display.py``

其他的再说。。。