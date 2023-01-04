'''
封装关于page的基本的方法
 对元素进行查找
'''
import yaml
from appium.webdriver.webdriver import WebDriver


class BasePage():
    # 声明的 实列变量 子类就可以使用
    _driver: WebDriver

    def __init__(self, driver: WebDriver = None):
        self._driver = driver

    # 寻找元素  locator 定位的方式 id 还是class ， value：是具体的参数
    def find(self, locator, value):
        return self._driver.find_element(locator, value)

    # 解析 yaml的文件
    def steps(self, path):
        with open(path) as f :
            steps = yaml.safe_load(f)
        for step in steps:
            # 找到这个元素
            if "by" in step.keys():
                element = self.find(step["by"], step["locator"])

            # 具体执行那些操作【click，send_keys 等】
            if "action" in step.keys():
                action = step["action"]
                if action == "click":
                    element.click()