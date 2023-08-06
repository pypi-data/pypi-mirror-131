# -*- coding: utf-8 -*-
"""
Created on Mon Nov 22 17:28:26 2021

@author: Administrator
"""

    calibration_factor_left_0=np.linalg.inv(info_biaoding['left_0'])
    calibration_factor_left_90=np.linalg.inv(info_biaoding['left_90'])    
    calibration_factor_left_180=np.linalg.inv(info_biaoding['left_180'])
    calibration_factor_left_270=np.linalg.inv(info_biaoding['left_270'])    
    calibration_factor_right_0=np.linalg.inv(info_biaoding['right_0'])
    calibration_factor_right_90=np.linalg.inv(info_biaoding['right_90'])    
    calibration_factor_right_180=np.linalg.inv(info_biaoding['right_180'])
    calibration_factor_right_270=np.linalg.inv(info_biaoding['right_270']) 


    fq=50     #50Hz低通滤波
    n=3   #董工数采应变有个3倍的关系，此处除以3 
    speed=lvbo_low(data[info_tongdao['速度']],fq=3,fs=sample_rate,n=1)
    mileage=data[info_tongdao['里程']]    
    yingbian_left_chui_1=lvbo_low(data[info_tongdao['左轮垂1']],fq=fq,fs=sample_rate)[speed>5]/n  
    yingbian_left_heng_1=lvbo_low(data[info_tongdao['左轮横1']],fq=fq,fs=sample_rate)[speed>5]/n      
    yingbian_right_chui_1=lvbo_low(data[info_tongdao['右轮垂1']],fq=fq,fs=sample_rate)[speed>5]/n  
    yingbian_right_heng_1=lvbo_low(data[info_tongdao['右轮横1']],fq=fq,fs=sample_rate)[speed>5]/n   

    yingbian_left_chui_2=lvbo_low(data[info_tongdao['左轮垂2']],fq=fq,fs=sample_rate)[speed>5]/n  
    yingbian_left_heng_2=lvbo_low(data[info_tongdao['左轮横2']],fq=fq,fs=sample_rate)[speed>5]/n      
    yingbian_right_chui_2=lvbo_low(data[info_tongdao['右轮垂2']],fq=fq,fs=sample_rate)[speed>5]/n  
    yingbian_right_heng_2=lvbo_low(data[info_tongdao['右轮横2']],fq=fq,fs=sample_rate)[speed>5]/n   
      
    #平衡
    yingbian_left_chui_1=yingbian_left_chui_1-yingbian_left_chui_1.mean() 
    yingbian_left_heng_1=yingbian_left_heng_1-yingbian_left_heng_1.mean()
    yingbian_right_chui_1=yingbian_right_chui_1-yingbian_right_chui_1.mean()
    yingbian_right_heng_1=yingbian_right_heng_1-yingbian_right_heng_1.mean()    
    yingbian_left_chui_2=yingbian_left_chui_2-yingbian_left_chui_2.mean() 
    yingbian_left_heng_2=yingbian_left_heng_2-yingbian_left_heng_2.mean()
    yingbian_right_chui_2=yingbian_right_chui_2-yingbian_right_chui_2.mean()
    yingbian_right_heng_2=yingbian_right_heng_2-yingbian_right_heng_2.mean()     


    
    loc_left_chui_1_1,force_left_chui_1_1,force_left_heng_1_1=dcon_wheel_rail_force_single_deta_time(yingbian_left_chui_1,
                                           yingbian_left_heng_1,
                                           sample_rate=sample_rate,
                                           info_biaoding=calibration_factor_left_180
                                           )
    speed_left_1_1=speed[loc_left_chui_1_1]
    mileage_left_1_1=mileage[loc_left_chui_1_1]    
    #求下沿应变需要对数值负数进行求解最大值即可
    loc_left_chui_1_2,force_left_chui_1_2,force_left_heng_1_2=dcon_wheel_rail_force_single_deta_time(-yingbian_left_chui_1,
                                           -yingbian_left_heng_1,
                                           sample_rate=sample_rate,
                                           info_biaoding=calibration_factor_left_0
                                           )
    force_left_chui_1_2=-force_left_chui_1_2
    force_left_heng_1_2=-force_left_heng_1_2
    speed_left_1_2=speed[loc_left_chui_1_2]
    mileage_left_1_2=mileage[loc_left_chui_1_2]    

    loc_left_chui_2_1,force_left_chui_2_1,force_left_heng_2_1=dcon_wheel_rail_force_single_deta_time(yingbian_left_chui_2,
                                           yingbian_left_heng_2,
                                           sample_rate=sample_rate,
                                           info_biaoding=calibration_factor_left_270
                                           )
    speed_left_2_1=speed[loc_left_chui_2_1]
    mileage_left_2_1=mileage[loc_left_chui_2_1]     
    #求下沿应变需要对数值负数进行求解最大值即可    
    loc_left_chui_2_2,force_left_chui_2_2,force_left_heng_2_2=dcon_wheel_rail_force_single_deta_time(-yingbian_left_chui_2,
                                           -yingbian_left_heng_2,
                                           sample_rate=sample_rate,
                                           info_biaoding=calibration_factor_left_90
                                           )
    force_left_chui_2_2=-force_left_chui_2_2
    force_left_heng_2_2=-force_left_heng_2_2    
    speed_left_2_2=speed[loc_left_chui_2_2]
    mileage_left_2_2=mileage[loc_left_chui_2_2]  
    
    loc_right_chui_1_1,force_right_chui_1_1,force_right_heng_1_1=dcon_wheel_rail_force_single_deta_time(yingbian_right_chui_1,
                                           yingbian_right_heng_1,
                                           sample_rate=sample_rate,
                                           info_biaoding=calibration_factor_right_180
                                           )
    speed_right_1_1=speed[loc_right_chui_1_1]
    mileage_right_1_1=mileage[loc_right_chui_1_1]     
    loc_right_chui_1_2,force_right_chui_1_2,force_right_heng_1_2=dcon_wheel_rail_force_single_deta_time(-yingbian_right_chui_1,
                                           -yingbian_right_heng_1,
                                           sample_rate=sample_rate,
                                           info_biaoding=calibration_factor_right_0
                                           )
    force_right_chui_1_2=-force_right_chui_1_2
    force_right_heng_1_2=-force_right_heng_1_2
    speed_right_1_2=speed[loc_right_chui_1_2]
    mileage_right_1_2=mileage[loc_right_chui_1_2] 
    loc_right_chui_2_1,force_right_chui_2_1,force_right_heng_2_1=dcon_wheel_rail_force_single_deta_time(yingbian_right_chui_2,
                                           yingbian_right_heng_2,
                                           sample_rate=sample_rate,
                                           info_biaoding=calibration_factor_right_270
                                           )
    speed_right_2_1=speed[loc_right_chui_2_1]
    mileage_right_2_1=mileage[loc_right_chui_2_1]     
    loc_right_chui_2_2,force_right_chui_2_2,force_right_heng_2_2=dcon_wheel_rail_force_single_deta_time(-yingbian_right_chui_2,
                                           -yingbian_right_heng_2,
                                           sample_rate=sample_rate,
                                           info_biaoding=calibration_factor_right_90
                                           )
    force_right_chui_2_2=-force_right_chui_2_2
    force_right_heng_2_2=-force_right_heng_2_2
    speed_right_2_2=speed[loc_right_chui_2_2]
    mileage_right_2_2=mileage[loc_right_chui_2_2] 

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
#按照片位置分析结果
#180°片            
    res_1_1={}
    res_1_1['速度']=speed_left_1_1
    res_1_1['里程']=mileage_left_1_1
    res_1_1['左轮脱轨系数']=abs(force_left_heng_1_1)/force_left_chui_1_1
    res_1_1['右轮脱轨系数']=abs(force_right_heng_1_1)/force_right_chui_1_1
    res_1_1['轮重减载率']=abs(abs(force_left_chui_1_1)-abs(force_right_chui_1_1))/((force_left_chui_1_1+force_right_chui_1_1)/2) #轮重减载率 
    res_1_1['轮轴横向力']=abs(force_left_heng_1_1-force_right_heng_1_1)
    res_1_1['左轮垂向力']=force_left_chui_1_1
    res_1_1['左轮横向力']=force_left_heng_1_1
    res_1_1['右轮垂向力']=force_right_chui_1_1
    res_1_1['右轮横向力']=force_right_heng_1_1
    res_1_1=pd.DataFrame(res_1_1)
    res_1_1=res_1_1[res_1_1['左轮垂向力']>10]
    res_1_1=res_1_1[res_1_1['右轮垂向力']>10]
     
    plot_wheel_rail_force(res_1_1,dir_gepian,'180')
