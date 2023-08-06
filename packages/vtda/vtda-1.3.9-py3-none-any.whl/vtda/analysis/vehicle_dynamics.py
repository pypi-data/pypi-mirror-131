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
    h=np.percentile(res,85)-np.percentile(res,15)
    high_limit=np.percentile(res,85)-h/6
    low_limit=np.percentile(res,15)+h/6
    # loc=np.where(
    #     (res<low_limit) | \
    #     (res>high_limit)
    #     )
    loc_max=np.where((res>high_limit)) 
    loc_min=np.where((res<low_limit)) 
    return loc_ls[loc_min],loc_ls[loc_max]



def discontinuous_wheel_rail_force(y, 
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
    
      
    pd.DataFrame(yingbian_left_chui).plot()
    pd.DataFrame(yingbian_right_chui).plot()
    
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
    res['轮轨横向力2']=force_right_chui    
    
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
def plot_wheel_rail_force(res):
    
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
    plt.plot(res,force_left_chui,label='左轮垂向力')      
    plt.plot(data_mileage,force_left_heng,label='左轮横向力')   
    plt.legend(loc ="best",fontsize=font_size_legend)       
    #右轮垂横力
    plt.figure(figsize=figsize) 
    plt.xlabel("里程（km）",fontdict={'size'   : font_size_label})
    plt.ylabel( '轮轨力（kN）',fontdict={'size'  : font_size_label}) 
    plt.grid(b='True',linestyle="dashed",linewidth=1)
    plt.plot(data_mileage,force_right_chui,label='右轮垂向力')      
    plt.plot(data_mileage,force_right_heng,label='右轮横向力')   
    plt.legend(loc ="best",fontsize=font_size_legend)     
    
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
    plt.ylabel( '轮重减载率',fontdict={'size'  : font_size_label})    
    plt.grid(b='True',linestyle="dashed",linewidth=1)     
    plt.axhline(0.65,color = "r",linewidth = '3')
    plt.ylim(0,0.8) 
    plt.text(2.2, 0.67, '限值', fontdict=font)  

    plt.scatter(data_mileage,reduction_rate_of_wheel_load, s=20,label='轮重减载率')  
    plt.legend(loc ="best",fontsize=font_size_legend)
    #轮轴横向力
    xianzhi=15+50/3
    plt.figure(figsize=figsize) 

    plt.xlabel("里程（km）",fontdict={'size'   : font_size_label})
    plt.ylabel( '轮轴横向力（kN）',fontdict={'size'  : font_size_label}) 
    plt.grid(b='True',linestyle="dashed",linewidth=1)     
    plt.text(2.2, xianzhi+2, '限值', fontdict=font) 
    plt.axhline(xianzhi,color = "r",linewidth = '3')
    plt.ylim(0,xianzhi*1.3)   
    plt.scatter(data_mileage,wheelset_lateral_force, s=20,label='轮轴横向力')   
    plt.legend(loc ="best",fontsize=font_size_legend)       
 
    sudu2=sudu[sudu>5]    
    aa=derailment_coefficient
    print(aa.max() )  
    print(data_mileage[np.argmax(aa)]  )       
    print(sudu2[np.argmax(aa)])
    
    aa=reduction_rate_of_wheel_load
    print(aa.max() )  
    print(data_mileage[np.argmax(aa)]  )       
    print(sudu2[np.argmax(aa)]) 
      
    
    aa=wheelset_lateral_force  
    print(aa.max() )  
    print(data_mileage[np.argmax(aa)]  )       
    print(sudu2[np.argmax(aa)]) 

    pd.DataFrame(sudu2).plot()
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