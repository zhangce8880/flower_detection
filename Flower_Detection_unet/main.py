# -*- coding: utf-8 -*-
"""
Created on Fri March 11 12:12:34 2021
Drone for Flower Detection
@author: Ce Zhang
"""
from model import unet, segnet_vgg16, fcn_vgg16_8s, fcn_2s, VGGUnet2, res_unet1, D_resunet, D_resunet1
from data import trainGenerator, testGenerator, saveResult, testGenerator2
from keras.callbacks import ModelCheckpoint, Callback, EarlyStopping, ReduceLROnPlateau, TensorBoard
import keras.backend as K
import os, cv2
import numpy as np
import skimage.io as io
import skimage.transform as trans

#fileDir = "data/flower/test/images"

#test_image_num = len(os.listdir(fileDir))
        

data_gen_args = dict(rotation_range = 90.,
                    #width_shift_range=0.1,
                    #height_shift_range=0.1,
                    #shear_range=0.1,
                    #zoom_range=0.1,
                    fill_mode = 'nearest',
                    #horizontal_flip = True,
                    #vertical_flip = True
					)

train_Gene = trainGenerator(8,'data/flower/train','image_crops','mask_crops',data_gen_args,save_to_dir = None)
val_Gene = trainGenerator(8,'data/flower/test','images_crops','masks_crops',data_gen_args)

reduce_lr = ReduceLROnPlateau(monitor = 'val_loss', factor=0.2, patience=3, verbose=0, mode='min', epsilon=1e-4, 
                              cooldown=0, min_lr=1e-6)
visual = TensorBoard(log_dir='./unet_log', histogram_freq=0, write_graph=True, write_images=True)
earlystop = EarlyStopping(monitor='val_loss', patience=7, verbose=0, mode='min')
model = unet()
#model = segnet_vgg16()
#model = fcn_vgg16_8s()
#model.load_weights('fcn_vgg16_8s.hdf5')
#model = fcn_vgg16_8s()
#model = VGGUnet2()
#model = D_resunet()
#model = fcn_2s()
#model = res_unet1()
#model.load_weights('res_unet.hdf5')

model_checkpoint = ModelCheckpoint('unet.hdf5', monitor='val_loss',verbose=1, save_best_only=True)
model.fit_generator(train_Gene,steps_per_epoch=500,epochs=30,
                    callbacks=[model_checkpoint, visual, reduce_lr, earlystop], 
                    validation_data=val_Gene, validation_steps=20)#step_per_epoch and validation_steps equals to number of samples divide batchsize


'''
test_samples = os.listdir(fileDir)
#num_image = len(test_samples)
for name in test_samples:
    img = cv2.imread(os.path.join(fileDir,name))
    img = img / 255.0
    #img = np.array([img])
    img = trans.resize(img,(512,512))
    img = np.reshape(img,(1,)+img.shape)
    mask = model.predict(img)
    mask[mask > 0.5] = 1
    mask[mask <= 0.5] = 0
    mask = mask * 255
    print (mask.shape)
    cv2.imwrite("data/flower/train/predict/%d.png"%i, mask[0,:,:,:])
    i = i+1



testGene = testGenerator2(fileDir)
results = model.predict_generator(testGene, test_image_num, verbose=1)

#print(results)
for i,item in enumerate(results):
    #print(i)
    item[item >= 0.5] = 1
    item[item < 0.5] = 0
    mask = item * 255
    #print(mask[200:210,200:210,0])
    cv2.imwrite("data/flower/test/fcn_finetune/%d.png"%i, mask)
#saveResult("data/flower/train/predict", results)
'''  
