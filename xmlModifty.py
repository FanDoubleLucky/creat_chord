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
from midi2locationMap import clefG2Map

tempHLAlterMap = {
        'sharp':1,
        'flat':-1,
        'double-sharp':2,
        'flat-flat':-2,
        'three-quarters-flat':-1.5,
        'quarter-flat':-0.5,
        'quarter-sharp':0.5,
        'three-quarters-sharp':1.5
        }
tempHL = ['sharp','flat','natural',
          'double-sharp','flat-flat',
          'slash-flat','slash-sharp','double-slash-flat',
          'three-quarters-flat','three-quarters-sharp',
          'quarter-flat','quarter-sharp','slash-quarter-sharp',
          'sharp-up','sharp-down',
          'flat-up','flat-down',
          'natural-up','natural-down',
          'sori','koron']

notationsList = ['fermata[type:upright]',
                 'fermata[type:upright]text:angled',
                 'fermata[type:upright]text:square',
                 'articulations_accent',
                 'articulations_staccato',
                 'articulations_staccatissimo',
                 'articulations_tenuto',
                 'articulations_detached-legato',
                 'articulations_strong-accent',#strong-accent type opposite stem direction
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

inverseclefG2Map = {value:key for key,value in clefG2Map.items()}

def add_random_element(file_url):
        
    xmlFile = ET.parse(file_url)
    
    oldRoot = xmlFile.getroot()
    
    clef = 'clefG2-'
    
    #rest
    for measure in oldRoot.iter('measure'):
        for i in range(0,len(measure)):
            if measure[i].tag == 'note' and len(list(measure[i].iter('duration'))) != 0 and len(list(measure[i].iter('dot'))) == 0:
                choice = random.randint(1,20)
                #note to rest 1/20
                if choice <= 2:
                    rest = ET.Element('rest')
                    for child in measure[i].getchildren():
                        if child.tag != 'voice' and child.tag != 'type' and child.tag != 'duration':
                            measure[i].remove(child)
                    measure[i].insert(0,rest)
                    
                    
    #chord articu tempHL    
    for measure in oldRoot.iter('measure'):
        for i in range(0,len(measure)):
            if measure[i].tag == 'note' and len(list(measure[i].iter('rest'))) == 0:
                choice = random.randint(1,10)
                #note add chord 1/10
                if choice <= 1:
                    location = 1
                    for pitch in measure[i].iter('pitch'):
                        locationKey = clef
                        for step in pitch.iter('step'):
                            locationKey = locationKey + step.text
                            break;
                        for octave in pitch.iter('octave'):
                            locationKey = locationKey + octave.text
                            break;
                        location = locationMap[clef + pitch[0].text + pitch[1].text]
                    if location<=11:
                        location = location+ random.randint(1,7)
                    else:
                        location = location- random.randint(1,7)
                        
                    midi = inverseclefG2Map[location].split(clef)[1]
                    newNote = copy.deepcopy(measure[i])
                    chord = ET.Element('chord')
                    newNote.attrib = {}
                    if len(list(newNote.iter('chord'))) == 0:
                        newNote.insert(0,chord)
                    for pitch in newNote.iter('pitch'):
                        pitch[0].text = midi[0]
                        pitch[1].text = midi[1]
                    measure.insert(i+1,newNote)
                elif choice >=2:
                #note add tempHL 3/20
                    choice = random.randint(1,20)
                    if choice <=3:
                        chooseAccident = random.randint(0,len(tempHL)-1)
                        accidentText = tempHL[chooseAccident]
                        if  accidentText in tempHLAlterMap.keys():
                            alterText = tempHLAlterMap[accidentText]
                            alter = ET.Element('alter')
                            alter.text = str(alterText)
                            for pitch in measure[i].iter('pitch'):
                                pitch.insert(1,alter)
                        
                        existedAcc = 0
                        
                        for j in range(0, len(measure[i])):
                            if measure[i][j].tag == 'type':
                                accidental = ET.Element('accidental')
                                accidental.text = accidentText
                                measure[i].insert(j+1,accidental)
                                existedAcc=j+1
                            elif measure[i][j].tag == 'dot': 
                                measure[i].remove(measure[i][existedAcc])
                                accidental = ET.Element('accidental')
                                accidental.text = accidentText
                                measure[i].insert(j,accidental) #insert at j
                                break
                            elif measure[i][j].tag == 'stem':
                                break
                            elif measure[i][len(measure[i])-1].tag == 'dot' and j==len(measure[i])-2: #as insert a new element, len(mea[i]) add 1, so the last location len - 1 becomes len - 2
                                measure[i].remove(measure[i][existedAcc])
                                accidental = ET.Element('accidental')
                                accidental.text = accidentText
                                measure[i].insert(j+1,accidental) # insert at j+1
                                break
                #note add nontations 3/20
                    choice = random.randint(1,20)
                    if choice <= 3 and len(list(measure[i].iter('chord'))) == 0:
                        chooseNotation = random.randint(0,len(notationsList)-1)
                        notationText = notationsList[chooseNotation]
                        if notationText == 'articulations_strong-accent':
                            for stem in measure[i].iter('stem'):
                                notations = ET.Element('notations')
                                articulations = ET.Element('articulations')
                                strong_accent = ET.Element('strong-accent')
                                if stem.text == 'down':
                                    strong_accent.attrib = {'type':'up'}
                                else:
                                    strong_accent.attrib = {'type':'down'}
                                articulations.append(strong_accent)
                                notations.append(articulations)
                                measure[i].append(notations)
                        else:
                            notations = ET.Element('notations')
                            if not('[' in notationText) and not('text:' in notationText):
                                subNote1 = ET.Element(notationText.split('_')[0])
                                subNote2 = ET.Element(notationText.split('_')[1])
                                subNote1.append(subNote2)
                                notations.append(subNote1)
                            elif ('[' in notationText) and not('text:' in notationText):
                                if notationText == 'fermata[type:upright]':
                                    fermata = ET.Element('fermata')
                                    fermata.attrib = {'type':'upright'}
                                    notations.append(fermata)
                                else: #only ornaments_xxx[]
                                    ornaments = ET.Element('ornaments')
                                    ornamentsSubTag = notationText.split('[')[0].split('_')[1]
                                    ornamentsSub = ET.Element(ornamentsSubTag)
                                    ornamentsSubAttribs = notationText.split(']')[0].split('[')[1]
                                    for subAttrib in ornamentsSubAttribs.split(' '):
                                        key,value = subAttrib.split(':')
                                        ornamentsSub.attrib[key] = value
                                    ornaments.append(ornamentsSub)  
                                    notations.append(ornaments)
                            elif 'text:' in notationText:
                                text = notationText.split('text:')[1]
                                fermata = ET.Element('fermata')
                                fermata.attrib = {'type':'upright'}
                                fermata.text = text
                                notations.append(fermata)
                            measure[i].append(notations)
       
                     
    xmlFile.write('articalXML/'+file_url.split('\\')[1])
        
if __name__=="__main__":
    for file in os.listdir('newXML'):
        file = os.path.join('newXML',file)
        try:
            add_random_element(file)
        except Exception as e:
            print(file)
            print(e)