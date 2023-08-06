# -*- coding: utf-8 -*-
"""
Created on Sat Jun 26 21:23:50 2021

@author: ZSL
"""
import numpy as np
import math
import time
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from vtda.util.util import weight_factor

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
from vtda.analysis.base import (               choose_windows,
                                               fft,
                                               octave_3,
                                               base_level,
                                               rms_time,
                                               rms_frec,
                                            )

def sperling(y, 
            sample_rate=4096,
            len_=5,
            window='hanning',
            cdxs=0.8,
            direction='vertical', #horizontal
            unit='m/ss',#g
            n=1 #保留结果小数点后位数
            ):
    '''
    计算平稳性函数
    Parameters
    ----------
    y : TYPE
        待计算数据，可以为np.ndarray或者 pd.Series格式
    sample_rate : TYPE, optional
        采样点数，默认为4096，如果待计算数据为pd.Series格式，其中有采样频率信息，则优先采用其信息。
    len : TYPE, optional
        分析长度，默认为5秒
    window : TYPE, optional
        加窗，默认为汉宁窗
    cdxs : TYPE, optional
        重叠系数，默认为0
    Returns
    -------
    返回两个结果list，一个为时间，另一个为随时间变化的平稳性

    '''

    if isinstance(y, pd.DataFrame) or isinstance(y, pd.Series):
        sample_rate=1/(y.index[1]-y.index[0])
        y=y.fillna(0)
        y=np.array(y)        
    elif isinstance(y, np.ndarray):
        pass
    else:
        print("{} 错误数据输入格式。。。".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))             
    
    if unit=='m/ss':
        pass
    elif unit=='g':
        y=y*9.8
    
    fft_size=len_*sample_rate   
    n_zong=max(math.ceil((len(y)-fft_size)/(round((1-cdxs),5)*fft_size))+1,1)#上取整
    res=np.zeros(int(fft_size/2))
    res_sperling=[]
    res_x=[]
    for i in tqdm(np.arange(n_zong),desc='正在计算平稳性'):
        pass
        #i=4
        y_=y[int(i*round((1-cdxs),5)*fft_size):int(i*round((1-cdxs),5)*fft_size+fft_size)][:int(fft_size)] 
        if len(y_)>0:
            res_x,res_y_=fft(y_,
                             sample_rate=sample_rate,
                             fft_size =fft_size,
                             cdxs=cdxs,
                             fix_meth='能量修正',
                             window=window,
                             )
            if direction in ['vertical','v','V','chui','chuixiang','垂','垂向']: #垂向
                w=[]
                for i in np.arange(len(res_x)):
                    pass
                    x_fft=res_x[i]
                    y_fft=res_y_[i]
                    if x_fft>=0.5 and x_fft<5.9:
                        w_ls=7.08*math.pow((y_fft**3*0.325*x_fft), 1/10)
                        w.append(w_ls)
                    elif x_fft>=5.9 and x_fft<20:
                        w_ls=7.08*math.pow((y_fft**3*400/(x_fft**3)), 1/10)
                        w.append(w_ls)    
                    elif x_fft>=20 and x_fft<=40:
                        w_ls=7.08*math.pow((y_fft**3/x_fft), 1/10)
                        w.append(w_ls)
                ww=math.pow(sum([i**10 for i in w]), 1/10)
            elif direction in ['horizontal','h','H','heng','hengxiang','横','横向']: #横向
                w=[]
                for i in np.arange(len(res_x)):
                    pass
                    x_fft=res_x[i]
                    y_fft=res_y_[i]
                    if x_fft>=0.5 and x_fft<5.4:
                        w_ls=7.08*math.pow((y_fft**3*0.8*x_fft), 1/10)
                        w.append(w_ls)
                    elif x_fft>=5.4 and x_fft<26:
                        w_ls=7.08*math.pow((y_fft**3*650/(x_fft**3)), 1/10)
                        w.append(w_ls)    
                    elif x_fft>=26 and x_fft<=40:
                        w_ls=7.08*math.pow((y_fft**3/x_fft), 1/10)
                        w.append(w_ls)
                ww=math.pow(sum([i**10 for i in w]), 1/10)            

            res_sperling.append(ww)
            
    ls=round(len_*(1-cdxs),2)
    ls_z=ls*(n_zong)+len_
    res_x=list(np.arange(len_,ls_z,ls))
