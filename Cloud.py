

import jieba      #分词
import pandas as pd
import pymysql
from matplotlib import pyplot as plt        #绘图，数据可视化
from wordcloud import WordCloud           #词云
from PIL import Image                    #图片处理
import numpy as np                       #矩阵运算
import sqlite3




data =pd.read_csv('lvyoudata.csv',header=None)


text=""
for item in data[0]:
    text=text+item[0]

cut=jieba.cut(text)
string=' '.join(cut)

img=Image.open(r'static\image\test.png')
img_array=np.array(img)
wc=WordCloud(
    background_color='white',
    mask=img_array,
    font_path="HGDGY_CNKI.TTF"
)
wc.generate_from_text(string)


#绘制图片
fig = plt.figure(1)
plt.imshow(wc)
plt.axis('off')

plt.savefig(r'static\image\word.jpg',dpi=500)