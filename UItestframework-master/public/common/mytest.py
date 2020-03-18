#coding=utf-8

import unittest
from public.common.log import Log
from public.common.driver import Browser
from public.common.readconfig import ReadConfig

class MyTest(unittest.TestCase):
    """
    The base class is for all testcase.
    """
    def setUp(self):
        self.logger = Log()
        self.logger.info('############################### START ###############################')
        browser=ReadConfig().read_config("./config/config.conf","BROWSER","browser")
        self.dr=Browser(browser).driver()
        self.dr.maximize_window()

    def tearDown(self):
        self.dr.quit()
        self.logger.info('###############################  End  ###############################')
