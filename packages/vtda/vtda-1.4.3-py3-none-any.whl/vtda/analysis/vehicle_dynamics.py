# -*- coding: utf-8 -*-
"""
Created on Sat Jun 26 21:23:50 2021

@author: ZSL
"""
import numpy as np
import math
import time
import datetime
import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from vtda.util.util import weight_factor
from scipy import signal
#解决中文乱码问题
plt.rcParams["font.sans-serif"]='SimHei'
#解决负号无法正常显示问题
plt.rcParams["axes.unicode_minus"]= False
from tqdm import tqdm
from vtda.util.util import (
                                               weight_factor,
                                               fix_num,
                                               find_start_end
                                            )
from vtda.analysis.base import (
                                               choose_windows,
                                               fft,
                                               octave_3,
                                               rolling_octave_3,
                                               base_level,
                                               rms_time,
                                               rms_frec,
                                    			lvbo_low,
                                    			lvbo_high,
                                    			lvbo_daitong,
                                    			lvbo_daizu
                                            )


# data=data2['1']
# sample_rate=5000
def discontinuous_wheel_rail_force(data, 
                                    sample_rate=5000,
                                    info_tongdao=None,
                                    dir_=None,#储存文件目录
                                    name=None,                                    
                                    ):
#创建储存结果文件夹
    dir_gepian=dir_+'/'+name+'/'+datetime.datetime.now().strftime("%Y-%m-%d")+'_1各片结果'
    dir_zuqiao=dir_+'/'+name+'/'+datetime.datetime.now().strftime("%Y-%m-%d")+'_2组桥结果'
    dir_zhengti=dir_+'/'+name+'/'+datetime.datetime.now().strftime("%Y-%m-%d")+'_3整体结果'
    list_dir=[dir_gepian,dir_zuqiao,dir_zhengti]
    for i in list_dir:  
        pass          
        isExists=os.path.exists(i)
        if isExists:
            pass
        else:
            os.makedirs(i)
            
#标定系数求逆
    for i in info_tongdao:
        pass
        try:  
            for j in info_tongdao[i]['标定系数']:
                pass
                info_tongdao[i]['标定系数'][j]=np.linalg.inv(info_tongdao[i]['标定系数'][j])
        except:
            pass
                
    speed=lvbo_low(data[info_tongdao['速度']],fq=3,fs=sample_rate,n=1)
    mileage=data[info_tongdao['里程']][speed>5]
    
#处理应变----滤波和平衡
    yingbian={}
    
    list_qiaolu=['左1桥','左2桥','右1桥','右2桥']
    fq=50     #50Hz低通滤波
    n=3   #董工数采应变有个3倍的关系，此处除以3    
    for i in info_tongdao:
        pass 
        if i in list_qiaolu:
            pass
            #i='左1桥'
            yingbian[i]={}
            ls=lvbo_low(data[info_tongdao[i]['垂向']],fq=fq,fs=sample_rate)[speed>5]/n  #滤波
            yingbian[i]['垂向']=ls-ls.mean()  #平衡通道 
            ls=lvbo_low(data[info_tongdao[i]['横向']],fq=fq,fs=sample_rate)[speed>5]/n 
            yingbian[i]['横向']=ls-ls.mean()

#确定应变极大值和极小值的位置
    loc_max={}
    for i in info_tongdao:
        pass 
        if i in list_qiaolu:
            pass
            #i='左1桥'
            loc_max[i]={}
            #max_=find_max_deta_time(yingbian[i]['垂向'],sample_rate=sample_rate,nn=0.4)
            max_=find_max_jizhi(yingbian[i]['垂向'])
            loc_max[i]['正']=max_
            #min_=find_max_deta_time(-yingbian[i]['垂向'],sample_rate=sample_rate,nn=0.4)
            min_=find_max_jizhi(-yingbian[i]['垂向'])
            loc_max[i]['负']=min_        

#修正左右轮极大值个数不一致的情况
    #当左右轮出现选择的最大值个数不一致时，实际工程中几乎必然会出现这种情况，以点数少的为准 
    #从多的loc里面挑选出和少的最接近的数，组成一个新的loc，这样左右轮就一样多了。每一个点都是最大值，这样操作的误差可以接受    
    def fix_len(a,b):
        if len(a)>len(b):
            long=a
            short=b
            res=[]
            for i in short:
                pass
                idx = np.abs(long - i).argmin()
                res.append(long.flat[idx]) 
            return  np.array(res),short
        elif len(a)<len(b):
            long=b
            short=a
            res=[]
            for i in short:
                pass
                idx = np.abs(long - i).argmin()
                res.append(long.flat[idx]) 
            return  short,np.array(res)            
        else:
            return a,b
   
    loc_max['左1桥']['正'],loc_max['右1桥']['正']=fix_len(loc_max['左1桥']['正'],loc_max['右1桥']['正'])
    loc_max['左1桥']['负'],loc_max['右1桥']['负']=fix_len(loc_max['左1桥']['负'],loc_max['右1桥']['负'])
    loc_max['左2桥']['正'],loc_max['右2桥']['正']=fix_len(loc_max['左2桥']['正'],loc_max['右2桥']['正'])
    loc_max['左2桥']['负'],loc_max['右2桥']['负']=fix_len(loc_max['左2桥']['负'],loc_max['右2桥']['负'])    

