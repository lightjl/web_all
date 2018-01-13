#!usr/bin/env
# -*-coding:utf-8 -*-
import os
import codecs
from common.sendMail import recMail
import logging


logging.basicConfig(level=logging.CRITICAL, format='%(asctime)s - %(levelname)s -%(message)s')

class saveToFile():
    def __init__(self, fold):
        self.__subFolderPath = "/saveFile/" + fold + "/"
        self.sub_folder = os.path.join(os.getcwd(), self.__subFolderPath)
        if not os.path.exists(self.sub_folder):
            os.mkdir(self.sub_folder)

    def save(self, filename, text, size = 4):
        self.__filename = self.sub_folder + filename + ".txt"
        #print(self.__filename)
        f = codecs.open(self.__filename, "w", "utf-8")
        f.write(text)
        f.close()
        fileSizeKb = os.path.getsize(self.__filename)/1024
        if ( fileSizeKb >= size):
            logging.debug(self.__filename + 'size(Kb): ' + str(fileSizeKb))
            return True
        return False
        
    def getSubfolder(self):
        return self.__subFolderPath

    def isDownloaded(self, filename):
        filename2 = self.sub_folder + filename + ".txt"
        #print(filename2)
        return os.path.isfile(self.sub_folder + filename + ".txt")  # 如果不存在就返回False
        pass

    def isSended(self, filename):
        return recMail.checkMail(filename, 7)  #7 days

