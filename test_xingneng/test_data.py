from selenium import webdriver



class TestData1:
    def test_data(self):
        driver = webdriver.Chrome("/Users/ww/Downloads/chromedriver")
        driver.get("https://www.baidu.com")
        # 执行js脚本
        print(driver.execute_script("return JSON.stringify(window.performance.timing)"))