#确定应变极大值和极小值
    yingbian_max={}
    for i in info_tongdao:
        pass 
        if i in list_qiaolu:
            pass
            #i='左1桥'
            yingbian_max[i]={}
            yingbian_max[i]['垂_正']=yingbian[i]['垂向'][loc_max[i]['正']]
            yingbian_max[i]['横_正']=yingbian[i]['横向'][loc_max[i]['正']]
            yingbian_max[i]['垂_负']=yingbian[i]['垂向'][loc_max[i]['负']]
            yingbian_max[i]['横_负']=yingbian[i]['横向'][loc_max[i]['负']] 

#计算应力值
    force={}
    for i in info_tongdao:
        pass 
        if i in list_qiaolu:
            pass
            #i='左1桥'
            force[i]={}
            force[i]['垂_正'],force[i]['横_正']=np.dot(info_tongdao[i]['标定系数']['正值'],np.array([yingbian_max[i]['垂_正'],yingbian_max[i]['横_正']]))   
            force[i]['垂_负'],force[i]['横_负']=np.dot(info_tongdao[i]['标定系数']['负值'],np.array([yingbian_max[i]['垂_负'],yingbian_max[i]['横_负']]))   

#计算力值对应的速度和里程  
    for i in info_tongdao:
        pass 
        if i in list_qiaolu:
            pass
            #i='左1桥'
            force[i]['速度_正']=speed[loc_max[i]['正']]       
            force[i]['速度_负']=speed[loc_max[i]['负']]       
            force[i]['里程_正']=mileage[loc_max[i]['正']]       
            force[i]['里程_负']=mileage[loc_max[i]['负']] 


    list_tongdaoduiying=[[['左1桥','垂_正'],['右1桥','垂_正']],
                         [['左1桥','垂_负'],['右1桥','垂_负']],
                         [['左2桥','垂_正'],['右2桥','垂_正']],
                         [['左2桥','垂_负'],['右2桥','垂_负']]]

 
