#!usr/bin/env
# -*-coding:utf-8 -*-
import os
import codecs
import logging
from pathlib import Path




class saveToFile():
    def __init__(self, fold):
        self.__savePath = Path("./saveTmpFile/")
        self.__savePath.mkdir(exist_ok=True)
        

    def save(self, filename, text, size = 4):
        self.__filename = filename + ".txt"
        #print(self.__filename)
        self.__file = self.__savePath.joinpath(self.__filename)
        self.__file.write_text(text, encoding='utf-8')

        fileSizeKb = self.__file.stat().st_size/1024
        if ( fileSizeKb >= size):
            logging.debug(self.__filename + 'size(Kb): ' + str(fileSizeKb))
            return True
        return False
        
    def getSavePath(self):
        return self.__savePath


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s -%(message)s')
    test = saveToFile('xs')
    test.save('text', "text", 4)
else:
    from common.sendMail import recMail
    logging.basicConfig(level=logging.CRITICAL, format='%(asctime)s - %(levelname)s -%(message)s')