#    res_x.append((len(y_)/fft_size)*len_+len_*(n_zong-1))  #解决最后一个不整的问题
    return res_x,res_sperling

def discontinuous_wheel_rail_force(y, 
                                    sample_rate=500,
                                    fq_s=2,
                                    fq_e=50,
                                    n=1 #保留结果小数点后位数
                                    ):
    pass

    # a=pd.DataFrame([res_c[50000:50000+ll],res_h[50000:50000+ll]]).T
    # a.plot()
    tj6_t_1_0=np.array([[0.724,-0.243],
               [-0.027,1.938]])
    tj6_t_1_90=np.array([[0.724,-0.243],
               [-0.027,1.938]])
    tj6_t_1_180=np.array([[0.73,-0.257],
               [-0.034,1.946]])   
    tj6_t_1_270=np.array([[0.693,-0.259],
           [-0.03,1.973]])
    tj6_t_1=(tj6_t_1_0+tj6_t_1_90+tj6_t_1_180+tj6_t_1_270)/4
    
    
    tj6_t_2_0=np.array([[0.738,-0.276],
               [-0.06,2.139]])
    tj6_t_2_90=np.array([[0.699,-0.26],
               [-0.05,2.072]])
    tj6_t_2_180=np.array([[0.713,-0.297],
               [-0.07,2.098]])   
    tj6_t_2_270=np.array([[0.667,-0.266],
           [-0.058,2.099]])    
    tj6_t_2=(tj6_t_2_0+tj6_t_2_90+tj6_t_2_180+tj6_t_2_270)/4   
    
    
    tj6_d_1_0=np.array([[0.689,-0.338],
               [-0.031,2.196]])
    tj6_d_1_90=np.array([[0.684,-0.353],
               [-0.032,2.213]])
    tj6_d_1_180=np.array([[0.687,-0.359],
               [-0.034,2.154]])   
    tj6_d_1_270=np.array([[0.693,-0.331],
           [-0.03,2.171]])
    tj6_d_1=(tj6_d_1_0+tj6_d_1_90+tj6_d_1_180+tj6_d_1_270)/4
     

    tj6_d_2_0=np.array([[0.669,-0.378],
               [-0.065,2.217]])
    tj6_d_2_90=np.array([[0.658,-0.378],
               [-0.048,2.226]])
    tj6_d_2_180=np.array([[0.669,-0.397],
               [-0.054,2.167]])   
    tj6_d_2_270=np.array([[0.667,-0.388],
           [-0.058,2.19]]) 
    tj6_d_2=(tj6_d_2_0+tj6_d_2_90+tj6_d_2_180+tj6_d_2_270)/4     
    

    info={'左轮垂':'1',
     '左轮横':'2',
     '右轮垂':'5',  
     '右轮横':'6', 
     '里程':'DT0'
     }
    calibration_factor_left_0=np.linalg.inv(tj6_t_1_0)
    calibration_factor_left_180=np.linalg.inv(tj6_t_1_180)
    calibration_factor_right_0=np.linalg.inv(tj6_t_2_0)
    calibration_factor_right_180=np.linalg.inv(tj6_t_2_180)

    data=data['1']
    
    
    yingbian_left_chui=lvbo_daitong(data[info['左轮垂']],fq_s=fq_s,fq_e=fq_e,fs=sample_rate,n=6)[31000:31000+20000]
    yingbian_left_heng=lvbo_daitong(data[info['左轮横']],fq_s=fq_s,fq_e=fq_e,fs=sample_rate,n=6)[31000:31000+20000]     
    yingbian_right_chui=lvbo_daitong(data[info['右轮垂']],fq_s=fq_s,fq_e=fq_e,fs=sample_rate,n=6)[31000:31000+20000]
    yingbian_right_heng=lvbo_daitong(data[info['右轮横']],fq_s=fq_s,fq_e=fq_e,fs=sample_rate,n=6)[31000:31000+20000]   
    data_mileage_=data[info['里程']][31000:31000+20000] 
    
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
    force_left_chui=abs(force_left[:,1])         
    force_left_heng=force_left[:,2]
    force_right_chui=abs(force_right[:,1])    
    force_right_heng=force_right[:,2]
    #jishuqi=jishuqi_[loc_right] 
    jishuqi2=np.array(range(len(data_mileage)))
    derailment_coefficient_left=abs(force_left_heng)/abs(force_left_chui)  #左脱轨系数