#计算指标画图，存数据
    i='左1桥'
    j='右1桥'
    res_1_1=cal_index(speed=force[i]['速度_正'],
              mileage=force[i]['里程_正'],
              force_left_chui=force[i]['垂_正'],
              force_left_heng=force[i]['横_正'],
              force_right_chui=force[j]['垂_正'],
              force_right_heng=force[j]['横_正'],
              dir_=dir_gepian,
              name='1_1') 
    i='左1桥'
    j='右1桥'
    res_1_2=cal_index(speed=force[i]['速度_负'],
              mileage=force[i]['里程_负'],
              force_left_chui=force[i]['垂_负'],
              force_left_heng=force[i]['横_负'],
              force_right_chui=force[j]['垂_负'],
              force_right_heng=force[j]['横_负'],
              dir_=dir_gepian,
              name='1_2')    
    i='左2桥'
    j='右2桥'
    res_2_1=cal_index(speed=force[i]['速度_正'],
              mileage=force[i]['里程_正'],
              force_left_chui=force[i]['垂_正'],
              force_left_heng=force[i]['横_正'],
              force_right_chui=force[j]['垂_正'],
              force_right_heng=force[j]['横_正'],
              dir_=dir_gepian,
              name='2_1') 
    i='左2桥'
    j='右2桥'
    res_2_2=cal_index(speed=force[i]['速度_负'],
              mileage=force[i]['里程_负'],
              force_left_chui=force[i]['垂_负'],
              force_left_heng=force[i]['横_负'],
              force_right_chui=force[j]['垂_负'],
              force_right_heng=force[j]['横_负'],
              dir_=dir_gepian,
              name='2_2') 
    
    huizong={}
    huizong['1_1']={}
    ls=np.maximum(np.array(res_1_1['左轮脱轨系数']), np.array(res_1_1['右轮脱轨系数']), out=None)
    huizong['1_1']['脱轨系数']=round(ls.max(),2)
    huizong['1_1']['速度_脱轨系数']=round(res_1_1.loc[np.argmax(ls),'速度'],1)
    huizong['1_1']['里程_脱轨系数']=round(res_1_1.loc[np.argmax(ls),'里程'],3)    
    ls=res_1_1['轮重减载率']
    huizong['1_1']['轮重减载率']=round(ls.max(),2)
    huizong['1_1']['速度_减载率']=round(res_1_1.loc[np.argmax(ls),'速度'],1)
    huizong['1_1']['里程_减载率']=round(res_1_1.loc[np.argmax(ls),'里程'],3)   
    ls=res_1_1['轮轴横向力']
    huizong['1_1']['轮轴横向力']=round(ls.max(),1)
    huizong['1_1']['速度_横向力']=round(res_1_1.loc[np.argmax(ls),'速度'],1)
    huizong['1_1']['里程_横向力']=round(res_1_1.loc[np.argmax(ls),'里程'],3) 
    
    huizong['1_2']={}
    ls=np.maximum(np.array(res_1_2['左轮脱轨系数']), np.array(res_1_2['右轮脱轨系数']), out=None)
    huizong['1_2']['脱轨系数']=round(ls.max(),2)
    huizong['1_2']['速度_脱轨系数']=round(res_1_2.loc[np.argmax(ls),'速度'],1)
    huizong['1_2']['里程_脱轨系数']=round(res_1_2.loc[np.argmax(ls),'里程'],3) 
    ls=res_1_2['轮重减载率']
    huizong['1_2']['轮重减载率']=round(ls.max(),2)
    huizong['1_2']['速度_减载率']=round(res_1_2.loc[np.argmax(ls),'速度'],1)
    huizong['1_2']['里程_减载率']=round(res_1_2.loc[np.argmax(ls),'里程'],3)   
    ls=res_1_2['轮轴横向力']
    huizong['1_2']['轮轴横向力']=round(ls.max(),1)
    huizong['1_2']['速度_横向力']=round(res_1_2.loc[np.argmax(ls),'速度'],1)
    huizong['1_2']['里程_横向力']=round(res_1_2.loc[np.argmax(ls),'里程'],3)     
    
    huizong['2_1']={}
    ls=np.maximum(np.array(res_2_1['左轮脱轨系数']), np.array(res_2_1['右轮脱轨系数']), out=None)
    huizong['2_1']['脱轨系数']=round(ls.max(),2)
    huizong['2_1']['速度_脱轨系数']=round(res_2_1.loc[np.argmax(ls),'速度'],1)
    huizong['2_1']['里程_脱轨系数']=round(res_2_1.loc[np.argmax(ls),'里程'],3)      
    ls=res_2_1['轮重减载率']
    huizong['2_1']['轮重减载率']=round(ls.max(),2)
    huizong['2_1']['速度_减载率']=round(res_2_1.loc[np.argmax(ls),'速度'],1)
    huizong['2_1']['里程_减载率']=round(res_2_1.loc[np.argmax(ls),'里程'],3)   
    ls=res_2_1['轮轴横向力']
    huizong['2_1']['轮轴横向力']=round(ls.max(),1)
    huizong['2_1']['速度_横向力']=round(res_2_1.loc[np.argmax(ls),'速度'],1)
    huizong['2_1']['里程_横向力']=round(res_2_1.loc[np.argmax(ls),'里程'] ,3)
    
    huizong['2_2']={}
    ls=np.maximum(np.array(res_2_2['左轮脱轨系数']), np.array(res_2_2['右轮脱轨系数']), out=None)
    huizong['2_2']['脱轨系数']=round(ls.max(),2)
    huizong['2_2']['速度_脱轨系数']=round(res_2_2.loc[np.argmax(ls),'速度'],1)
    huizong['2_2']['里程_脱轨系数']=round(res_2_2.loc[np.argmax(ls),'里程'] ,3)
    ls=res_2_2['轮重减载率']
    huizong['2_2']['轮重减载率']=round(ls.max(),2)
    huizong['2_2']['速度_减载率']=round(res_2_2.loc[np.argmax(ls),'速度'],1)
    huizong['2_2']['里程_减载率']=round(res_2_2.loc[np.argmax(ls),'里程'] ,3)  
    ls=res_2_2['轮轴横向力']
    huizong['2_2']['轮轴横向力']=round(ls.max(),1)
    huizong['2_2']['速度_横向力']=round(res_2_2.loc[np.argmax(ls),'速度'],1)
    huizong['2_2']['里程_横向力']=round(res_2_2.loc[np.argmax(ls),'里程'],3)

    huizong=pd.DataFrame(huizong).T
    with pd.ExcelWriter(dir_gepian+'/各片轮轨力测试结果.xlsx') as writer:
        res_1_1.to_excel(writer, sheet_name='1_1')  
        res_1_2.to_excel(writer, sheet_name='1_2')  
        res_2_1.to_excel(writer, sheet_name='2_1')  
        res_2_2.to_excel(writer, sheet_name='2_2') 
        huizong.to_excel(writer, sheet_name='汇总') 
        
def cal_index(speed,mileage,force_left_chui,force_left_heng,force_right_chui,force_right_heng,dir_,name):               
    res={}
    res['速度']=speed
    res['里程']=mileage
    res['左轮脱轨系数']=abs(force_left_heng)/force_left_chui
    res['右轮脱轨系数']=abs(force_right_heng)/force_right_chui
    res['轮重减载率']=abs(abs(force_left_chui)-abs(force_right_chui))/((force_left_chui+force_right_chui)/2) #轮重减载率 
    res['轮轴横向力']=abs(force_left_heng-force_right_heng)
    res['左轮垂向力']=force_left_chui
    res['左轮横向力']=force_left_heng
    res['右轮垂向力']=force_right_chui
    res['右轮横向力']=force_right_heng
    res=pd.DataFrame(res)
    res=res[res['左轮垂向力']>10]
    res=res[res['右轮垂向力']>10]
     
    plot_wheel_rail_force(res,dir_,name)

    return res


# n=3
# fq=50
# sample_rate=5000
# sudu=lvbo_low(data['1']['23'],fq=3,fs=sample_rate,n=1)
# data_chui=lvbo_low(data['1']['8'],fq=fq,fs=sample_rate)[sudu>5]/n  
# data_heng=lvbo_low(data['1']['9'],fq=fq,fs=sample_rate)[sudu>5]/n      
 

# #平衡
# data_chui=data_chui-data_chui.mean() 
# data_heng=data_heng-data_heng.mean()

    