#0°片 
    res_1_2={}
    res_1_2['速度']=speed_left_1_2
    res_1_2['里程']=mileage_left_1_2
    res_1_2['左轮脱轨系数']=abs(force_left_heng_1_2)/force_left_chui_1_2
    res_1_2['右轮脱轨系数']=abs(force_right_heng_1_2)/force_right_chui_1_2
    res_1_2['轮重减载率']=abs(abs(force_left_chui_1_2)-abs(force_right_chui_1_2))/((force_left_chui_1_2+force_right_chui_1_2)/2) #轮重减载率 
    res_1_2['轮轴横向力']=abs(force_left_heng_1_2-force_right_heng_1_2)
    res_1_2['左轮垂向力']=force_left_chui_1_2
    res_1_2['左轮横向力']=force_left_heng_1_2
    res_1_2['右轮垂向力']=force_right_chui_1_2
    res_1_2['右轮横向力']=force_right_heng_1_2
    res_1_2=pd.DataFrame(res_1_2)
    res_1_2=res_1_2[res_1_2['左轮垂向力']>10]
    res_1_2=res_1_2[res_1_2['右轮垂向力']>10]
     
    plot_wheel_rail_force(res_1_2,dir_gepian,'0')

#270°片            
    res_2_1={}
    res_2_1['速度']=speed_left_2_1
    res_2_1['里程']=mileage_left_2_1
    res_2_1['左轮脱轨系数']=abs(force_left_heng_2_1)/force_left_chui_2_1
    res_2_1['右轮脱轨系数']=abs(force_right_heng_2_1)/force_right_chui_2_1
    res_2_1['轮重减载率']=abs(abs(force_left_chui_2_1)-abs(force_right_chui_2_1))/((force_left_chui_2_1+force_right_chui_2_1)/2) #轮重减载率 
    res_2_1['轮轴横向力']=abs(force_left_heng_2_1-force_right_heng_2_1)
    res_2_1['左轮垂向力']=force_left_chui_2_1
    res_2_1['左轮横向力']=force_left_heng_2_1
    res_2_1['右轮垂向力']=force_right_chui_2_1
    res_2_1['右轮横向力']=force_right_heng_2_1
    res_2_1=pd.DataFrame(res_2_1)
    res_2_1=res_2_1[res_2_1['左轮垂向力']>10]
    res_2_1=res_2_1[res_2_1['右轮垂向力']>10]
     
    plot_wheel_rail_force(res_1_1,dir_gepian,'270')