#    derailment_coefficient_left=derailment_coefficient_left[derailment_coefficient_left<1]
    derailment_coefficient_right=abs(force_right_heng)/abs(force_right_chui)  #右脱轨系数
#    derailment_coefficient_right=derailment_coefficient_right[derailment_coefficient_right<1] 
    derailment_coefficient=np.maximum(derailment_coefficient_left, derailment_coefficient_right, out=None)
    reduction_rate_of_wheel_load=abs(abs(force_left_chui)-abs(force_right_chui))/((force_left_chui+force_right_chui)/2) #轮重减载率 
    
    wheelset_lateral_force=abs(force_left_heng-force_right_heng)

    font_size_label=13
    font_size_axis=13
    font_size_legend=13 
    figsize=(8, 3.905) 
    ls_line=1.5  
    markersize=5      
    font={'size': 20,'color':'red'} 
    ###脱轨系数
    plt.figure(figsize=figsize) 
    plt.xlabel("里程（km）",fontdict={'size'   : font_size_label})
    plt.ylabel( '脱轨系数',fontdict={'size'  : font_size_label}) 
    plt.grid(b='True',linestyle="dashed",linewidth=1) 
    #plt.title(str(i)+'位移',fontsize=font_size_axis)
    plt.axhline(0.8,color = "r",linewidth = '3')
    plt.ylim(0,1.0)
    plt.text(2.2, 0.85, '限值', fontdict=font)       
    plt.scatter(data_mileage,derailment_coefficient, s=20,label='脱轨系数') 
    plt.legend(loc ="best",fontsize=font_size_legend)#,title=str(i)+str(lab))    
    #plt.savefig(dir_disp+'/'+'位移'+str(i)+'7-8.png', dpi=200)  
    
    #轮重减载率
    plt.figure(figsize=figsize) 
    plt.xlabel("里程（km）",fontdict={'size'   : font_size_label})
    plt.grid(b='True',linestyle="dashed",linewidth=1)     
    plt.axhline(0.65,color = "r",linewidth = '3')
    plt.ylim(0,0.8) 
    plt.text(2.2, 0.67, '限值', fontdict=font)  
    plt.ylabel( '轮重减载率',fontdict={'size'  : font_size_label})
    plt.scatter(data_mileage,reduction_rate_of_wheel_load, s=20,label='轮重减载率')  
    plt.legend(loc ="best",fontsize=font_size_legend)
    #轮轴横向力
    xianzhi=15+50/3
    plt.figure(figsize=figsize) 

    plt.xlabel("里程（km）",fontdict={'size'   : font_size_label})
    plt.ylabel( '轮轴横向力',fontdict={'size'  : font_size_label}) 
    plt.grid(b='True',linestyle="dashed",linewidth=1)     
    plt.text(2.2, xianzhi+2, '限值', fontdict=font) 
    plt.axhline(xianzhi,color = "r",linewidth = '3')
    plt.ylim(0,xianzhi*1.3)   
    plt.ylabel( '轮轴横向力（kN）',fontdict={'size'  : font_size_label})
    plt.scatter(data_mileage,wheelset_lateral_force, s=20,label='轮轴横向力')   
    plt.legend(loc ="best",fontsize=font_size_legend)       
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

