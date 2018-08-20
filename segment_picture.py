# -*- coding: utf-8 -*-
"""
Created on Wed May 30 20:34:36 2018

@author: FYZ
"""
import os
from PIL import Image
import numpy as np
import cv2

            
def segmentLine(dirName,fileName,newFolderName):
    img = Image.open('./'+dirName+'/'+fileName)
    #img = Image.open(fileName)
    x,y = img.size
    BG = Image.new('RGB',img.size,(255,255,255))
    BG.paste(img,(0,0,x,y),img)
    
    grayImage = cv2.cvtColor(np.array(BG),cv2.COLOR_BGR2GRAY)
    ret,binaryImage = cv2.threshold(grayImage,240,255,cv2.THRESH_BINARY)
    
    
    image_height, image_width = binaryImage.shape
    staff_lines = []
    line_found = 0
    
    line_len = []
    for row in range(0,image_height):
        line_len.append(np.sum(binaryImage[row,:]))
        
    max_len = min(line_len)    
    
    
    for row in range(0,image_height):
            white_pixel = 0
            white_pixel = np.sum(binaryImage[row,:])
            if white_pixel<=max_len*1.25:
                if line_found ==0:
                    staff_lines.append(row)
                line_found = 1
            else:
                line_found =0
    
    staff_lines = np.reshape(staff_lines,(int(len(staff_lines)/5),5))
    line_height =0
    staff_num, staffLine_num = staff_lines.shape
    
    for column in range(0,staffLine_num-1):
        column_diff = staff_lines[:, column + 1] - staff_lines[:, column];
        current_line_height = max(column_diff);
        if current_line_height>line_height:
            line_height = current_line_height
            
            
    
    for i in range(0,staff_num):
        if i ==0:
            min_y = staff_lines[0,0] - 4*line_height
            if min_y<0:
                min_y=0
        else:
            min_y = int((staff_lines[i,0]+staff_lines[i-1,staffLine_num-1])/2);
        
    
        if i == staff_num-1:
            max_y = staff_lines[staff_num-1, staffLine_num-1] + 4*line_height
            if max_y>image_height-1:
                max_y = image_height-1
        else:
            max_y = int((staff_lines[i,staffLine_num-1] + staff_lines[i+1,0])/2);
            
        #each_line = binaryImage[min_y:max_y,:]
        each_line = grayImage[min_y:max_y,:]
        
        
        isExists = os.path.exists(newFolderName)
        if not isExists:
            os.makedirs(newFolderName)
            
            
        imageName ='./'+newFolderName+'/'+fileName.split('-')[0]+'_score_'+str(page)+'-'+str(i)+'.jpg'
        cv2.imwrite(imageName,each_line)
    
    
    
if __name__=='__main__':
	dirName = 'testPNG'#which folder name
	error_file = open('SegmentErrorsegment.txt','w+')
	print('open')
	pathDir = os.listdir(dirName)
	print('started')
	for fileName in pathDir:
	    if len(fileName.split('.')) == 1:
		continue;
	    try:
		page = fileName.split('.')[0].split('-')[1]#101-09.png
		newFolderName = 'articalPNGLines' + '/'+ fileName.split('-')[0]+'_score_'+str(page)
		
		isExists = os.path.exists(newFolderName)
		if not isExists:
		    os.makedirs(newFolderName)
		    
		segmentLine(dirName,fileName,newFolderName)
		
	    except:
		error_file.write(fileName)
		error_file.write('\n')
	    
	print('over')
	error_file.close()  
	'''
	fileName = '1027676-37.png'
	page = fileName.split('.')[0].split('-')[1]
	newFolderName = dirName + '/'+ fileName.split('-')[0]+'_score_'+str(page)
	segmentLine(dirName,fileName,newFolderName)
	'''


	#segmentLine('errorExtractPNG','423106_c459552944_score_6.png','supplementLines') 
