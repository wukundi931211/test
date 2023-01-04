'''
启动app等的初始方法
'''
import yaml
from appium import webdriver
from appium_po.page.base_page import BasePage
from appium_po.page.main import Main


class App(BasePage):
    # 声明的 实列变量 子类就可以使用
    _package = 'com.xueqiu.android'
    _activity = '.view.WelcomeActivityAlias'



    def start(self):


        if self._driver is None:
            cap = dict()
            cap["platformVersion"] = "11"
            cap["deviceName"] = yaml.safe_load(open("../parameter/config/configuration.yaml "))['caps']['udid']
            cap["noReset"] = True
            cap["resetKeyBoard"] = True
            cap["platformName"] = "Android"
            cap["unicodeKeyBoard"] = True
            cap["autoAcceptAlerts"] = True
            cap["appPackage"] = self._package
            cap["appActivity"] = self._activity
            # 初始化
            self._driver = webdriver.Remote(
                "http://127.0.0.1:4723/wd/hub",
                cap
            )
        else:
            self._driver.start_activity(self._package, self._activity)
        #继承了basepage 之前声明的
        self._driver.implicitly_wait(3)
        return self

    def main(self) -> Main:
        return Main(self._driver)