def find_max_deta_time(data_chui,sample_rate=5000,nn=1):
                                 
    '''
    按照时间提取最大值，1秒提取一个值
    '''
    #data_chui=yingbian['左1桥']['垂向']
    
    #nn=0.2
    len_=sample_rate*nn    
    n_zong=math.floor(len(data_chui)/len_)#上取整ceil   向下取整math.floor
    data_max=[]
    loc=[]

    for i in np.arange(n_zong):
        pass
        y_=data_chui[int(i*len_):int((i+1)*len_)]
        #if y_.max()>10:
            
        data_max.append(y_.max())
        loc.append(int(i*len_+np.argmax(y_))) 
    
    data_max=np.array(data_max) 
    mean = np.mean(data_max)
    sd = np.std(data_max)
    
    loc_max=np.where((data_max>mean - 2 * sd))     
    
    loc=np.array(loc) 
        
    res={'位置':loc,
         '最大值':data_max
        }
    return loc[loc_max]

 # np.where((data_max>mean - 2 * sd) & \
 #            (data_max>mean - 2 * sd) )

    
#find_max_jizhi(yingbian['左1桥']['垂向'])

def find_max_jizhi(y):
    '''
    寻找最大值点的位置
    '''
    #y=yingbian['左1桥']['垂向']
    # pd.DataFrame(y).plot()    
    loc_ls1=signal.argrelextrema(y, np.greater)

    #两者之间不能小于一个数值，否则认为是错误信号，只取最大值
    max_jianju=100
    loc_ls1=loc_ls1[0]
    
    loc_ls1_=[]
    ls=loc_ls1[0]
    for i in loc_ls1:
        pass
        if i-ls>max_jianju :
            loc_ls1_.append(i)
        else:
            if len(loc_ls1_)>0:
                if abs(y[i])>abs(y[loc_ls1_[-1]]):
                    loc_ls1_[-1]=i
                else:
                    pass
            else:
                loc_ls1_.append(i)
        ls=i 
    loc_ls1=np.array(loc_ls1_)
    
  
    # loc_ls=np.sort(np.append(loc_ls1,loc_ls2))
    res=y[loc_ls1]
    
    h=np.percentile(res,95)-np.percentile(res,5)
    high_limit=np.percentile(res,95)-h/3
    loc_max=np.where((res>high_limit)) 
    
    
    # loc_max=np.where((res>np.percentile(res,85)/2)) 
    # plt.scatter(loc_ls1[loc_max[0]],y[loc_ls1[loc_max[0]]], s=50)
    # plt.plot(range(len(y)),y) 
    # plt.xlim(70000,80000)
    # plt.show()      
    
    return loc_ls1[loc_max[0]]



