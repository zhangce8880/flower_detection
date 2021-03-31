# -*- coding: utf-8 -*-
"""
Created on Mon Dec 17 14:14:52 2018
1.split pic(mask/images)
2.random split pic for train/test

@author: zetn
"""

'''
------------------------1.split to mask/images--------------------
import os
import shutil
path_img='train'
ls = os.listdir(path_img)
print(len(ls))
for i in ls:
    if i.find('mask')!=-1:      #cannot find key words, then return -1,else return the index position
       shutil.move(path_img+'/'+i,"data/train2/images/"+i)
'''

'''
------------------------2.split to train/test(mask&&images)--------------------
#reference: https://blog.csdn.net/kenwengqie2235/article/details/81509714
import os, sys
import random
import shutil
 
 
def copyFile(fileDir):
    pathDir = os.listdir(fileDir)
    sample = random.sample(pathDir, 1226)
    #print(sample)
    for name in sample:
        shutil.move(fileDir+'/' + name, tarDir+'/' + name)
        cor_mask_name = name[0:-7]+'mask.png'
        shutil.move(path_masks+'/' + cor_mask_name, tar_masks+'/' + cor_mask_name)
        #print(cor_mask_name)
 
 
if __name__ == '__main__':
    # open /textiles
    path = "data/flower/train/images/"
    path_masks = "data/flower/train/masks/"
    ls = os.listdir(path)
    print(len(ls))
    tarDir = "data/flower/test/images/"
    tar_masks = "data/flower/test/masks/"
    copyFile(path)
'''

'''
#------------------------3.get 8 Bit test masks--------------------
import os
import cv2

path = "data/flower/train/masks/"
ls = os.listdir(path)
#i = 0

for name in ls:
    img = cv2.imread(os.path.join(path, name))
    img1 = img[:, :, 0]
    #cv2.imwrite("data/flower/train/mask8/%d.png"%i, img1)
    cv2.imwrite("data/flower/train/mask8/%s"%name, img1)
    #i = i+1


'''
#------------------------4.metrics of pre and GT--------------------
import os
import cv2
import numpy as np
import skimage.io as io

#path1 = "data/flower/test/sub_test/mask_8bit"
path1 = "data/flower/test/sub_test/mask8" #Dir of Ground Truth
#path1 = "data/test/mask_8bit"
#path2 = "data/test/sub_test/predict1"
path2 = "data/flower/test/sub_test/predict" #Dir of predict map
#path2 = "data/flower/train/predict"
sample1 = os.listdir(path1)
Iou = []#Iou for each test images
TP = 0
FP = 0
FN = 0
sum_fenmu = 0
for name in sample1:
    mask1 = io.imread(os.path.join(path1, name))
    mask1 = mask1 / 255
    mask1 = mask1.flatten()
    
    #name1 = name[0:-8]+'sat.jpg'
    #mask2 = io.imread(os.path.join(path2, name1))
    mask2 = io.imread(os.path.join(path2, name))
    mask2 = mask2 / 255.0
    mask2[mask2 >= 0.5] = 1
    mask2[mask2 < 0.5] = 0
    mask2 = mask2.flatten()
    
    tp = np.dot(mask1, mask2)
    TP = TP + tp
    fp = mask2.sum()-tp
    FP = FP + fp
    fn = mask1.sum()-tp
    FN = FN + fn
    #fenmu = mask1.sum()+mask2.sum()-tp
    fenmu = mask1.sum()+mask2.sum()-tp
    sum_fenmu = sum_fenmu + fenmu
    #element_wise = np.multiply(mask1, mask2)
    Iou.append(tp / fenmu)
    #if(tp / fenmu == 0.0):
        #print(name)
    
print(Iou)
print(TP / sum_fenmu)#active IoU
print(TP / (TP+FN))#recall
print(TP / (TP+FP))#precision 
