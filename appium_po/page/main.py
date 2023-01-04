from appium_po.page.base_page import BasePage


class Main(BasePage):

    def goto_search(self):
        #self.find(By.ID, 'home_search').click()
        self.steps("../parameter/main.yaml")