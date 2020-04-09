"""
ADX后台 - [开发者管理] - [开发者广告位管理] - [开发者管理] - 广告配置(新) - 二级预下发量配置页面


Author: Sun Yaping
date: 2019-08-02

"""

# -*- coding: utf-8 -*-

from common.webCommon import YamlHelper
from page.adx.DeveloperAdsenseManage_AdConfig import DeveloperAdsenseManage_AdConfigPage
import os


class DAM_AdCfg_TrafficCfg(DeveloperAdsenseManage_AdConfigPage):
    proDir = os.path.split(os.path.realpath(__file__))[0]  # 绝对路径中当前脚本所在目录
    Path = os.path.join(proDir, "adxWebElement.yaml")
    DAMTrafficCfg_SELECTOR = YamlHelper().get_config_dict(Path)["DAM_AdCfg_TrafficCfgPage"]

    # 广告配置(新)2级页面,遍历页面顶部展示的广告位及DSP广告源信息
    def get_ad2trafficconfig_info(self):
        """
        广告配置(新)2级页面,遍历页面顶部展示的广告位及DSP广告源信息
        :param
        :return: 遍历到的展示信息
        """
        ad2trafficconfig_info_list = self.base_driver.get_table_cell_text_list(
            self.DAMTrafficCfg_SELECTOR["TRAFFICCFG_TITLEBAR_SELECTOR"], 2, 5, 1, 1)
        return ad2trafficconfig_info_list

    # 广告配置(新)2级页面,设置有效时间段为01:00 - 02:00
    def set_time(self):
        """
        广告配置(新)2级页面,设置有效时间段为01:00 - 02:00
        :param
        :return:
        """
        # 点击有效时间段
        self.base_driver.click(self.DAMTrafficCfg_SELECTOR["TRAFFICCFG_CONFIG_TIMEINPUT_SELECTOR"])
        self.base_driver.forced_wait(1)
        # 设置开始时间为01:00
        self.base_driver.click(str(self.DAMTrafficCfg_SELECTOR["TRAFFICCFG_CONFIG_TIME_SELECTOR"]).format(1, 2))
        self.base_driver.forced_wait(1)
        # 设置结束时间为02:00
        self.base_driver.click(str(self.DAMTrafficCfg_SELECTOR["TRAFFICCFG_CONFIG_TIME_SELECTOR"]).format(2, 3))
        self.base_driver.forced_wait(2)

    # 广告配置(新)2级页面,设置竞价价格(eCPM),一级展示上限,一级预估点击率,二级预下发量占比,有效时间段
    def set_ad2trafficconfig_item(self, text_list):
        """
        广告配置(新)2级页面,设置竞价价格(eCPM),一级展示上限,一级预估点击率,二级预下发量占比,有效时间段
        :param
        :return:
        """
        text_index = 0
        for i in range(1, 2):
            for j in [2, 3, 5, 6]:
                self.base_driver.type(
                    self.DAMTrafficCfg_SELECTOR["TRAFFICCFG_CONFIG_ITEM_SELECTOR"].format(i, j), text_list[text_index])
                text_index = text_index + 1
                self.base_driver.forced_wait(1)
        self.base_driver.forced_wait(1)

        self.set_time()
        self.base_driver.forced_wait(1)

    # 广告配置(新)2级页面,点击保存
    def click_save_btn(self):
        """
        广告配置(新)2级页面,点击保存
        :param
        :return:
        """
        self.base_driver.click(self.DAMTrafficCfg_SELECTOR["TRAFFICCFG_SAVE_SELECTOR"])
        self.base_driver.forced_wait(2)

    # 广告配置(新)2级页面,点击刷新
    def click_refresh_btn(self):
        """
        广告配置(新)2级页面,点击保存
        :param
        :return:
        """
        self.base_driver.click(self.DAMTrafficCfg_SELECTOR["TRAFFICCFG_REFRESH_SELECTOR"])
        self.base_driver.forced_wait(2)

    # 批量新增后,获取24行每一行的有效时间段
    def get_column_texts(self, selector, rownum):
        """
        获取行数
        :param selector: 对应字段的定位
        :param rownum: 行数,一共要获取几行
        :return: 以列表的形式返回获取到的所有值
        """
        value_list = []
        for i in range(1, rownum + 1):
            locate = self.base_driver._locate_element(selector.format(i))
            value_list.append(locate.get_attribute("value"))
        print(value_list)
        return value_list

    # 广告配置(新)2级页面,获取第一行有效时间段的值
    def get_time_text(self):
        """
        广告配置(新)2级页面,获取第一行有效时间段的值
        :param
        :return:有效时间段的值
        """
        time_text = self.get_column_texts(self.DAMTrafficCfg_SELECTOR["TRAFFICCFG_CONFIG_TIMEINPUTS_SELECTOR"], 1)
        return time_text

    # 广告配置(新)2级页面,获取竞价价格(eCPM),一级展示上限,一级预估点击率,二级预下发量占比,有效时间段的值
    def get_input_texts(self, selector, rownum):
        """
        广告配置(新)2级页面,获取竞价价格(eCPM),一级展示上限,一级预估点击率,二级预下发量占比,有效时间段的值
        :param
        :return: 以list的形式返回获取到的值
        """
        current_value_list = []
        for i in range(1, rownum + 1):
            for j in [2, 3, 5, 6]:
                locate = self.base_driver._locate_element(selector.format(i, j))
                current_value_list.append(locate.get_attribute("value"))
                self.base_driver.forced_wait(1)
        print(current_value_list)
        return current_value_list

    # 广告配置(新)2级页面,获取第1行竞价价格(eCPM),一级展示上限,一级预估点击率,二级预下发量占比,有效时间段的值
    def get_ad2trafficconfig_rows1_text(self):
        """
        广告配置(新)2级页面,获取第1行竞价价格(eCPM),一级展示上限,一级预估点击率,二级预下发量占比,有效时间段的值
        :param
        :return: 以list的形式返回获取到的值
        """
        current_value_list = self.get_input_texts(self.DAMTrafficCfg_SELECTOR["TRAFFICCFG_CONFIG_ITEM_SELECTOR"], 1)
        '''
        for i in range(1, 2):
            for j in [2, 3, 5, 6]:
                locate = self.base_driver._locate_element(
                    str(self.DAMTrafficCfg_SELECTOR["TRAFFICCFG_CONFIG_ITEM_SELECTOR"]).format(i, j))
                current_value_list.append(locate.get_attribute("value"))
                self.base_driver.forced_wait(1)
        '''
        current_value_list.extend(self.get_time_text())
        return current_value_list

    # 广告配置(新)2级页面,判断该广告位二级预下发量配置是否为空(判断第1行)
    def is_ad2trafficconfig_empty(self):
        """
        广告配置(新)2级页面,判断该广告位下二级预下发量配置是否为空(判断第1行)
        :param
        :return: 为空返回True,不为空返回False
        """
        current_value_list = self.get_ad2trafficconfig_rows1_text()
        if current_value_list == ['0', '0', '0', '0', '00:00 - 00:00']:
            return True
        else:
            return False

    # 广告配置(新)2级页面,点击重置并确认
    def click_reset_btn(self):
        """
        广告配置(新)2级页面,点击重置并确认
        :param
        :return:
        """
        self.base_driver.click(self.DAMTrafficCfg_SELECTOR["TRAFFICCFG_RESET_SELECTOR"])
        self.base_driver.forced_wait(1)
        self.base_driver.click(self.DAMTrafficCfg_SELECTOR["TRAFFICCFG_RESET_OK_SELECTOR"])
        self.base_driver.forced_wait(2)

    # 广告配置(新)2级页面,点击批量新增
    def click_batch_add_btn(self):
        """
        广告配置(新)2级页面,点击批量新增
        :param
        :return:
        """
        self.base_driver.click(self.DAMTrafficCfg_SELECTOR["TRAFFICCFG_BATCH_ADD_SELECTOR"])
        self.base_driver.forced_wait(2)

    # 获取行数
    def get_row_num(self):
        """
        获取行数
        :param
        :return: 返回行数
        """
        locate = self.base_driver._locate_element(self.DAMTrafficCfg_SELECTOR["TRAFFICCFG_CONFIG_ROWS_SELECTOR"])
        rownum = len(locate.find_elements_by_xpath("//*[@class='c1 ivu-row']"))
        print("行数: %s" % rownum)
        return rownum

    # 广告配置(新)2级页面,批量新增后,获取24行每一行的有效时间段
    def get_time_texts(self):
        """
        广告配置(新)2级页面,批量新增后,获取24行每一行的有效时间段
        :param
        :return:获取到的24个有效时间段的值
        """
        time_texts_list = self.get_column_texts(self.DAMTrafficCfg_SELECTOR["TRAFFICCFG_CONFIG_TIMEINPUTS_SELECTOR"],
                                                24)
        return time_texts_list

    # 广告配置(新)2级页面,批量新增后,获取24行每一行的竞价价格(eCPM),一级展示上限,一级预估点击率,二级预下发量占比
    def get_ad2trafficconfig_rows24_text(self):
        """
        广告配置(新)2级页面,获取24行每一行的竞价价格(eCPM),一级展示上限,一级预估点击率,二级预下发量占比,有效时间段的值
        :param
        :return: 以list的形式返回获取到的值
        """
        current_value_list = self.get_input_texts(self.DAMTrafficCfg_SELECTOR["TRAFFICCFG_CONFIG_ITEM_SELECTOR"], 24)
        return current_value_list

    # 针对列表,循环输入文本
    def batch_input(self, selector, text_list, row_num=None, column_num=None, start_row_index=None,
                    start_column_index=None):
        """
        针对列表,循环输入文本
        :param selector: 元素组定位
        :param text_list: 将要输入的所有值以行为单位,以list的形式传入
        :param start_row_index: 开始行数的索引,默认为0
        :param row_num: 共有几行
        :param start_column_index: 开始列数的索引,默认为0
        :param column_num: 共有几列
        :return:
        """
        if start_row_index is None:
            start_row_index = 0
        if row_num is None:
            row_num = 0
        if start_column_index is None:
            start_column_index = 0
        if column_num is None:
            column_num = 0

        text_index = 0
        for i in range(start_row_index, row_num + 1):
            for j in range(start_column_index, column_num + 1):
                self.base_driver.type(selector.format(i, j), text_list[text_index])
                text_index = text_index + 1
                self.base_driver.forced_wait(1)

    # 广告配置(新)2级页面,设置批量修改-竞价价格(ECPM),一级展示量上限,一级预估点击率,二级预下发量占比
    def set_batch_modify_item(self, text_list):
        """
        广告配置(新)2级页面,设置批量修改-竞价价格(ECPM),一级展示量上限,一级预估点击率,二级预下发量占比
        :param
        :return
        """
        self.batch_input(self.DAMTrafficCfg_SELECTOR["TRAFFICCFG_BATCH_INPUT_SELECTOR"], text_list, 4, 1, 1, 1)

    # 广告配置(新)2级页面,开启批量修改开关-竞价价格(ECPM),一级展示量上限,一级预估点击率,二级预下发量占比
    def turn_on_batch_modify_switch(self):
        """
        广告配置(新)2级页面,设置批量修改开关-竞价价格(ECPM),一级展示量上限,一级预估点击率,二级预下发量占比
        :param
        :return
        """
        for i in range(1, 5):
            selector = str(self.DAMTrafficCfg_SELECTOR["TRAFFICCFG_BATCH_SWITCH_SELECTOR"]).format(i)
            switch_status = self.base_driver.get_attribute(selector, "value")
            print(switch_status)
            if switch_status == "false":
                self.base_driver.click(selector)
            self.base_driver.forced_wait(1)
