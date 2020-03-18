#coding=utf-8
from selenium import webdriver
from public.common.log import Log
from public.common.readconfig import ReadConfig

logger=Log()

class Browser:

    def __init__(self,browser):
        self.browser=browser

    def driver(self):

        if self.browser == "firefox" or self.browser == "ff":
            logger.info("正在启动Firefox浏览器")
            driver = webdriver.Firefox()

        elif self.browser == "chrome" or self.browser == "Chrome":
            logger.info("正在启动Chrome浏览器")
            driver = webdriver.Chrome()

        elif self.browser == "internet explorer" or self.browser == "ie":
            logger.info("正在启动IE浏览器")
            driver = webdriver.Ie()

        elif self.browser == "opera":
            logger.info("正在启动opera浏览器")
            driver = webdriver.Opera()

        elif self.browser == "edge":
            logger.info("正在启动Edge浏览器")
            driver = webdriver.Edge()
        else:
            logger.error("Not found %s browser,You can enter 'ie','ff',"
                            "'chrome'"%self.browser)
            driver =webdriver.Chrome()
            #set the default browser

        return driver

#test coding
#t=Browser("../../config/config.conf")
#print(t)
#t.driver()