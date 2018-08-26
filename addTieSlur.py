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

inverseclefG2Map = {value: key for key, value in clefG2Map.items()}


def add_random_element(file_url):
    xml_file = ET.parse(file_url)

    old_root = xml_file.getroot()

    clef = 'clefG2-'

    # rest
    for measure in old_root.iter('measure'):
        for i in range(0, len(measure)):
            if measure[i].tag == 'note' and len(list(measure[i].iter('duration'))) != 0 and len(
                    list(measure[i].iter('dot'))) == 0:
                choice = random.randint(1, 20)
                # note to rest 1/20
                if choice <= 2:
                    rest = ET.Element('rest')
                    for child in measure[i].getchildren():
                        if child.tag != 'voice' and child.tag != 'type' and child.tag != 'duration':
                            measure[i].remove(child)
                    measure[i].insert(0, rest)

    # chord articu tempHL
    for measure in old_root.iter('measure'):
        for i in range(0, len(measure)):
            if measure[i].tag == 'note' and len(list(measure[i].iter('rest'))) == 0:
                choice = random.randint(1, 10)
                # note add chord 1/10
                if choice <= 1:
                    location = 1
                    for pitch in measure[i].iter('pitch'):
                        location_key = clef
                        for step in pitch.iter('step'):
                            location_key = location_key + step.text
                            break
                        for octave in pitch.iter('octave'):
                            location_key = location_key + octave.text
                            break
                        # location = locationMap[clef + pitch[0].text + pitch[1].text]
                        location = locationMap[location_key]
                    if location <= 11:
                        location = location + random.randint(1, 7)
                    else:
                        location = location - random.randint(1, 7)

                    midi = inverseclefG2Map[location].split(clef)[1]
                    new_note = copy.deepcopy(measure[i])
                    chord = ET.Element('chord')
                    new_note.attrib = {}
                    if len(list(new_note.iter('chord'))) == 0:
                        new_note.insert(0, chord)
                    for pitch in new_note.iter('pitch'):
                        pitch[0].text = midi[0]
                        pitch[1].text = midi[1]
                    measure.insert(i + 1, new_note)
                elif choice >= 2:
                    # note add tempHL 3/20
                    choice = random.randint(1, 20)
                    if choice <= 3:
                        choose_accident = random.randint(0, len(tempHL) - 1)
                        accident_text = tempHL[choose_accident]
                        if accident_text in tempHLAlterMap.keys():
                            alter_text = tempHLAlterMap[accident_text]
                            alter = ET.Element('alter')
                            alter.text = str(alter_text)
                            for pitch in measure[i].iter('pitch'):
                                pitch.insert(1, alter)

                        existed_acc = 0

                        for j in range(0, len(measure[i])):
                            if measure[i][j].tag == 'type':
                                accidental = ET.Element('accidental')
                                accidental.text = accident_text
                                measure[i].insert(j + 1, accidental)
                                existed_acc = j + 1
                            elif measure[i][j].tag == 'dot':
                                measure[i].remove(measure[i][existed_acc])
                                accidental = ET.Element('accidental')
                                accidental.text = accident_text
                                measure[i].insert(j, accidental)  # insert at j
                                break
                            elif measure[i][j].tag == 'stem':
                                break
                            elif measure[i][len(measure[i]) - 1].tag == 'dot' and j == len(measure[
                                                                                               i]) - 2:  # as insert
                                # a new element, len(mea[i]) add 1, so the last location len - 1 becomes len - 2
                                measure[i].remove(measure[i][existed_acc])
                                accidental = ET.Element('accidental')
                                accidental.text = accident_text
                                measure[i].insert(j + 1, accidental)  # insert at j+1
                                break
                    # note add nontations 3/20
                    choice = random.randint(1, 20)
                    if choice <= 3 and len(list(measure[i].iter('chord'))) == 0:
                        choose_notation = random.randint(0, len(notationsList) - 1)
                        notation_text = notationsList[choose_notation]
                        if notation_text == 'articulations_strong-accent':
                            for stem in measure[i].iter('stem'):
                                notations = ET.Element('notations')
                                articulations = ET.Element('articulations')
                                strong_accent = ET.Element('strong-accent')
                                if stem.text == 'down':
                                    strong_accent.attrib = {'type': 'up'}
                                else:
                                    strong_accent.attrib = {'type': 'down'}
                                articulations.append(strong_accent)
                                notations.append(articulations)
                                measure[i].append(notations)
                        else:
                            notations = ET.Element('notations')
                            if not ('[' in notation_text) and not ('text:' in notation_text):
                                sub_note1 = ET.Element(notation_text.split('_')[0])
                                sub_note2 = ET.Element(notation_text.split('_')[1])
                                sub_note1.append(sub_note2)
                                notations.append(sub_note1)
                            elif ('[' in notation_text) and not ('text:' in notation_text):
                                if notation_text == 'fermata[type:upright]':
                                    fermata = ET.Element('fermata')
                                    fermata.attrib = {'type': 'upright'}
                                    notations.append(fermata)
                                else:  # only ornaments_xxx[]
                                    ornaments = ET.Element('ornaments')
                                    ornaments_sub_tag = notation_text.split('[')[0].split('_')[1]
                                    ornaments_sub = ET.Element(ornaments_sub_tag)
                                    ornaments_sub_attribs = notation_text.split(']')[0].split('[')[1]
                                    for subAttrib in ornaments_sub_attribs.split(' '):
                                        key, value = subAttrib.split(':')
                                        ornaments_sub.attrib[key] = value
                                    ornaments.append(ornaments_sub)
                                    notations.append(ornaments)
                            elif 'text:' in notation_text:
                                text = notation_text.split('text:')[1]
                                fermata = ET.Element('fermata')
                                fermata.attrib = {'type': 'upright'}
                                fermata.text = text
                                notations.append(fermata)
                            measure[i].append(notations)

    # tie
    note_list = list(old_root.iter('note'))
    for i in range(0, len(note_list)):
        choice = random.randint(1, 15)
        if choice <= 1 and len(list(note_list[i].iter('notations'))) == 0 and len(list(note_list[i].iter('alter'))) == 0: # 1/20
            j = i + 1
            while j in range(i + 1, i + 10) and j < len(note_list)-1:
                if len(list(note_list[j].iter('notations'))) == 0:
                    pitch_info_i = ''
                    for pitch_i in note_list[i].iter('pitch'):
                        for step in pitch_i.iter('step'):
                            pitch_info_i = pitch_info_i + step.text
                            break
                        for octave in pitch_i.iter('octave'):
                            pitch_info_i = pitch_info_i + octave.text
                            break
                    pitch_info_j = ''
                    for pitch_j in note_list[j].iter('pitch'):
                        for step in pitch_j.iter('step'):
                            pitch_info_j = pitch_info_j + step.text
                            break
                        for octave in pitch_j.iter('octave'):
                            pitch_info_j = pitch_info_j + octave.text
                            break

                    if pitch_info_i == pitch_info_j:
                        notations_i = ET.Element('notations')
                        tie_i = ET.Element('tied')
                        tie_i.attrib = {'type': 'start'}
                        notations_i.append(tie_i)
                        note_list[i].append(notations_i)
                        notations_j = ET.Element('notations')
                        tie_j = ET.Element('tied')
                        tie_j.attrib = {'type': 'stop'}
                        notations_j.append(tie_j)
                        note_list[j].append(notations_j)
                        break
                j+=1;
    xml_file.write('artificialXML/' + file_url.split('/')[1])


if __name__ == "__main__":
    add_random_element('newXML/score (1).musicxml')
    '''
    for file in os.listdir('newXML'):
        file = os.path.join('newXML', file)
        try:
            add_random_element(file)
        except Exception as e:
            print(file)
            print(e)
    '''
