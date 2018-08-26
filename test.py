# -*- coding: utf-8 -*-
"""
Created on Tue Jul 31 14:54:43 2018

@author: FYZ
"""

import os

if __name__ == "__main__":
    pathDir = os.listdir('artificialPNGs')
    print(pathDir)
    for path_name in pathDir:
        if len(path_name.split('.')) != 1:
            continue
        else:
            print(path_name)
            print(len(path_name.split('.')))
            line_pictures = os.listdir('artificialPNGs/' + path_name)
            for picture_name in line_pictures:
                print(picture_name)