def discontinuous_wheel_rail_force2(y, 
                                    sample_rate=5000,
                                    info_tongdao=None,
                                    info_biaoding=None,
                                    format='pd'
                                    ):

    # a=pd.DataFrame([res_c[50000:50000+ll],res_h[50000:50000+ll]]).T
    # a.plot()

    calibration_factor_left_0=np.linalg.inv(info_biaoding['left_1'])
    calibration_factor_left_180=np.linalg.inv(info_biaoding['left_2'])
    calibration_factor_right_0=np.linalg.inv(info_biaoding['right_1'])
    calibration_factor_right_180=np.linalg.inv(info_biaoding['right_2'])

    data=y

    # yingbian_left_chui=lvbo_daitong(data[info_tongdao['左轮垂']],fq_s=fq_s,fq_e=fq_e,fs=sample_rate,n=n)
    # yingbian_left_heng=lvbo_daitong(data[info_tongdao['左轮横']],fq_s=fq_s,fq_e=fq_e,fs=sample_rate,n=n)     
    # yingbian_right_chui=lvbo_daitong(data[info_tongdao['右轮垂']],fq_s=fq_s,fq_e=fq_e,fs=sample_rate,n=n)
    # yingbian_right_heng=lvbo_daitong(data[info_tongdao['右轮横']],fq_s=fq_s,fq_e=fq_e,fs=sample_rate,n=n)  
    fq=50
    n=3
    sudu=lvbo_low(data[info_tongdao['速度']],fq=3,fs=sample_rate,n=1)
    yingbian_left_chui=lvbo_low(data[info_tongdao['左轮垂']],fq=fq,fs=sample_rate)[sudu>5]/n  
    yingbian_left_heng=lvbo_low(data[info_tongdao['左轮横']],fq=fq,fs=sample_rate)[sudu>5]/n      
    yingbian_right_chui=lvbo_low(data[info_tongdao['右轮垂']],fq=fq,fs=sample_rate)[sudu>5]/n  
    yingbian_right_heng=lvbo_low(data[info_tongdao['右轮横']],fq=fq,fs=sample_rate)[sudu>5]/n   
    
    #平衡
    yingbian_left_chui=yingbian_left_chui-yingbian_left_chui.mean() 
    yingbian_left_heng=yingbian_left_heng-yingbian_left_heng.mean()
    yingbian_right_chui=yingbian_right_chui-yingbian_right_chui.mean()
    yingbian_right_heng=yingbian_right_heng-yingbian_right_heng.mean()
    
      
    # pd.DataFrame(yingbian_left_chui).plot()
    # pd.DataFrame(yingbian_right_chui).plot()
    
    if info_tongdao['里程']=='无':
        data_mileage_=np.array(np.arange(0,len(yingbian_left_chui)/sample_rate,1/sample_rate))
    else:
        data_mileage_=data[info_tongdao['里程']]

    # yingbian_left_chui=data[info_tongdao['左轮垂']]
    # yingbian_left_heng=data[info_tongdao['左轮横']]    
    # yingbian_right_chui=data[info_tongdao['右轮垂']]
    # yingbian_right_heng=data[info_tongdao['右轮横']]


    

    
    ##左侧轮
    #寻找应变0°和180°极值    
    loc_left_min,loc_left_max=find_min_max_location(yingbian_left_chui) 
    #得出相应应变      
    yingbian_left_max_chui=yingbian_left_chui[loc_left_max] 
    yingbian_left_max_heng=yingbian_left_heng[loc_left_max] 
    yingbian_left_min_chui=yingbian_left_chui[loc_left_min] 
    yingbian_left_min_heng=yingbian_left_heng[loc_left_min] 
    #得出相应力 
    force_left_max=np.dot(calibration_factor_left_0,np.array([yingbian_left_max_chui,yingbian_left_max_heng]))   
    force_left_min=np.dot(calibration_factor_left_0,np.array([yingbian_left_min_chui,yingbian_left_min_heng]))   
    #0°力和180°力融合
    ls=np.c_[force_left_min,force_left_max].T  #沿着矩阵列拼接
    ls=np.c_[np.append(loc_left_min,loc_left_max),ls]  #沿着矩阵行拼接   
    force_left=ls[np.argsort(ls[:,0]),:]#按照第n列排序
    
    ##右侧轮    
    #寻找应变0°和180°极值    
    loc_right_min,loc_right_max=find_min_max_location(yingbian_right_chui) 
    #得出相应应变      
    yingbian_right_max_chui=yingbian_right_chui[loc_right_max] 
    yingbian_right_max_heng=yingbian_right_heng[loc_right_max] 
    yingbian_right_min_chui=yingbian_right_chui[loc_right_min] 
    yingbian_right_min_heng=yingbian_right_heng[loc_right_min] 
    #得出相应力 
    force_right_max=np.dot(calibration_factor_right_0,np.array([yingbian_right_max_chui,yingbian_right_max_heng]))   
    force_right_min=np.dot(calibration_factor_right_0,np.array([yingbian_right_min_chui,yingbian_right_min_heng]))   
    #0°力和180°力融合
    ls=np.c_[force_right_min,force_right_max].T  #沿着矩阵列拼接
    ls=np.c_[np.append(loc_right_min,loc_right_max),ls]  #沿着矩阵行拼接   
    force_right=ls[np.argsort(ls[:,0]),:]#按照第n列排序


    #当左右轮出现选择的最大值个数不一致时，实际工程中几乎必然会出现这种情况，以点数少的为准 
    #从多的loc里面挑选出和少的最接近的数，组成一个新的loc，这样左右轮就一样多了。每一个点都是最大值，这样操作的误差可以接受    
    def fix_len(short,long):
        res=[]
        for i in short:
            pass
            idx = np.abs(long - i).argmin()
            res.append(long.flat[idx]) 
        return np.array(res)
    if len(force_left[:,0])>len(force_right[:,0]):
        loc_left=fix_len(force_right[:,0],force_left[:,0])
        force_left_=[]
        for i in loc_left:
            force_left_.append(list(force_left[force_left[:, 0]==i])[0])
        force_left=np.array(force_left_)
    elif len(force_right[:,0])>len(force_left[:,0]):
        loc_right=fix_len(force_left[:,0],force_right[:,0])
        ###采用isin是比较简单的办法，但是如果有一侧轮的数据对应另一侧两个相同值得时候，就不适用，还是需要用for来解决
        ##（即一侧数据丢失或者没有识别出来，就需要用两次同一位置数据进行补齐）
        force_right_=[]
        for i in loc_right:
            force_right_.append(list(force_right[force_right[:, 0]==i])[0])
        force_right=np.array(force_right_)
        #force_right=force_right[np.isin(force_right[:, 0], loc_)]
          
    data_mileage=data_mileage_[force_right[:,0].astype(int)]   
    sudu=sudu[force_right[:,0].astype(int)]         
    force_left_chui=abs(force_left[:,1])         
    force_left_heng=abs(force_left[:,2])
    force_right_chui=abs(force_right[:,1])    
    force_right_heng=abs(force_right[:,2])
    #jishuqi=jishuqi_[loc_right] 
    jishuqi2=np.array(range(len(data_mileage)))
    derailment_coefficient_left=abs(force_left_heng)/abs(force_left_chui)  #左脱轨系数
#    derailment_coefficient_left=derailment_coefficient_left[derailment_coefficient_left<1]
    derailment_coefficient_right=abs(force_right_heng)/abs(force_right_chui)  #右脱轨系数
