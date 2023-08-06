# -*- coding: utf-8 -*-
"""
Created on Sun Nov 14 14:47:25 2021

@author: Administrator
"""

from ctypes import *

dll_name="DWDataReaderLib64.dll"
dll = windll.LoadLibrary(dll_name)  # 加载链接库

dll.DWInit()
dir_='E:/20200620磁各庄实验室/6科研/平稳性/'
name='北京地铁19号线车辆平稳性测试_2021_09_27_224902.dxd'
dll.DWOpenDataFile(dir_+name)

dll.DWGetChannelListCount()
dll.DWFileInfo()
dll.DWGetChannelListItem()

windll.libfunctions(dll_name)