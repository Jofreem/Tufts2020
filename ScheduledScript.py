#!/usr/bin/env python
# coding: utf-8

# In[1]:


import schedule
import time
import ctypes
from os import listdir
from os.path import isfile, join
import win32api
import win32gui
import win32con


# In[ ]:


class backgroundClass:
    
    def __init__(self, folder):
        self.fileList = [f for f in listdir(folder) if isfile(join(folder, f))]
        self.filePath = folder
        self.on = 0
        self.background = None
        self.adjustOn()
        
    def adjustOn(self):
        self.background = self.filePath + "\\" + self.fileList[self.on]
        self.on += 1
        if(self.on == len(self.fileList)):
            self.on = 0
    
    def setBackground(self):
        win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER,self.background,3)
        self.adjustOn()


# In[ ]:


obj = backgroundClass(r"C:\Users\jd_fr\Desktop\Background-Photos\Backgrounds")
schedule.every(3).minutes.do(obj.setBackground)

while 1:
    schedule.run_pending()
    time.sleep(1)

