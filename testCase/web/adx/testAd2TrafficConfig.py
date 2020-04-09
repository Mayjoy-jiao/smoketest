from page.adx.DAM_AdCfg_TrafficCfg import DAM_AdCfg_TrafficCfg
from common.webCommon import BoxDriver
import unittest


class AdConfig(unittest.TestCase):

    def setUp(self):
        self.base_driver = BoxDriver()
        self.base_driver.navigate("http://192.168.0.245:8585/login#configPubAppAdNew")
        self.base_driver.implicitly_wait(10)
        self.base_driver.forced_wait(3)
        self.ad2trafficconfig = DAM_AdCfg_TrafficCfg(self.base_driver)
        self.ad2trafficconfig.login("sunyaping", "sunyaping")
        self.ad2trafficconfig.checkin_developer_manage_menuPage("developer_adsense_manage")
        self.ad2trafficconfig.search_developer_adsense_id("rsjnyljl")  # 广告位:测试-SYP-横幅
        self.ad2trafficconfig.checkin_adConfig_page()
        self.ad2trafficconfig.enter_frame()
        # self.ad2trafficconfig.checkin_ad2trafficconfig_page()

    def test_adsense_and_dsp_info(self):
        """验证广告配置(新)2级页面,页面顶部展示的广告位及DSP广告源信息"""
        print("\n*****验证广告配置(新)2级页面,页面顶部展示的广告位及DSP广告源信息*****\n")

        print("获取广告配置(新)1级页面顶部展示的广告位信息")
        adconfig_info_list = self.ad2trafficconfig.get_adconfig_adsense_info()
        self.base_driver.forced_wait(1)
        print("筛选出指定的DSP应用")
        self.ad2trafficconfig.select_dsp_app("DSP应用-SYP")
        print("遍历列表,获取该DSP广告源的信息")
        dsp_info_list = self.ad2trafficconfig.get_dsp_info()
        switch_attribute = self.ad2trafficconfig.get_switch_attribute()
        dsp_info_list.extend(switch_attribute)
        self.base_driver.forced_wait(1)
        adconfig_info_list[0].extend(dsp_info_list)
        print("广告位及DSP广告源信息:\n%s" % adconfig_info_list)

        print("进入广告配置(新)2级页面")
        self.ad2trafficconfig.checkin_ad2trafficconfig_page()

        print("获取广告配置(新)2级页面顶部展示的广告位及DSP广告源信息")
        ad2trafficconfig_info_list = self.ad2trafficconfig.get_ad2trafficconfig_info()
        self.base_driver.forced_wait(1)

        self.assertEqual(adconfig_info_list[0], ad2trafficconfig_info_list[0])

    def test_save(self):
        """验证广告配置(新)2级页面二级预下发量配置保存是否成功"""
        print("\n*****验证广告配置(新)2级页面二级预下发量配置保存是否成功*****\n")

        print("广告配置(新)页面,指定DSP应用,进入2级页面")
        self.ad2trafficconfig.checkin_ad2trafficconfig_page_withdspapp("DSP应用-SYP")

        print("进行二级预下发量分时段的配置")
        # 设置竞价价格(eCPM), 一级展示上限, 一级预估点击率, 二级预下发量占比, 有效时间段
        expected_value_list = ['6', '1000', '60', '30']
        self.ad2trafficconfig.set_ad2trafficconfig_item(expected_value_list)

        # [竞价价格(eCPM), 一级展示上限, 一级预估点击率, 二级预下发量占比, 有效时间段]
        expected_value_list.extend(['01:00 - 02:00'])
        print("设置值为: %s" % expected_value_list)

        print("点击保存")
        self.ad2trafficconfig.click_save_btn()
        print("点击刷新")
        self.ad2trafficconfig.click_save_btn()

        print("获取配置项,验证是否与所设一致")
        current_value_list = self.ad2trafficconfig.get_ad2trafficconfig_rows1_text()
        print("当前值为: %s" % current_value_list)

        self.assertEqual(expected_value_list, current_value_list)

    def test_reset(self):
        """验证广告配置(新)2级页面二级预下发量配置重置是否成功"""
        print("\n*****验证广告配置(新)2级页面二级预下发量配置重置是否成功*****\n")

        print("广告配置(新)页面,指定DSP应用,进入2级页面")
        self.ad2trafficconfig.checkin_ad2trafficconfig_page_withdspapp("DSP应用-SYP")

        print("判断该广告位二级预下发量配置是否为空")
        is_ad2trafficconfig_empty = self.ad2trafficconfig.is_ad2trafficconfig_empty()
        if is_ad2trafficconfig_empty:
            print("该广告位二级预下发量配置不为空")
        else:
            print("该广告位二级预下发量配置为空")
            print("进行二级预下发量分时段的配置")
            # 设置竞价价格(eCPM), 一级展示上限, 一级预估点击率, 二级预下发量占比, 有效时间段(设置为01:00 - 02:00)
            expected_value_list = ['8', '8000', '80', '20']
            self.ad2trafficconfig.set_ad2trafficconfig_item(expected_value_list)
            print("点击保存")
            self.ad2trafficconfig.click_save_btn()

        print("点击重置并确认")
        self.ad2trafficconfig.click_reset_btn()
        print("点击保存")
        self.ad2trafficconfig.click_save_btn()

        print("重置后,验证二级预下发量配置是否为空")
        is_ad2trafficconfig_empty = self.ad2trafficconfig.is_ad2trafficconfig_empty()
        self.assertTrue(is_ad2trafficconfig_empty)

    def test_batch_add(self):
        """验证广告配置(新)2级页面批量新增二级预下发量配置"""
        print("\n*****验证广告配置(新)2级页面批量新增二级预下发量配置*****\n")

        print("广告配置(新)页面,指定DSP应用,进入2级页面")
        self.ad2trafficconfig.checkin_ad2trafficconfig_page_withdspapp("DSP应用-SYP")

        print("点击重置并确认")
        self.ad2trafficconfig.click_reset_btn()
        print("点击保存")
        self.ad2trafficconfig.click_save_btn()

        print("点击批量新增")
        self.ad2trafficconfig.click_batch_add_btn()

        print("验证新增了24行")
        rownum = self.ad2trafficconfig.get_row_num()
        self.assertEqual(rownum, 24)

        print("验证有效时间段为从00:00开始,1小时为1个时间段")
        current_time_texts_list = self.ad2trafficconfig.get_time_texts()
        expected_time_texts_list = ['00:00 - 01:00', '01:00 - 02:00', '02:00 - 03:00', '03:00 - 04:00', '04:00 - 05:00',
                                    '05:00 - 06:00', '06:00 - 07:00', '07:00 - 08:00', '08:00 - 09:00', '09:00 - 10:00',
                                    '10:00 - 11:00', '11:00 - 12:00', '12:00 - 13:00', '13:00 - 14:00', '14:00 - 15:00',
                                    '15:00 - 16:00', '16:00 - 17:00', '17:00 - 18:00', '18:00 - 19:00', '19:00 - 20:00',
                                    '20:00 - 21:00', '21:00 - 22:00', '22:00 - 23:00', '23:00 - 00:00']
        self.assertEqual(current_time_texts_list, expected_time_texts_list)

        print("验证其余输入框都为0")
        current_input_texts_list = self.ad2trafficconfig.get_ad2trafficconfig_rows24_text()
        for i, value in enumerate(current_input_texts_list):
            self.assertEqual(int(value), 0)

    def test_batch_modify(self):
        """验证广告配置(新)2级页面批量修改"""
        print("\n*****验证广告配置(新)2级页面批量修改*****\n")

        print("广告配置(新)页面,指定DSP应用,进入2级页面")
        self.ad2trafficconfig.checkin_ad2trafficconfig_page_withdspapp("DSP应用-SYP")

        print("点击重置并确认")
        self.ad2trafficconfig.click_reset_btn()
        print("点击保存")
        self.ad2trafficconfig.click_save_btn()
        print("点击批量新增")
        self.ad2trafficconfig.click_batch_add_btn()

        print("设置批量修改项: 竞价价格(ECPM),一级展示量上限,一级预估点击率,二级预下发量占比")
        self.ad2trafficconfig.set_batch_modify_item(['6.6', '6666', '66', '20'])
        print("开启批量修改每一项的开关")
        self.ad2trafficconfig.turn_on_batch_modify_switch()
        print("点击保存")
        self.ad2trafficconfig.click_save_btn()

    def tearDown(self):
        self.base_driver.quit()


