# -*- coding: utf-8 -*-
"""
Created on Wed May 30 20:34:36 2018

@author: FYZ
"""
import os
from PIL import Image
import numpy as np
import cv2
import random


def random_location_resize(self):
    image = Image.open('7.png')
    BG_w = 1024
    BG_h = 128
    
    
    
    
    x,y = image.size
    w_ratio = random.uniform(0.9,1.08)
    h_ratio = random.uniform(0.85,1.25)
    image = image.resize((int(x*0.38*w_ratio),int(y*0.38*h_ratio)),Image.ANTIALIAS)
    BG = Image.new('RGBA', (BG_w,BG_h), (255, 255, 255))
    x,y = image.size
    r,g,b,a = image.split()
    
    start_x = random.randint(0,BG_w-x)
    start_y = random.randint(0,BG_h-y)
    
    # img = cv2.cvtColor(np.asarray(image),cv2.COLOR_RGB2BGR)
           
    # image = Image.fromarray(cv2.cvtColor(img,cv2.COLOR_BGR2RGB))          
                       
    BG.paste(image, (start_x, start_y, start_x+x, start_y+y), a)
    BG.save('11.png')
    
    
    
    
def segment_line(dirName, fileName, newFolderName):
    BG_w = 1024
    BG_h = 128
    img = Image.open('./' + dirName + '/' + fileName)

    # img = Image.open(fileName)
    x, y = img.size
    BG = Image.new('RGB', img.size, (255, 255, 255))
    BG.paste(img, (0, 0, x, y), img)
    img.close()
    grayImage = cv2.cvtColor(np.array(BG), cv2.COLOR_BGR2GRAY)
    ret, binaryImage = cv2.threshold(grayImage, 240, 255, cv2.THRESH_BINARY)

    image_height, image_width = binaryImage.shape
    staff_lines = []
    line_found = 0

    line_len = []
    for row in range(0, image_height):
        line_len.append(np.sum(binaryImage[row, :]))

    max_len = min(line_len)

    for row in range(0, image_height):
        white_pixel = 0
        white_pixel = np.sum(binaryImage[row, :])
        if white_pixel <= max_len * 1.25:
            if line_found == 0:
                staff_lines.append(row)
            line_found = 1
        else:
            line_found = 0

    staff_lines = np.reshape(staff_lines, (int(len(staff_lines) / 5), 5))
    line_height = 0
    staff_num, staffLine_num = staff_lines.shape

    for column in range(0, staffLine_num - 1):
        column_diff = staff_lines[:, column + 1] - staff_lines[:, column];
        current_line_height = max(column_diff);
        if current_line_height > line_height:
            line_height = current_line_height

    img = Image.open('./' + dirName + '/' + fileName)
    bg_photo_list = os.listdir('BGWEB')
    bg_id = random.randint(1, len(bg_photo_list))
    bg_real = Image.open('BGWEB/'+str(bg_id)+'.jpg')
    
    x, y = img.size # x, y is the size of one whole page PNG
    bg_real = bg_real.resize((BG_w, y))
    
    
    for i in range(0, staff_num):
        if i == 0:
            min_y = staff_lines[0, 0] - 4 * line_height
            if min_y < 0:
                min_y = 0
        else:
            min_y = int((staff_lines[i, 0] + staff_lines[i - 1, staffLine_num - 1]) / 2);

        if i == staff_num - 1:
            max_y = staff_lines[staff_num - 1, staffLine_num - 1] + 4 * line_height
            if max_y > image_height - 1:
                max_y = image_height - 1
        else:
            max_y = int((staff_lines[i, staffLine_num - 1] + staff_lines[i + 1, 0]) / 2);

        # get one line png from one whole page PNG 
        each_line = img.crop(
                (
                    0,
                    min_y,
                    x,
                    max_y
                )
        )
        
        # one line png resize in random
        
        x_each_line, y_each_line = each_line.size
        w_ratio = random.uniform(0.9,1.08)
        h_ratio = random.uniform(0.85,1.2)
        if y_each_line <280:
            each_line = each_line.resize((int(x_each_line*0.38*w_ratio),int(y_each_line*0.38*h_ratio)),Image.ANTIALIAS)
        else:
            h_ratio = random.uniform(0.9,1)
            each_line = each_line.resize((int(x_each_line*0.38*w_ratio),int(BG_h*h_ratio)),Image.ANTIALIAS)
        
        
        x_each_line, y_each_line = each_line.size
        
        
        
        # get one line BG from one whole page BG by choosing a random location
        loc = random.randint(1, y - BG_h - 1)
        bg_one_line = np.array(bg_real)
        bg_one_line = bg_one_line[loc:loc + BG_h, :]
        bg_one_line = Image.fromarray(bg_one_line)
        rotate = random.randint(1, 2)
        if rotate == 1:
            bg_one_line = bg_one_line.transpose(Image.FLIP_LEFT_RIGHT)
        else:
            bg_one_line = bg_one_line.transpose(Image.FLIP_TOP_BOTTOM)
            
        # paste each_line and bg_line
        R, G, B, A = each_line.split()
        start_x = random.randint(0,BG_w-x_each_line)
        start_y = random.randint(0,BG_h-y_each_line)
        bg_one_line.paste(each_line, (start_x, start_y, start_x+x_each_line, start_y+y_each_line), A)
        
        is_exists = os.path.exists(newFolderName)
        if not is_exists:
            os.makedirs(newFolderName)

        image_name = './' + newFolderName + '/' + fileName.split('-')[0] + '_score_' + str(page) + '-' + str(i) + '.jpg'
        bg_one_line.save(image_name)
        
    img.close()
    bg_real.close()

if __name__ == '__main__':
    dirName = 'artificial_whole_PNG'  # which folder name
    pathDir = os.listdir(dirName)
    print('started')
    for fileName in pathDir:
        if len(fileName.split('.')) == 1:
            continue
        #try:
        page = fileName.split('.')[0].split('-')[1]  # 101-09.png
        #newFolderName = 'artificial_whole_PNG_with_realBG' + '/' + fileName.split('-')[0] + '_score_' + str(page)
        newFolderName = 'artificial_and_append_lines_photo_with_BGWEB_Random_Resize1024*128' + '/' + fileName.split('-')[0] + '_score_' + str(page)
        isExists = os.path.exists(newFolderName)
        if not isExists:
            os.makedirs(newFolderName)

        segment_line(dirName, fileName, newFolderName)

        #except:
            #error_file.write(fileName)
            #error_file.write('\n')

    #print('over')
    #error_file.close()
    
