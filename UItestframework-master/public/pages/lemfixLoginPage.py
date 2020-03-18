#coding=utf-8

from public.common.basepage import BasePage

class LemfixLoginPage(BasePage):

    def into_login_page(self):
        """打开lemfix登录页面"""
        self.open('http://www.lemfix.com:3030/signin')

    def type_username(self,name):
        """输入登录用户名"""
        self.type('id->name',name)

    def type_password(self,password):
        """输入登密码"""
        self.type('id->pass',password)

    def click_login_button(self):
        self.click('class->span-primary')

    def return_title(self):
        """返回该页面的title"""
        return self.get_title()