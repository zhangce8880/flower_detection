# -*- coding: utf-8 -*-
"""
Created on Wed Jan 19 19:12:15 2021

@author: Ce Zhang
"""

# -*- coding:utf8 -*-

import os

class BatchRename():
    '''
    batch rename the picture file name

    '''
    def __init__(self):
        self.path = 'data/flower/test/images'  #the file needs to rename

    def rename(self):
        filelist = os.listdir(self.path) 
        total_num = len(filelist) 
        i = 0  
        for item in filelist:
            if item.endswith('.jpg'):  
                src = os.path.join(os.path.abspath(self.path), item)
                dst = os.path.join(os.path.abspath(self.path), ''+str(i) + '.jpg')
                try:
                    os.rename(src, dst)
                    print ('converting %s to %s ...' % (src, dst))
                    i = i + 1
                except:
                    continue
        print ('total %d to rename & converted %d jpgs' % (total_num, i))

if __name__ == '__main__':
    demo = BatchRename()
    demo.rename()
