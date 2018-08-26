# -*- coding: utf-8 -*-
"""
Created on Sun Jun  3 02:12:39 2018

@author: FYZ
"""

from xml.etree import ElementTree as ET
from midi2locationMap import locationMap
from articalLabel import label_list
import numpy as np
import pandas as pd
import os, shutil


def analyze_tag(note):
    if len(note) == 0:
        return note.tag, note.text
    else:
        for i in range(0, len(note)):
            print(note.tag, analyze_tag(note[i]))


tag_list = ['measure', 'measure-attributes-time', 'measure-note', 'measure-note-pitch', 'measure-note-duration',
            'measure-note-stem', 'measure-note-duration', 'measure-note-rest']


def extract_info(fileName):
    # 101_score_01-0.jpg
    print('fileName', fileName)
    file_id = fileName.split('_')[0]
    xml_file = ET.parse('artificialXML/' + file_id + '.musicxml')
    page_number = int(fileName.split('score_')[1].split('-')[0])
    line_number = int(fileName.split('.')[0].split('-')[1])
    s_e_measure = []
    page_measure = []
    startMeasure = -1
    endMeasure = -1
    clefs = []
    key_fifth = []
    times = []

    measure_num = 1
    root = xml_file.getroot()

    # catch symbol-measure
    for measure in root.iter("measure"):
        measure_num = int(measure.attrib['number'])
        # clef catch
        for clefLabel in measure.iter('clef'):
            clefInfo = ''
            for i in range(0, len(clefLabel)):
                clefInfo = clefInfo + clefLabel[i].text
            clefs.append([measure_num, clefInfo])

        # key-fifths catch
        for keyLabel in measure.iter('fifths'):
            key_fifth.append([measure_num, 'key' + keyLabel.text])

        # time-type catch
        for timeLabel in measure.iter('time'):
            time_info = timeLabel[0].text + '/' + timeLabel[1].text
            if time_info == '4/4' or time_info == '2/2':
                if len(timeLabel.attrib) == 1:
                    time_info = timeLabel.attrib['symbol'] + time_info

            times.append([measure_num, time_info])

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

    # analyze
    print(page_number,line_number)
    [startMeasure, endMeasure] = page_measure[page_number-1][line_number]
    everyline_label = []
    line_head = 1
    # measure_width = 1
    # first_measureNum = 1
    # first_measureNum_flag = 1
    for measure in root.iter("measure"):
        clef_of_this_mea = ''
        measure_num = int(measure.attrib['number'])

        if (measure_num >= startMeasure) and (measure_num <= endMeasure or endMeasure == -1):

            for i in range(0, len(clefs)):
                [clef_measure, clef_info] = clefs[i]
                if measure_num >= clef_measure and (i + 1 == len(clefs) or measure_num < clefs[i + 1][0]):
                    clef_of_this_mea = 'clef' + clef_info
                    if measure_num == clef_measure or line_head == 1:
                        everyline_label.append('clef' + clef_info)
                        everyline_label.append('break')  # add one break

            if line_head == 1:
                for i in range(0, len(key_fifth)):
                    [key_fifth_measure, key_fifth_info] = key_fifth[i]
                    if measure_num >= key_fifth_measure and (
                            i + 1 == len(key_fifth) or measure_num < key_fifth[i + 1][0]):
                        if measure_num == key_fifth_measure or line_head == 1:
                            everyline_label.append(key_fifth_info)
                            everyline_label.append('break')  # add one break

                head_barline = 0
                for barline in measure.iter('barline'):
                    if barline.attrib['location'] == 'left':
                        head_barline = 1
                        barline_info = 'bar:'
                        for bar_style in barline.iter('bar-style'):
                            barline_info = barline_info + bar_style.text
                        for repeat in barline.iter('repeat'):
                            barline_info = barline_info + '_' + repeat.attrib['direction']
                        everyline_label.append(barline_info)
                        everyline_label.append('break')  # add one break

                if head_barline == 1:
                    try:
                        everyline_label.remove('bar:line-end')
                    except:
                        pass

                else:
                    try:
                        everyline_label[everyline_label.index('bar:line-end')] = 'bar:line'
                    except:
                        pass

            else:
                head_barline = 0
                for barline in measure.iter('barline'):
                    if barline.attrib['location'] == 'left':
                        head_barline = 1
                        barline_info = 'bar:'
                        for bar_style in barline.iter('bar-style'):
                            barline_info = barline_info + bar_style.text
                        for repeat in barline.iter('repeat'):
                            barline_info = barline_info + '_' + repeat.attrib['direction']
                        everyline_label.append(barline_info)
                        everyline_label.append('break')  # add one break

                if head_barline == 1:
                    try:
                        everyline_label.remove('bar:line-end')
                    except:
                        pass

                else:
                    try:
                        everyline_label[everyline_label.index('bar:line-end')] = 'bar:line'
                    except:
                        pass

                for i in range(0, len(key_fifth)):
                    [key_fifth_measure, key_fifth_info] = key_fifth[i]
                    if measure_num >= key_fifth_measure and (
                            i + 1 == len(key_fifth) or measure_num < key_fifth[i + 1][0]):
                        if measure_num == key_fifth_measure or line_head == 1:
                            everyline_label.append(key_fifth_info)
                            everyline_label.append('break')  # add one break

            for i in range(0, len(times)):
                [time_measure, time_info] = times[i]
                if measure_num == time_measure:
                    everyline_label.append(time_info)
                    everyline_label.append('break')  # add one break

            for note in measure.iter('note'):

                if len(list(note.iter('chord'))) == 0:
                    if everyline_label[len(everyline_label) - 1] != 'break':
                        everyline_label.append('break')  # add one break

                for notations in note.iter('notations'):
                    for tied in notations.iter('tied'):
                        tied_info = tied.attrib['type']
                        if tied_info == 'stop':
                            everyline_label.append('tied'+tied_info)

                for notations in note.iter('notations'):
                    for tied in notations.iter('slur'):
                        tied_info = tied.attrib['type']
                        if tied_info == 'stop':
                            everyline_label.append('slur'+tied_info)

                fermata_info = ''
                articulations_info = ''
                technical_info = ''
                ornaments_info = ''
                notations_info = ''
                for notations in note.iter('notations'):
                    try:
                        for fermata in notations.iter('fermata'):
                            fermata_info = 'fermata.' + str(fermata.text)

                        for articulations in notations.iter('articulations'):
                            articulations_info = 'articulations-' + str(articulations[0].tag)
                            for (key, value) in articulations[0].attrib.items():
                                articulations_info = articulations_info + str((key, value))

                        for technical in notations.iter('technical'):
                            technical_info = 'technical-' + str(technical[0].tag)
                            for (key, value) in technical[0].attrib.items():
                                technical_info = technical_info + str((key, value))

                        for ornaments in notations.iter('ornaments'):
                            ornaments_info = 'ornaments-' + str(ornaments[0].tag)
                            for (key, value) in ornaments[0].attrib.items():
                                ornaments_info = ornaments_info + str((key, value))

                        if fermata_info != '':
                            notations_info = notations_info + fermata_info
                            everyline_label.append(notations_info)
                        if articulations_info != '':
                            notations_info = notations_info + articulations_info
                            everyline_label.append(notations_info)
                        if technical_info != '':
                            notations_info = notations_info + technical_info
                            everyline_label.append(notations_info)
                        if ornaments_info != '':
                            print ornaments_info
                            notations_info = notations_info + ornaments_info
                            everyline_label.append(notations_info)
                    except:
                        pass

                rest_time = 'whole'
                rest_info = ''

                for rest in note.iter('rest'):
                    for rest_type in note.iter('type'):
                        rest_time = rest_type.text
                    rest_info = 'rest-' + rest_time
                    everyline_label.append(rest_info)

                pitch_time = 'whole'
                pitch_midi = ''
                accidental_info = ''
                for accidental in note.iter('accidental'):
                    accidental_info = accidental.text
                    everyline_label.append(accidental_info)
                for pitch in note.iter('pitch'):
                    for step in pitch.iter('step'):
                        step_info = step.text
                    for octave in pitch.iter('octave'):
                        octave_info = octave.text
                    pitch_midi = step_info + octave_info
                    for pitch_type in note.iter('type'):
                        pitch_time = pitch_type.text

                    if locationMap.__contains__(clef_of_this_mea + '-' + pitch_midi):
                        everyline_label.append(pitch_time + str(locationMap[clef_of_this_mea + '-' + pitch_midi]))

                for dot in note.iter('dot'):
                    everyline_label.append('dot')

                for notations in note.iter('notations'):
                    for tied in notations.iter('tied'):
                        tied_info = tied.attrib['type']
                        if tied_info == 'start':
                            everyline_label.append('tied'+tied_info)

                for notations in note.iter('notations'):
                    for tied in notations.iter('slur'):
                        tied_info = tied.attrib['type']
                        if tied_info == 'start':
                            everyline_label.append('slur'+tied_info)

            special_bar = 0
            for barline in measure.iter('barline'):
                if barline.attrib['location'] == 'right':
                    special_bar = 1
                    barline_info = 'bar:'
                    for bar_style in barline.iter('bar-style'):
                        barline_info = barline_info + bar_style.text
                    for repeat in barline.iter('repeat'):
                        barline_info = barline_info + '_' + repeat.attrib['direction']
                    everyline_label.append(barline_info)
                    everyline_label.append('break')

            if special_bar == 0:
                everyline_label.append('bar:line-end')
                everyline_label.append('break')
            line_head = 0

    '''  
    start = s_e_measure[0][0]
    end = s_e_measure[0][1]
    i=0
    for measure in root.iter("measure"):
        for (key,value) in measure.attrib.items():
            if key == 'number':
                number = value
            if key == 'width':
                width = value
        if int(number) >= start and (int(number)  <= end or end ==-1):
            
            for note in measure.iter('note'):
                j=1
        if int(number)  == end:
            i=i+1
            start = s_e_measure[i][0]
            end = s_e_measure[i][1]
          
    print(clefs)
    print(key_fifth)
    print(times)
    print(page_measure)
    '''
    labels = np.zeros((len(everyline_label), 256))
    i = 0
    for oneSymbol in everyline_label:
        if label_list.__contains__(oneSymbol):
            labels[i][label_list.index(oneSymbol)] = 1

        i = i + 1

    df = pd.DataFrame(labels, columns=label_list)
    df.to_csv('artificialLabels/' + fileName + '.csv', index=False, header=True)
    return everyline_label
    # return page_measure, clefs
    '''
        if measure[0].tag ==  'print':
            print('measure[i][0]',measure[0].tag)
        for i in range(0,len(measure)):
            print('measure.tag',measure[i].tag)
            for time in  measure[i].iter('time'):#measure-attributes-time
                print('measure time', measure.attrib, time[0].text, time[1].text)
                
       
        for note in measure.iter("note"):#measure-note
                #for i in range(0,len(note)):
            analyze_tag(note)
    '''
    # tag_info.append(measure[i].text)
    # measure.tag measure.attrib
    # print(i,'measure',measure[i].attrib)
    # print('pitch',tag_info)

'''
if __name__ == "__main__":
    pathDir = os.listdir('artificialPNGs')
    errorExtract = open('errorExtract.txt', 'w')
    for path_name in pathDir:
        if len(path_name.split('.')) != 1:
            continue
        else:
            # try:
            error_file = ''
            line_pictures = os.listdir('artificialPNGs/' + path_name)
            for picture_name in line_pictures:
                error_file = picture_name
                everyline_label = extract_info(picture_name)
                # pass
            # except Exception as e:
            # errorExtract.write(error_file+' '+str(e.args))
            # errorExtract.write('\n')
    errorExtract.close()
'''
extract_info('score (1)_score_01-0.jpg')
# page_measure, clefs= extract_info('1185866_8bac7d2bef_score_0-0.jpg','train/1185866.xml')
