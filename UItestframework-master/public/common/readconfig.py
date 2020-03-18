__author__ = 'zz'

import configparser

class ReadConfig:

    def read_config(self,path,section,option):
        cf=configparser.ConfigParser()
        cf.read(path)
        return cf[section][option]

#test coding
#print(ReadConfig().read_config("../../config/config.conf","BROWSER","browser"))