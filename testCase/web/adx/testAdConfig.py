from page.adx.DeveloperAdsenseManage_AdConfig import DeveloperAdsenseManage_AdConfigPage
import unittest
from common.webCommon import BoxDriver


class AdConfig(unittest.TestCase):
    def setUp(self):
        self.base_driver = BoxDriver()
        self.base_driver.navigate("http://192.168.0.245:8585/login#configPubAppAdNew")
        self.base_driver.implicitly_wait(10)
        self.base_driver.forced_wait(3)
        self.adconfig = DeveloperAdsenseManage_AdConfigPage(self.base_driver)
        self.adconfig.login("wangyufen","Wangyufen0527")
        self.adconfig.checkin_developer_manage_menuPage("developer_adsense_manage")
        self.adconfig.search_developer_adsense_id("tikv1jna")
        # self.infro = self.adconfig.get_developer_adsense_info()
        self.adconfig.checkin_adConfig_page()
        self.adconfig.enter_frame()
        self.base_driver.forced_wait(3)

    def tearDown(self):
        self.base_driver.close_browser()

    def test_assert_developName(self):
        developName = self.adconfig.get_title_bar_text("developerName").split(": ")[1]
        self.assertEqual("自动化测试", developName)

    def test_assert_developerApp(self):
        developerApp = self.adconfig.get_title_bar_text("developerApp").split(": ")[1]
        self.assertEqual("自动化测试", developerApp)

    def test_assert_adsenseName(self):
        adsenseName = self.adconfig.get_title_bar_text("adsenseName").split(": ")[1]
        self.assertEqual("test广告位_wang", adsenseName)

    def test_assert_adsenseType(self):
        adsenseType = self.adconfig.get_title_bar_text("adsenseType").split(": ")[1]
        self.assertEqual("横幅", adsenseType)

    def test_assert_DSPType(self):
        DSPType = self.adconfig.get_title_bar_text("DSPType").split(": ")[1]
        self.assertEqual("s2s, 爱告c2s", DSPType)

    def test_assert_requestNum_istext(self):
        requestNum_attr = self.adconfig.get_requestNum_attribute()
        self.assertEqual("text", requestNum_attr)

    def test_assert_biddingRate_istext(self):
        biddingRate_attr = self.adconfig.get_biddingRate_attribute()
        self.assertEqual("text", biddingRate_attr)

    def test_assert_testAD(self):
        test_ad = self.adconfig.get_test_advertisement()
        print(test_ad)

    def test_assert_save_resquestNumAndBiddingRate(self):
        """
        测试请求数与竞价比例的保存功能
        """
        data = list(self.adconfig.save_requestNum_bidding(6,70))
        print(data)
        self.assertListEqual([6, 70.0], data)

    def test_assert_serch_dsp(self):
        s = self.adconfig.search_dsp()
        for i in s["record"]:
            self.assertEqual(s["search_dsp_text"], i)

    def test_assert_serch_dsp_app(self):
        s = self.adconfig.search_dsp_app()
        for i in s["record"]:
            self.assertEqual(s["search_dsp_text"], i)

    def test_assert_serch_dsp_type(self):
        s = self.adconfig.search_dsp_type()
        for i in s["record"]:
            self.assertEqual(s["search_dsp_text"], i)

    def test_assert_serch_dsp_isFullTime(self):
        s = self.adconfig.search_is_fullTime()
        for i in s["record"]:
            self.assertEqual(s["search_dsp_text"], i)

    def test_offOn_button(self):
        result = self.adconfig.open_dsp_app()
        self.assertEqual("true", result)