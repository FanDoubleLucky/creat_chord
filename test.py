# -*- coding: utf-8 -*-
"""
Created on Tue Jul 31 14:54:43 2018

@author: FYZ
"""

import os

for subdir in os.listdir('articalPNGLines'):
	if len(os.listdir('articalPNGLines/'+subdir)) == 0:
		print(subdir)

print('over')
