# -*- coding: utf-8 -*-
"""
Created on Wed May 30 20:34:36 2018

@author: FYZ
"""
import os
from PIL import Image
import numpy as np
import cv2
import xml.etree.ElementTree as ET


def segment_measure(dirName, fileName, newFolderName):
    file_id = fileName.split('_')[0]
    img = cv2.imread(dirName + '/' + fileName)
    [x, y, z] = img.shape #x:~268 y:2480
    xml_file = ET.parse('testXML/' + file_id + '.musicxml')
    #xml_file = ET.parse(dirName+'/1000.musicxml')
    root = xml_file.getroot()
    
    for page_layout in root.iter('page-layout'):
        for page_width_tag in page_layout.iter('page-width'):
            page_width = page_width_tag.text
        for left_margin_tag in page_layout.iter('left-margin'):
            left_margin = left_margin_tag.text
            
    ratio = y/float(page_width)
    measure_location = []     
    
    for measure in root.iter('measure'):
        measure_num = int(measure.attrib['number'])
        
        if len(list(measure.iter('print'))) !=0:
            loc = ratio * (float(left_margin) + float(measure.attrib['width']))
            measure_location.append(int(loc))
        else:
            loc = measure_location[measure_num-1-1]+ ratio * float(measure.attrib['width'])
            measure_location.append(int(loc))


    s_e_measure = []
    page_measure = []
    startMeasure = -1
    endMeasure = -1
    # catch symbol-measure
    for measure in root.iter("measure"):
        measure_num = int(measure.attrib['number'])


        # segment line and page
        for printLabel in measure.iter('print'):
            endMeasure = measure_num - 1
            if startMeasure >= 0:
                s_e_measure.append([startMeasure, endMeasure])
            startMeasure = measure_num
            for (key, value) in printLabel.attrib.items():
                # if (key == 'new-system' or key == 'new-page' ) and value == 'yes':
                if key == 'new-page' and value == 'yes':
                    page_measure.append(s_e_measure)
                    s_e_measure = []

                break
            break

    s_e_measure.append([startMeasure, -1])
    page_measure.append(s_e_measure)
    
    
    
    page_number = int(fileName.split('score_')[1].split('-')[0])
    line_number = int(fileName.split('.')[0].split('-')[1])
    [startMeasure, endMeasure] = page_measure[page_number-1][line_number]
    
    for measure in root.iter("measure"):
        measure_num = int(measure.attrib['number'])
        if (measure_num >= startMeasure) and (measure_num <= endMeasure or endMeasure == -1):
            if measure_num ==1 or measure_location[measure_num-1-1]>measure_location[measure_num-1] or len(list(measure.iter('print'))) !=0:
                startCol = 0
            else:
                startCol = measure_location[measure_num-1-1]
            endCol = measure_location[measure_num-1]
            each_measure= img[:,startCol:endCol+10]
            cv2.imwrite(newFolderName+'/'+fileName.split('.')[0]+'-'+str(measure_num)+'.jpg', each_measure)
    #imageName = './' + newFolderName + '/' + fileName.split('-')[0] + '_score_' + str(page) + '-' + str(i) + '.jpg'
    #cv2.imwrite(imageName, each_line)


if __name__ == '__main__':
    
    dirName = 'testPNGs'  # which folder name
    newFolderName = 'segMea'
    #fileName='1000_score_01-0.jpg'
    #segment_measure(dirName, fileName, newFolderName)
    error_file = open('SegmentErrorsegment.txt', 'w+')
    
    linesDir = os.listdir(dirName)
    for linesDir_name in linesDir:
        if len(linesDir_name.split('.')) != 1:
                continue
        else:
            try:
                newFolderName = 'segMea/' +linesDir_name
    
                isExists = os.path.exists(newFolderName)
                if not isExists:
                    os.makedirs(newFolderName)
                linesDir = os.listdir(dirName+'/'+linesDir_name)
                
                
                for png_name in linesDir:
                    segment_measure(dirName+'/'+linesDir_name, png_name, newFolderName)
    
            except Exception as e:
                print('error')
                print(e)
                
    print('over')
    error_file.close()
            
        
    

    
