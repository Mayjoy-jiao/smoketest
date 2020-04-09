from common.webCommon import YamlHelper
from page.adx.main import MainPage
import os
class DeveloperAdsenseManagePage(MainPage):
    proDir = os.path.split(os.path.realpath(__file__))[0]  # 绝对路径中当前脚本所在目录
    Path = os.path.join(proDir, "adxWebElement.yaml")
    DAM_SELECTOR =YamlHelper().get_config_dict(Path)["DeveloperAdsenseManagePage"]

    def search_developer_adsense_id(self,ad_id):
        self.base_driver.type(self.DAM_SELECTOR["DEVELOPER_ADSENSE_MANAGE_SEARCH_ADID_SELECTOR"], ad_id)
        self.base_driver.click(self.DAM_SELECTOR["DEVELOPER_ADSENSE_MANAGE_SEARCH_BUTTON_SELECTOR"])
        self.base_driver.forced_wait(3)

    def checkin_adConfig_page(self):
        self.base_driver.click(self.DAM_SELECTOR["DEVELOPER_ADSENSE_MANAGE_ADCONFIG_NEW_SELECTOR"])
        self.base_driver.forced_wait(3)

    def get_developer_adsense_info(self):
        info = self.base_driver.get_text(self.DAM_SELECTOR["DEVELOPER_ADSENSE_INFO_SELECTOR"])
        print(info)
        info_list = info.split("\n")
        print(info_list)
        return info_list