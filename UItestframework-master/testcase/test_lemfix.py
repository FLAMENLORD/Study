#coding=utf-8

from public.common import mytest
from  public.pages.lemfixLoginPage import LemfixLoginPage

class TestLemfixLogin(mytest.MyTest):
    """lemfix测试"""

    def test_login_success(self):
        t=LemfixLoginPage(self.dr)
        t.into_login_page()
        t.type_username("summerliu90")
        t.type_password("huahua90")
        t.click_login_button()
        print(t.return_title())




