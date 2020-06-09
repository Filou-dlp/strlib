#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

Class for File/Folder edition

"""

__version__ = '0.1'
__author__ = 'Blacknax'

import os
import sys
import shutil


def str2bytes(_txt_):  # Convert a string to bytes string
    """
        Fonction to convert string into byte
    """
    return bytes(_txt_, 'utf-8')


def bytes2str(_txt_):  # Convert a bytes string to string
    """
        Fonction to convert byte into string
    """
    return str(_txt_, 'utf-8')


class TFolder:
    """
        Class for folder edition

        @param FOLDER_PATH is the path of this files or programme
        @type str
    """

    FOLDER_PATH = sys.path[0]
    FOLDER_NAME = ""

    def __init__(self,_path_):
        """
            Constructor
        """
        self.FOLDER_PATH = os.path.join(self.FOLDER_PATH, _path_)
        self.FOLDER_NAME = _path_

    def Create_Multi_Folder(self):
        """
            Function to create all folder path (like Folder/Folder/Folder/...)

            @param _path_ is the path of the created folder
            @type str
        """
        os.makedirs(self.FOLDER_PATH)

    @staticmethod
    def Renam_File_Folder(_old_, _new_):
        """
            Function to rename folder/file

            @param _old_ is the old folder name
            @type str

            @param _new_ is the new folder name
            @type str
        """
        os.rename(_old_, _new_)

    def Move_Folder(self, _path_):
        """
            Function to move folder

            @param _path_ is the path of the moved folder
            @type str
        """
        shutil.move(self.FILE_PATH, _path_)

    def Del_Folder(self):
        """
            Function to delete folder
        """
        shutil.rmtree(self.FOLDER_PATH)

    def Copy_Folder(self, _prefix_="", _suffix_="")
        """
            Function to copy file

            @param _prefix_ prefix could have the file
            @type str

            @param _suffix_ suffix could have the file
            @type str
        """

        new_name = _prefix_ + self.FILE_NAME + _suffix_ + "." + self.FILE_EXT
        shutil.copytree(self.FILE_PATH, new_name)

class TFiles(TFolder):

    """
        Function to file edition

        @param FILE_PATH is the path of the created file
        @type str

        @param FILE_NAME is the name
        @type str

         @param FILE_EXT is the type of file (txt or other for exemple)
        @type str

        @param FILE is the File variable (to write in the file)
        @type str
    """
    FILE_PATH = ""
    FILE_NAME = ""
    FILE_EXT = ""
    FILE = ""

    def __init__(self, _name_, _extention_=0, _path_=0):
        """
            Constructor

            @param _name_ is the name of the file
            @type str

            @param _extention_ is the file type
            @type str

            @param _path_ is the folder path
                if there is folder creation (like folder/file)
            @type str
        """
        if _path_ != 0:
            super(TFiles, self).__init__(_path_)
            self.Create_Multi_Folder()
        if _extention_ == 0:
            self.FILE_NAME = _name_
        else:
            self.FILE_NAME = _name_
            self.FILE_EXT = _extention_
        self.Create_File_Path(self.FOLDER_PATH,
                              self.FILE_NAME + "." + self.FILE_EXT)

    @staticmethod
    def Connect_Name_Ext(_name_, _ext_):
        """
            Fonction to make one variable of name and extention

            @param _name_ name of the file
            @type str

            @param _ext_ extention of the file
            @type str

            @return join of both
            @type str
        """
        return _name_ + "." + _ext_

    def Create_File_Path(self, _folder_, _file_):
        """
            Fonction to create file path

            @param _folder_ name of the folder
            @type str

            @param _file_ name of the file
            @type str
        """
        self.FILE_PATH = os.path.join(_folder_, _file_)

    def Create_File(self):
        """
            Function to create file
        """
        _file = open(self.FILE_PATH, "x")
        _file.close()

    def Copy_File(self, _path_="", _prefix_="", _suffix_=""):
        """
            Function to copy file

            @param _prefix_ prefix could have the file
            @type str

            @param _suffix_ suffix could have the file
            @type str
        """

        new_path_name = _path_ + _prefix_ + self.FILE_NAME + _suffix_
        + "." + self.FILE_EXT
        shutil.copy(self.FILE_PATH, new_path_name)

    def Open_File(self, _writting_):
        """
            Function to open file

            @param _writting_ is the path of the created folder
                r -> READ
                w -> WRITE and erase current
                a -> APPEND
                b -> BINARY
                t -> TEXT
                x -> Create file and open
            @type str
        """
        self.FILE = open(self.FILE_PATH, _writting_)

    def Close_File(self):
        """
            Function to close file
        """
        self.FILE.close()

    def Edit_File(self, _txt_):
        """
            Function to edit file

            @param _txt_ is the
            @type str
        """
        pass

    def Read_File_Str(self, _str=0):
        """
            Function to read file
            And put it in a string

            @return the file content
            @type str
        """
        if _str == 0:
            a = ""
            with self.FILE as fichier:
                a += fichier.read()
        else:
            a = b""
            with self.FILE as fichier:
                a += fichier.read()
        return a

    def Read_File_Array(self):
        """
            Function to read file
            And put it in in an array

            @return the file content
            @type str
        """
        a = []
        with self.FILE as fichier:
            a += fichier.readlines()

        return a

    def Write_File(self, _txt_):
        """
            Function to write string in the file

            @param _txt_ is the text to put inside the file
            @type str
        """
        if _txt_ is None:
            _txt_ = ""

        if isinstance(_txt_, dict):  # convert dict into str
            _txt_ = str(_txt_)

        elif isinstance(_txt_, tuple):  # convert tuple into str
            _txt_ = str(_txt_)

        if isinstance(_txt_, str):  # If txt is a string
            self.FILE.write(_txt_)
        elif isinstance(_txt_, bytes):  # If text if bytes
            self.FILE.write(_txt_)
        else:
            for item in _txt_:
                self.FILE.write("{}\n".format(item))

    def Del_File(self, _path_):
        """
            Function to delete file

            @param _path_ is the path of the deleted folder
            @type str
        """
        os.remove(self.FILE_PATH)


if __name__ == "__main__":

    _TMP = "password"
    _EXT = "txt"
    #T = TFiles(_TMP, _EXT, "Save")
    # T.Create_File()
    # T.Copy_File("","1")

    # shutil.copytree("Save","Save2")
    shutil.rmtree("Save")
    # T.Close_File()
    # T.Del_File("RE\Test.txt")
