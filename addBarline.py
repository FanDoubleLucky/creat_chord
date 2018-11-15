# -*- coding: utf-8 -*-
"""
Created on Sun Jul 15 19:20:07 2018

@author: FYZ
"""

import xml.etree.ElementTree as ET
import random
import copy
import os
from midi2locationMap import locationMap
from midi2locationMap import clefG2Map,inverseMap

tempHLAlterMap = {
    'sharp': 1,
    'flat': -1,
    'double-sharp': 2,
    'flat-flat': -2,
    'three-quarters-flat': -1.5,
    'quarter-flat': -0.5,
    'quarter-sharp': 0.5,
    'three-quarters-sharp': 1.5
}
tempHL = ['sharp', 'flat', 'natural',
          'double-sharp', 'flat-flat',
          'slash-flat', 'slash-sharp', 'double-slash-flat',
          'three-quarters-flat', 'three-quarters-sharp',
          'quarter-flat', 'quarter-sharp', 'slash-quarter-sharp',
          'sharp-up', 'sharp-down',
          'flat-up', 'flat-down',
          'natural-up', 'natural-down',
          'sori', 'koron']

notationsList = ['fermata[type:upright]',
                 'fermata[type:upright]text:angled',
                 'fermata[type:upright]text:square',
                 'articulations_accent',
                 'articulations_staccato',
                 'articulations_staccatissimo',
                 'articulations_tenuto',
                 'articulations_detached-legato',
                 'articulations_strong-accent',  # strong-accent type opposite stem direction
                 'technical_open-string',
                 'technical_stopped',
                 'technical_up-bow',
                 'technical_down-bow',
                 'technical_snap-pizzicato',
                 'ornaments_inverted-turn',
                 'ornaments_turn',
                 'ornaments_trill-mark',
                 'ornaments_inverted-mordent',
                 'ornaments_mordent',
                 'ornaments_inverted-mordent[long:yes]',
                 'ornaments_mordent[long:yes]',
                 'ornaments_inverted-mordent[long:yes approach:below]',
                 'ornaments_inverted-mordent[long:yes approach:above]',
                 'ornaments_mordent[long:yes approach:below]',
                 'ornaments_mordent[long:yes approach:above]',
                 'ornaments_inverted-mordent[long:yes departure:below]',
                 'ornaments_inverted-mordent[long:yes departure:above]',
                 'ornaments_schleifer']

clef_list = ['clefG2',
'clefG21',
'clefG22',
'clefG2-1',
'clefG1',
'clefC1',
'clefC2',
'clefC3',
'clefC4',
'clefC5',
'clefF4',
'clefF41',
'clefF42',
'clefF4-1',
'clefF4-2',
'clefF3',
'clefF5']


barline_list = [
'bar:dashed',
'bar:dotted',
'bar:light-heavy',
'bar:heavy-light_forward',
'bar:light-heavy_backward']

#inverseclefG2Map = {value: key for key, value in locationMap.items()}

#the output of addClef_keyLSlur.py is a musicxml. Transfer the musicxml to mscz and then tranfer back to musicxml.
#the final musicxml file is the input of this program.
def add_random_element(file_url):
    xml_file = ET.parse(file_url)

    old_root = xml_file.getroot()

    
    
    for measure in old_root.iter('measure'):
        add_YN = random.randint(1, 2)
        #only the measure without barline is added new barline. In input musicxml, every line have a light-light barline and a key symbol at line end.
        #but the key symbol in line end isn't signed in musicxml. so I must use the light-light barline to locate the key symbol not signed.
        #and in the input musicxml, if the measure contains a barline tag, the barline must be light-light. so 'len(list(measure.iter('barline')))==0' protects the light-light barline from covered.
        if add_YN == 1 and len(list(measure.iter('barline'))) == 0:
            barline_choice = random.randint(0, len(barline_list)-1)
            barline_info = barline_list[barline_choice]
            if barline_info == 'bar:heavy-light_forward':
                barline_create = ET.Element('barline')
                barline_create.attrib = {'location': 'left'}
                bar_style_create = ET.Element('bar-style')
                bar_style_create.text = 'heavy-light'
                repeat_create = ET.Element('repeat')
                repeat_create.attrib = {'direction': 'forward'}
                barline_create.insert(0,bar_style_create)
                barline_create.insert(1,repeat_create)
                measure.insert(0,barline_create)
            elif barline_info == 'bar:light-heavy_backward':
                barline_create = ET.Element('barline')
                barline_create.attrib = {'location': 'right'}
                bar_style_create = ET.Element('bar-style')
                bar_style_create.text = 'light-heavy'
                repeat_create = ET.Element('repeat')
                repeat_create.attrib = {'direction': 'backward'}
                barline_create.insert(0,bar_style_create)
                barline_create.insert(1,repeat_create)
                measure.insert(len(measure),barline_create)
            else:
                barline_create = ET.Element('barline')
                barline_create.attrib = {'location': 'right'}
                bar_style_create = ET.Element('bar-style')
                bar_style_create.text = barline_info.split(':')[1]
                barline_create.insert(0,bar_style_create)
                measure.insert(len(measure),barline_create)
               
    
    #only add light-light barline at head measure, it can avoid this light-light barline to mislead locating the line end light-light barline
    for measure in old_root.iter('measure'):
        if len(list(measure.iter('print'))) != 0 and len(list(measure.iter('barline'))) == 0:
            barline_create = ET.Element('barline')
            barline_create.attrib = {'location': 'right'}
            bar_style_create = ET.Element('bar-style')
            bar_style_create.text = 'light-light'
            barline_create.insert(0,bar_style_create)
            barline_create.insert(1,repeat_create)
            measure.insert(len(measure),barline_create)
            
    xml_file.write('appendbarlineXML\\' + file_url.split('\\')[1])

if __name__ == "__main__":
    #add_random_element('testPNGs\\819.musicxml')
     
    for file in os.listdir('testPNGs'):
        file = os.path.join('testPNGs', file)
        try:
            add_random_element(file)
        except Exception as e:
            print(file)
            print('error')
            print(e)
     