#    derailment_coefficient_right=derailment_coefficient_right[derailment_coefficient_right<1] 
    derailment_coefficient=np.maximum(derailment_coefficient_left, derailment_coefficient_right, out=None)
    reduction_rate_of_wheel_load=abs(abs(force_left_chui)-abs(force_right_chui))/((force_left_chui+force_right_chui)/2) #轮重减载率 
    
    wheelset_lateral_force=abs(force_left_heng-force_right_heng)

    res={}
    res['速度']=sudu
    res['里程']=data_mileage
    res['脱轨系数1']=derailment_coefficient_left
    res['脱轨系数2']=derailment_coefficient_right 
    res['轮重减载率']=reduction_rate_of_wheel_load  
    res['轮轴横向力']=wheelset_lateral_force
    res['轮轨垂向力1']=force_left_chui
    res['轮轨横向力1']=force_left_heng
    res['轮轨垂向力2']=force_right_chui
    res['轮轨横向力2']=force_right_heng
    
    if format in ['P', 'p', 'pandas', 'pd']:
        return pd.DataFrame(res)
    elif format in ['json', 'dict']:
        return res
    # 多种数据格式
    elif format in ['n', 'N', 'numpy','np']:
        return np.asarray(res)
    elif format in ['list', 'l', 'L']:
        return np.asarray(res).tolist()
    else:
        print("输出格式错误请输入以下格式：P, p, pandas, pd , json, dict , n, N, numpy, np,list, l, L ")
        return None


    # sudu=[0]
    # for i in range(len(force_left[:,0])):
    #     pass
    #     try:   
    #         time_=(force_left[:,0][i+3]-force_left[:,0][i-3])/sample_rate
    #         sudu_=0.42*2*3.1415926/time_*3.6*3
    #         sudu.append(sudu_)
    #     except:
    #         pass
    # pd.DataFrame(sudu).plot()
    # aa=data[info_tongdao['左轮垂']][50000:60000]
    # pd.DataFrame(yingbian_left_chui).plot()
    # aaa=lvbo_daitong(aa,fq_s=0.2,fq_e=fq_e,fs=sample_rate,n=1)
    # pd.DataFrame(aaa).plot()
def plot_wheel_rail_force(res,dir_,nn):
    
    font_size_label=13
    font_size_axis=13
    font_size_legend=13 
    figsize=(8, 3.905) 
    ls_line=1.5  
    markersize=5      
    font={'size': 20,'color':'red'} 

    
    #左轮垂横力
    plt.figure(figsize=figsize) 
    plt.xlabel("里程（km）",fontdict={'size'   : font_size_label})
    plt.ylabel( '轮轨力（kN）',fontdict={'size'  : font_size_label}) 
    plt.grid(b='True',linestyle="dashed",linewidth=1)
    plt.plot(res['里程'],res['左轮垂向力'],label='左轮垂向力')      
    plt.plot(res['里程'],res['左轮横向力'],label='左轮横向力')   
    plt.legend(loc ="best",fontsize=font_size_legend)
    plt.savefig(dir_+'/'+nn+'_左轮轨力.png', dpi=200)         
    #右轮垂横力
    plt.figure(figsize=figsize) 
    plt.xlabel("里程（km）",fontdict={'size'   : font_size_label})
    plt.ylabel( '轮轨力（kN）',fontdict={'size'  : font_size_label}) 
    plt.grid(b='True',linestyle="dashed",linewidth=1)
    plt.plot(res['里程'],res['右轮垂向力'],label='右轮垂向力')      
    plt.plot(res['里程'],res['右轮横向力'],label='右轮横向力')   
    plt.legend(loc ="best",fontsize=font_size_legend)     
    plt.savefig(dir_+'/'+nn+'_右轮轨力.png', dpi=200)     
    ###脱轨系数左轮
    plt.figure(figsize=figsize) 
    plt.xlabel("里程（km）",fontdict={'size'   : font_size_label})
    plt.ylabel( '脱轨系数',fontdict={'size'  : font_size_label}) 
    plt.grid(b='True',linestyle="dashed",linewidth=1) 
    #plt.title(str(i)+'位移',fontsize=font_size_axis)
    plt.axhline(0.8,color = "r",linewidth = '3')
    plt.ylim(0,1.0)
    plt.text(2.2, 0.85, '限值', fontdict=font)       
    plt.scatter(res['里程'],res['左轮脱轨系数'], s=20,label='左轮脱轨系数') 
    plt.legend(loc ="best",fontsize=font_size_legend)#,title=str(i)+str(lab))    
    plt.savefig(dir_+'/'+nn+'_左轮脱轨系数.png', dpi=200) 
    
    ###脱轨系数右轮
    plt.figure(figsize=figsize) 
    plt.xlabel("里程（km）",fontdict={'size'   : font_size_label})
    plt.ylabel( '脱轨系数',fontdict={'size'  : font_size_label}) 
    plt.grid(b='True',linestyle="dashed",linewidth=1) 
    #plt.title(str(i)+'位移',fontsize=font_size_axis)
    plt.axhline(0.8,color = "r",linewidth = '3')
    plt.ylim(0,1.0)
    plt.text(2.2, 0.85, '限值', fontdict=font)       
    plt.scatter(res['里程'],res['右轮脱轨系数'], s=20,label='右轮脱轨系数') 
    plt.legend(loc ="best",fontsize=font_size_legend)#,title=str(i)+str(lab))    
    plt.savefig(dir_+'/'+nn+'_右轮脱轨系数.png', dpi=200)      
    #轮重减载率
    plt.figure(figsize=figsize) 
    plt.xlabel("里程（km）",fontdict={'size'   : font_size_label})
    plt.ylabel( '轮重减载率',fontdict={'size'  : font_size_label})    
    plt.grid(b='True',linestyle="dashed",linewidth=1)     
    plt.axhline(0.65,color = "r",linewidth = '3')
    plt.ylim(0,0.8) 
    plt.text(2.2, 0.67, '限值', fontdict=font)  

    plt.scatter(res['里程'],res['轮重减载率'], s=20,label='轮重减载率')  
    plt.legend(loc ="best",fontsize=font_size_legend)
    plt.savefig(dir_+'/'+nn+'_轮重减载率.png', dpi=200)    
    #轮轴横向力
    xianzhi=15+50/3
    plt.figure(figsize=figsize) 

    plt.xlabel("里程（km）",fontdict={'size'   : font_size_label})
    plt.ylabel( '轮轴横向力（kN）',fontdict={'size'  : font_size_label}) 
    plt.grid(b='True',linestyle="dashed",linewidth=1)     
    plt.text(2.2, xianzhi+2, '限值', fontdict=font) 
    plt.axhline(xianzhi,color = "r",linewidth = '3')
    plt.ylim(0,xianzhi*1.3)   
    plt.scatter(res['里程'],res['轮轴横向力'], s=20,label='轮轴横向力')   
    plt.legend(loc ="best",fontsize=font_size_legend)       
    plt.savefig(dir_+'/'+nn+'_轮轴横向力.png', dpi=200)      
    # aa=derailment_coefficient
    # print('脱轨系数')
    # print(aa.max() )  
    # print(data_mileage[np.argmax(aa)]  )       
    # print(sudu2[np.argmax(aa)])
    
    # aa=reduction_rate_of_wheel_load
    # print(aa.max() )  
    # print(data_mileage[np.argmax(aa)]  )       
    # print(sudu2[np.argmax(aa)]) 
      
    
    # aa=wheelset_lateral_force  
    # print(aa.max() )  
    # print(data_mileage[np.argmax(aa)]  )       
    # print(sudu2[np.argmax(aa)]) 

    # pd.DataFrame(sudu2).plot()
    # force_right[0]
    # res_c=force_right[0][9500:10500]
    # res_h=force_left[0][9500:10500]
    # loc,force_chui=find_max_location(res_c)
    # force_heng=res_h[loc]     
    
    # plt.figure(figsize=(16,4))   
    # plt.plot(range(len(res_c)),res_c)
    # plt.scatter(loc,force_chui, s=50)
    # plt.plot(range(len(res_h)),res_h)
    # plt.scatter(loc,force_heng, s=50)   
    # plt.plot(range(len(res_h)),[0]*len(res_h))    
    # plt.show()    


       
    
