from common.webCommon import BasePage,YamlHelper
from selenium import webdriver
import os
class LoginPage(BasePage):
    proDir = os.path.split(os.path.realpath(__file__))[0]  # 绝对路径中当前脚本所在目录
    Path = os.path.join(proDir, "adxWebElement.yaml")
    # LOGIN_SELECTOR = YamlHelper().get_config_dict("/home/wangyf/smoketest/testFile/data/adxWebElement.yaml")["LoginPage"]
    LOGIN_SELECTOR = YamlHelper().get_config_dict(Path)["LoginPage"]

    def login(self, username, password):
        self.base_driver.maximize_window()
        self.base_driver.type(self.LOGIN_SELECTOR["LOGIN_FORM_ACCOUNT_SELECTOR"],username)
        self.base_driver.type(self.LOGIN_SELECTOR["LOGIN_FORM_PASSWORD_SELECTOR"], password)
        self.base_driver.type(self.LOGIN_SELECTOR["LOGIN_FORM_VALIDATECODE_SELECTOR"], '9527')
        self.base_driver.click(self.LOGIN_SELECTOR["LOGIN_FORM_SUBMIT_SELECTOR"])
        self.base_driver.forced_wait(3)