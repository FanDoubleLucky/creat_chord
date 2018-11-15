# -*- coding: utf-8 -*-
"""
Created on Tue Jul 10 15:05:35 2018

@author: FYZ
"""

import cv2
import os
import numpy as np
import random



def addSaltNoise(image, percetage):
    G_Noiseimg = image
    num = int(percetage*image.shape[0]*image.shape[1])
    for i in range(num):
        temx = np.random.random_integers(0,image.shape[0]-1)
        temy = np.random.random_integers(0,image.shape[1]-1)
        if np.random.random_integers(0,4)==0:
            G_Noiseimg[temx,temy] = 0
        else:
            G_Noiseimg[temx,temy] = 255
        
    return G_Noiseimg
    
    
def blurNoise(img):
    kernel_size = (5, 5)
    sigma = 100;
    return cv2.GaussianBlur(img, kernel_size, sigma)
    
def rotate(img):
    rows, cols, ch = img.shape
    pts1 = np.float32([[0,0],[cols-1,0],[0,rows-1]])
    direct = random.randint(0,1)
    if direct == 0:
        pts2 = np.float32([[cols*0.01, 0],[cols*0.98,rows*0.1],[cols*0.04,rows*0.9]])
    else:
        pts2 = np.float32([[cols*0.04, 0],[cols*0.98,rows*0.1],[cols*0.01,rows*0.9]])
    M = cv2.getAffineTransform(pts1,pts2)
    dst = cv2.warpAffine(img, M, (cols,rows), borderValue=(255, 255, 255))
    return dst
    
    
root = 'chord/measures/'
rootDir = os.listdir(root)    

for subDir in rootDir:
    pngLine = root+subDir
    pngDir = os.listdir(pngLine)
    
    
    newFolderName = 'chord/measures_N/'+subDir
        
    isExists = os.path.exists(newFolderName)
    if not isExists:
        os.makedirs(newFolderName)
            
            
    for imgName in pngDir:
        img = cv2.imread(root+subDir+'/'+imgName)
        [x, y, z] = img.shape #x:~268 y:2480
        newImage = cv2.resize(img,(int(y/2),int(x/2)),cv2.INTER_LINEAR)
        aff = rotate(newImage)
        blur = blurNoise(newImage)
        salt = addSaltNoise(newImage, 0.1)
        cv2.imwrite(newFolderName+'/'+imgName.split('.')[0]+'_N_aff.png', aff)
        cv2.imwrite(newFolderName+'/'+imgName.split('.')[0]+'_N_blur.png', blur)
        cv2.imwrite(newFolderName+'/'+imgName.split('.')[0]+'_N_salt.png', salt)
'''    
imgName = "000101098-1_1_2.png";
img = cv2.imread(imgName)
newImage = cv2.resize(img,(1024,128),cv2.INTER_LINEAR)
aff = rotate(newImage)
blur = blurNoise(newImage)
salt = addSaltNoise(newImage, 0.1)

cv2.imwrite('aff.png', aff)
cv2.imwrite('blur.png', blur)
cv2.imwrite('salt.png', salt)
''' 
