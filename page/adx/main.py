from common.webCommon import YamlHelper
from page.adx.login import LoginPage
import os

class MainPage(LoginPage):
    proDir = os.path.split(os.path.realpath(__file__))[0]  # 绝对路径中当前脚本所在目录
    Path = os.path.join(proDir, "adxWebElement.yaml")
    MAIN_SELECTOR = YamlHelper().get_config_dict(Path)["MainPage"]

    def local_developer_manage_menu(self,menu):
        if menu == "developer_manage":
            menu_selector = self.MAIN_SELECTOR["MAIN_LEFTMENU_DEVELOPER_MANAGE_SELECTOR"] % 1
        elif menu == "developer_app_manage":
            menu_selector = self.MAIN_SELECTOR["MAIN_LEFTMENU_DEVELOPER_MANAGE_SELECTOR"] % 2
        elif menu == "developer_adsense_manage":
            menu_selector = self.MAIN_SELECTOR["MAIN_LEFTMENU_DEVELOPER_MANAGE_SELECTOR"] % 3
        elif menu == "developer_adsense_plan":
            menu_selector = self.MAIN_SELECTOR["MAIN_LEFTMENU_DEVELOPER_MANAGE_SELECTOR"] % 4
        else:
            menu_selector = "error menu"
        return menu_selector

    def checkin_developer_manage_menuPage(self, menu):
        self.base_driver.click(self.local_developer_manage_menu(menu))
        self.base_driver.forced_wait(3)