#90°片 
    res_2_2={}
    res_2_2['速度']=speed_left_2_2
    res_2_2['里程']=mileage_left_2_2
    res_2_2['左轮脱轨系数']=abs(force_left_heng_2_2)/force_left_chui_2_2
    res_2_2['右轮脱轨系数']=abs(force_right_heng_2_2)/force_right_chui_2_2
    res_2_2['轮重减载率']=abs(abs(force_left_chui_2_2)-abs(force_right_chui_2_2))/((force_left_chui_2_2+force_right_chui_2_2)/2) #轮重减载率 
    res_2_2['轮轴横向力']=abs(force_left_heng_2_2-force_right_heng_2_2)
    res_2_2['左轮垂向力']=force_left_chui_2_2
    res_2_2['左轮横向力']=force_left_heng_2_2
    res_2_2['右轮垂向力']=force_right_chui_2_2
    res_2_2['右轮横向力']=force_right_heng_2_2
    res_2_2=pd.DataFrame(res_2_2)
    res_2_2=res_2_2[res_2_2['左轮垂向力']>10]
    res_2_2=res_2_2[res_2_2['右轮垂向力']>10]
     
    plot_wheel_rail_force(res_1_2,dir_gepian,'90')

    with pd.ExcelWriter(dir_gepian+'/各片轮轨力测试结果.xlsx') as writer:
        res_1_1.to_excel(writer, sheet_name='180°')  
        res_1_2.to_excel(writer, sheet_name='0°')  
        res_2_1.to_excel(writer, sheet_name='270°')  
        res_2_2.to_excel(writer, sheet_name='90°') 