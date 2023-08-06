# -*- coding: utf-8 -*-
"""
Created on Thu Nov 11 20:16:41 2021

@author: Administrator
"""

import vtda
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
#解决中文乱码问题
plt.rcParams["font.sans-serif"]='SimHei'
#解决负号无法正常显示问题
plt.rcParams["axes.unicode_minus"]= False


from vtda import  (read_dasp_data, #读取dasp数据
                  sperling)  #平稳性

dir_='E:/城轨中心/2项目/20210615昆明车辆异常晃动/昆明加速度数据/昆明1、2号线/上行-大学城南-北部汽车站'#目录 注意目录之间需要用 '/' 而不是 '\'
name='20210126昆明地铁1、2、呈贡支线测试'#文件名 注意文件名不要带试验号
dir_='E:/20200620磁各庄实验室/6科研/平稳性/'#目录 注意目录之间需要用 '/' 而不是 '\'
name='20210529北京6号线平稳性上行'#文件名 注意文件名不要带试验号
dir_='E:/20200620磁各庄实验室/6科研/平稳性/'
name='北京地铁19号线车辆平稳性测试'
data,info=vtda.read_dasp_data(name,dir_=dir_,num_shiyan='1')
y=data['1']['1'] #1试验号的3通道
time_,spr=sperling(y, 
            sample_rate=5000, #采样频率
            len_=5,  #分析窗长 单位：秒
            window='hanning', #窗函数
            cdxs=0.8, #重叠系数
            direction='垂向', #或者填横向  #数据方向
            unit='m/ss',#g
            )
    
plt.figure(figsize=(10, 6))
plt.plot(time_,spr)      

res=pd.DataFrame([time_,spr]).T  
res.columns=['时间','平稳性']
res.to_excel(dir_+'/平稳性.xlsx')