def find_min_max_location(y):
    '''
    寻找最大值、极小值的点的位置
    '''
    #y=yingbian_left_chui
    
    loc_ls1=signal.argrelextrema(y, np.greater)
    
    loc_ls2=signal.argrelextrema(-y, np.greater)
    
    #两者之间不能小于一个数值，否则认为是错误信号，只取最大值
    max_jianju=20
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
    loc_ls1=loc_ls1_
           
    loc_ls2=loc_ls2[0]  
    loc_ls2_=[]    
    ls=loc_ls2[0]
    for i in loc_ls2:
        pass
        if i-ls>max_jianju :
            loc_ls2_.append(i)
        else:
            if len(loc_ls2_)>0:
                if abs(y[i])>abs(y[loc_ls2_[-1]]):
                    loc_ls2_[-1]=i
                else:
                    pass
            else:
                loc_ls2_.append(i)
        ls=i 
    loc_ls2=loc_ls2_ 
    
    loc_ls=np.sort(np.append(loc_ls1,loc_ls2))
    res=y[loc_ls]
    h=np.percentile(res,95)-np.percentile(res,5)
    high_limit=np.percentile(res,99)-h/8
    low_limit=np.percentile(res,1)+h/8
    # loc=np.where(
    #     (res<low_limit) | \
    #     (res>high_limit)
    #     )
    loc_max=np.where((res>high_limit)) 
    loc_min=np.where((res<low_limit)) 
    return loc_ls[loc_min],loc_ls[loc_max]
    
    plt.figure(figsize=(16,4))
    plt.plot(np.arange(len(y)),y)    
    plt.plot(range(len(y)),y)
    plt.scatter(loc_ls[loc],res, s=50)
    plt.show()     
    
"""
    [B,A] = BUTTER(N,Wn,'high') designs a highpass filter.高通滤波器
    [B,A] = BUTTER(N,Wn,'low') designs a lowpass filter.低通滤波器
    [B,A] = BUTTER(N,Wn,'stop') is a bandstop filter if Wn = [W1 W2].
    [B,A] = BUTTER(N,Wn)--带通滤波器 
    
比如说你的采样频率fs=1000Hz，设计一个8阶、通带为fc1=100,fc2=200Hz的带通滤波器：
[b,a]=butter(8,[0.2 0.4])=butter(8,fc1/fa fc2/fa])
这里fa=fs/2，fa是分析频率    
"""
from scipy import signal

def lvbo_low(lb_q,fq=20,fs=4096):
    '''
    低通滤波函数
    Parameters
    ----------
    lb_q : TYPE
        滤波前数据
    fq : TYPE, optional
        滤波频率范围
    fs : TYPE, optional
        数据采样频率

    '''
    b,a = signal.butter(8,fq/(fs/2),'low')  #20Hz
    lb_h = signal.filtfilt(b,a,lb_q)
    return lb_h

def lvbo_high(lb_q,fq=20,fs=4096):
    '''
    高通滤波函数
    Parameters
    ----------
    lb_q : TYPE
        滤波前数据
    fq : TYPE, optional
        滤波频率范围
    fs : TYPE, optional
        数据采样频率

    '''
    b,a = signal.butter(8,fq/(fs/2),'high')  #20Hz
    lb_h = signal.filtfilt(b,a,lb_q)
    return lb_h

def lvbo_daitong(lb_q,fq_s=20,fq_e=50,fs=4096,n=8):
    '''
    带通滤波函数
    Parameters
    ----------
    lb_q : TYPE
        滤波前数据
    fq : TYPE, optional
        滤波频率范围
    fs : TYPE, optional
        数据采样频率

    '''
    # aa=np.random.randn(10000)
    # fq_s=2
    # fq_e=50
    # fs=4096
    # lb_q=aa
    b,a = signal.butter(n,[fq_s/(fs/2),fq_e/(fs/2)],'bandpass')  #20Hz
    lb_h = signal.filtfilt(b,a,lb_q)
    return lb_h

def lvbo_daizu(lb_q,fq_s=2,fq_e=30,fs=500,n=8):
    '''
    带阻滤波函数
    Parameters
    ----------
    lb_q : TYPE
        滤波前数据
    fq : TYPE, optional
        滤波频率范围
    fs : TYPE, optional
        数据采样频率

    '''
    
    b,a = signal.butter(n,[fq_s/(fs/2),fq_e/(fs/2)],'stop')  #20Hz
    lb_h = signal.filtfilt(b,a,lb_q)
    return lb_h

if __name__ == '__main__':  
    pass
    
    import vtda
    
    dir_='E:/城轨中心/2项目/20210615昆明车辆异常晃动/昆明加速度数据/昆明1、2号线/上行-大学城南-北部汽车站'
    name='20210126昆明地铁1、2、呈贡支线测试'
    dir_='E:/城轨中心/2项目/20211031天津6号线轮轨力/天津6'
    name='天津6号线测试'
    data,info=vtda.read_dasp_data(name,dir_=dir_,num_shiyan='1')
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
