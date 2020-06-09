#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

Class for File/Folder edition

"""

__version__ = '0.1'
__author__ = 'Alexandre FAIA'
__date__ = '11/05/2020'


import json

from TFile_folder import TFiles

class TJson:
    
    def __init__(self, val=False, name, extention=0, path=0):
        """
            Constructor
        """
        self.__files = TFiles(name, extention, path)
        
        
        self.__path = path
        if  not(val):
            self.__data = json.dumps(val)
            
    
    def __read_file(self):
        """
        
        """
        
        self.__files.Open_File("r")
        self.__file_val = self.__files.Read_File_Str()
    
    def get_str(self):
        """
        
        """
        tmp_ = json.loads(self.__file_val)2