"""
    [B,A] = BUTTER(N,Wn,'high') designs a highpass filter.高通滤波器
    [B,A] = BUTTER(N,Wn,'low') designs a lowpass filter.低通滤波器
    [B,A] = BUTTER(N,Wn,'stop') is a bandstop filter if Wn = [W1 W2].
    [B,A] = BUTTER(N,Wn)--带通滤波器 
    
比如说你的采样频率fs=1000Hz，设计一个8阶、通带为fc1=100,fc2=200Hz的带通滤波器：
[b,a]=butter(8,[0.2 0.4])=butter(8,fc1/fa fc2/fa])
这里fa=fs/2，fa是分析频率    
"""


if __name__ == '__main__':  
    pass
    
    dir_='E:/城轨中心/2项目/20211031天津6号线轮轨力/天津6'
    name='天津6号线测试'
    # ###天津
    # info_tongdao={'左轮垂':'3',
    #  '左轮横':'4',
    #  '右轮垂':'7',  
    #  '右轮横':'8', 
    #  '里程':'无',
    
    #  }
    # info_biaoding={
    #     'left_0':np.array([[-0.719,0.3],[0.041,-2.32]]) ,
    #     'left_180':np.array([[0.716,-0.341],[-0.038,2.283]]),
    #     'right_0':np.array([[-0.711,-0.353],[0.062,-2.299]]) ,
    #     'right_180':np.array([[0.714,-0.427],[-0.042,2.322]]),
    #  } 
    # y=data['1']
    # fq_s=0.2
    # fq_e=50
    # sample_rate=5000

    # import vtda
    
    # dir_='E:/城轨中心/2项目/20210615昆明车辆异常晃动/昆明加速度数据/昆明1、2号线/上行-大学城南-北部汽车站'
    # name='20210126昆明地铁1、2、呈贡支线测试'
    # dir_='E:/城轨中心/2项目/20211031天津6号线轮轨力/天津6'
    # name='天津6号线测试'
    # data,info=vtda.read_dasp_data(name,dir_=dir_,num_shiyan='1')
   #  i='1'
   #  j='17'
   #  y=data[i][j]
   #  a=pd.DataFrame(y)
   #  a.plot()      
   #  y1=data['1']['1']/100 
   #  y2=data['1']['2']/100 
   #  a=pd.DataFrame([y1,y2]).T
   #  a.plot()  
    
   #  res1=lvbo_low(y1,fq=2,fs=500)[50000:50000+5000]
   #  res2=lvbo_low(y2,fq=2,fs=500)[50000:50000+5000]
    
   #  a=pd.DataFrame([res1,res2]).T
   #  a.plot()
   #  res1=lvbo_low(y1,fq=30,fs=500)[50000:50000+5000]
   #  res1=lvbo_high(res1,fq=2,fs=500)
       
   #  ll=500
   #  i='1'
   #  j='9'  
   #  res_c=lvbo_daitong(data[i][j]/100,fq_s=2,fq_e=50,fs=500,n=6)[50000:50000+ll]
   #  i='1'
   #  j='10'  
   #  res_h=lvbo_daitong(data[i][j]/100,fq_s=2,fq_e=50,fs=500,n=6)[50000:50000+ll]
 
    
   #  loc,force_chui=find_max_location(res_c)
   #  force_heng=res_h[loc]    
   #  force=np.array([force_chui,force_heng])
   #  force=abs(np.dot(tj6_t_1,force))
    
   #  左脱轨系数=force[1]/force[0]  
    
   #  plt.figure(figsize=(16,4))   
   #  plt.plot(range(len(res_c)),res_c)
   #  plt.scatter(loc,force_chui, s=50)
   #  plt.plot(range(len(res_h)),res_h)
   #  plt.scatter(loc,force_heng, s=50)   
   #  plt.plot(range(len(res_h)),[0]*len(res_h))    
   #  plt.show()   


   #  pd.DataFrame(res1).plot()
   #  a1,a2=fft(res1 ,
   #                   sample_rate =500,
   #                   fft_size = 500,
   #                   window='hanning',
   #                   cdxs=0.75)
   #  pd.DataFrame(a2).plot()
    

   #  pd.DataFrame(res1[:500]).plot()
   #  x=res1[:500]
   #  plt.figure(figsize=(16,4))
   #  plt.plot(np.arange(len(x)),x)
   #  loc_ls1=signal.argrelextrema(x, np.greater)
   #  loc_ls2=signal.argrelextrema(-x, np.greater)
   #  loc_ls=np.append(loc_ls1,loc_ls2)
   #  res=np.append(x[loc_ls1],x[loc_ls2])
    
   #  loc=np.where(
   #      (res<(res.min()+res.mean())/2) | \
   #      (res>(res.mean()+res.max())/2)
   #      )
   #  res=res[loc]
        
   #  plt.plot(range(len(x)),x)
   # # plt.plot(loc_ls[loc],res,'+') 
    
   #  plt.scatter(loc_ls[loc],res, s=50)
   #  plt.show()    
   #  #signal.argrelextrema(x,np.greater)[0],
   #  #plt.plot(,'o')
   #  plt.plot(signal.argrelextrema(x,np.greater)[0],x[signal.argrelextrema(x, np.greater)],'+')    
   #  plt.plot(signal.argrelextrema(-x,np.greater)[0],x[signal.argrelextrema(-x, np.greater)],'+')
   #  # plt.plot(peakutils.index(-x),x[peakutils.index(-x)],'*')
   #  plt.show()


    
    # plt.figure(figsize=(10, 6))
    # plt.plot(range(len(res1)),res1)
    
    # t1=time.time()
    # time_,spr=sperling(y,  #数据
    #         sample_rate=4096, #采样频率
    #         len_=5, #分析窗长
    #         window='hanning', #窗函数
    #         cdxs=0.8, #重叠系数
    #         direction='垂向', #或者填横向  #数据方向
    #         )
    # print(time.time()-t1)
    
    # plt.figure(figsize=(10, 6))
    # plt.plot(time_,spr)   
    
    
    # tj6_t_1_0=np.array([[0.724,-0.243],
    #            [-0.027,1.938]])
    # tj6_t_1_90=np.array([[0.724,-0.243],
    #            [-0.027,1.938]])
    # tj6_t_1_180=np.array([[0.73,-0.257],
    #            [-0.034,1.946]])   
    # tj6_t_1_270=np.array([[0.693,-0.259],
    #        [-0.03,1.973]])
    # tj6_t_1=(tj6_t_1_0+tj6_t_1_90+tj6_t_1_180+tj6_t_1_270)/4
    
    
    # tj6_t_2_0=np.array([[0.738,-0.276],
    #            [-0.06,2.139]])
    # tj6_t_2_90=np.array([[0.699,-0.26],
    #            [-0.05,2.072]])
    # tj6_t_2_180=np.array([[0.713,-0.297],
    #            [-0.07,2.098]])   
    # tj6_t_2_270=np.array([[0.667,-0.266],
    #        [-0.058,2.099]])    
    # tj6_t_2=(tj6_t_2_0+tj6_t_2_90+tj6_t_2_180+tj6_t_2_270)/4   
    
    
    # tj6_d_1_0=np.array([[0.689,-0.338],
    #            [-0.031,2.196]])
    # tj6_d_1_90=np.array([[0.684,-0.353],
    #            [-0.032,2.213]])
    # tj6_d_1_180=np.array([[0.687,-0.359],
    #            [-0.034,2.154]])   
    # tj6_d_1_270=np.array([[0.693,-0.331],
    #        [-0.03,2.171]])
    # tj6_d_1=(tj6_d_1_0+tj6_d_1_90+tj6_d_1_180+tj6_d_1_270)/4
     

    # tj6_d_2_0=np.array([[0.669,-0.378],
    #            [-0.065,2.217]])
    # tj6_d_2_90=np.array([[0.658,-0.378],
    #            [-0.048,2.226]])
    # tj6_d_2_180=np.array([[0.669,-0.397],
    #            [-0.054,2.167]])   
    # tj6_d_2_270=np.array([[0.667,-0.388],
    #        [-0.058,2.19]]) 
    # tj6_d_2=(tj6_d_2_0+tj6_d_2_90+tj6_d_2_180+tj6_d_2_270)/4     