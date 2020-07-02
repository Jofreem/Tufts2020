#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import schedule
import time
import ctypes
import os
from os import listdir
from os.path import isfile, join
import win32api
import win32gui
import win32con
import random as r


# In[ ]:


class backgroundClass:
    
    def __init__(self, folder):
        self.fileList = []
        self.getImages(folder)
        self.background = None
        self.adjustOn()
        
    def getImages(self, folder):
        for dirpath, dirnames, filenames in os.walk(folder):
            for filename in [f for f in filenames if f.endswith(".JPG") or f.endswith(".png")]:
                self.fileList.append(os.path.join(dirpath, filename))
        
    def adjustOn(self):
        self.background = self.fileList[r.randrange(len(self.fileList))]

    def setBackground(self):
        win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER,self.background,3)
        self.adjustOn()


# In[ ]:


obj = backgroundClass(r"C:\Users\jd_fr\Desktop\Background-Photos")
interval = 3
schedule.every(interval).minutes.do(obj.setBackground)

while 1:
    schedule.run_pending()
    time.sleep(interval)

