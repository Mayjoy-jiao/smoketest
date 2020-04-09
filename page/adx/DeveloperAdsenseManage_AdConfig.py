from common.webCommon import YamlHelper
from page.adx.DeveloperAdsenseManage import DeveloperAdsenseManagePage
import os
from common.configDB import MyDB
class DeveloperAdsenseManage_AdConfigPage(DeveloperAdsenseManagePage):
    proDir = os.path.split(os.path.realpath(__file__))[0]  # 绝对路径中当前脚本所在目录
    Path = os.path.join(proDir, "adxWebElement.yaml")
    DAMADCONFIG_SELECTOR = YamlHelper().get_config_dict(Path)["DeveloperAdsenseManage_AdConfigPage"]

    def enter_frame(self):
        """
        进入广告配置（新）页面的框架
        :return:
        """
        self.base_driver.switch_to_frame(self.DAMADCONFIG_SELECTOR["DEVELOPER_ADSENSE_ADCONFIG_IFRAME_SELECTOR"])
        self.base_driver.forced_wait(3)

    def quit_frame(self):
        """
        退出框架
        :return:
        """
        self.base_driver.switch_to_default()

    # 获取页头部广告位的信息
    def get_title_bar_text(self,title):
        """
        获取广告配置的页面的广告位信息展示
        :param title: 信息展示的类型
        :return: 获取到的元素的值
        """
        if title == "developerName":
            local =  self.DAMADCONFIG_SELECTOR["DEVELOPER_ADSENSE_ADCONFIG_TITLEBAR_SELECTOR"] % 1
            title_text = self.base_driver.get_text(local)
        elif title == "developerApp":
            local =  self.DAMADCONFIG_SELECTOR["DEVELOPER_ADSENSE_ADCONFIG_TITLEBAR_SELECTOR"] % 2
            title_text = self.base_driver.get_text(local)
        elif title == "adsenseName":
            local =  self.DAMADCONFIG_SELECTOR["DEVELOPER_ADSENSE_ADCONFIG_TITLEBAR_SELECTOR"] % 3
            title_text = self.base_driver.get_text(local)
        elif title == "adsenseType":
            local =  self.DAMADCONFIG_SELECTOR["DEVELOPER_ADSENSE_ADCONFIG_TITLEBAR_SELECTOR"] % 4
            title_text = self.base_driver.get_text(local)
        elif title == "DSPType":
            local =  self.DAMADCONFIG_SELECTOR["DEVELOPER_ADSENSE_ADCONFIG_TITLEBAR_SELECTOR"] % 5
            title_text = self.base_driver.get_text(local)
        else:
            title_text = "error title"
        return title_text

    #获取请求数输入框的属性
    def get_requestNum_attribute(self):
        requestNum_attribute = self.base_driver.get_attribute(self.DAMADCONFIG_SELECTOR["DEVELOPER_ADSENSE_ADCONFIG_REQUESTNUM_SELECTOR"],"type")
        return requestNum_attribute

    # 获取竞价比例的输入框属性
    def get_biddingRate_attribute(self):
        biddingRate_attribute = self.base_driver.get_attribute(self.DAMADCONFIG_SELECTOR["DEVELOPER_ADSENSE_ADCONFIG_BIDDINGRATE_SELECTOR"],"type")
        return biddingRate_attribute

    # 获取测试广告的显示框的文本信息
    def get_test_advertisement(self):
        ad = self.base_driver.get_attribute("x,/html/body/div[1]/div/form[1]/div[3]/div[3]/div/div/div/div/div[1]/input", "value")
        print(f"挑选的测试广告是：{ad}")
        return ad

    # 保存请求数和竞价比例
    def save_requestNum_bidding(self, requestNum, bidding):
        rep = []
        self.base_driver.clear_text(self.DAMADCONFIG_SELECTOR["DEVELOPER_ADSENSE_ADCONFIG_REQUESTNUM_SELECTOR"])
        self.base_driver.type(self.DAMADCONFIG_SELECTOR["DEVELOPER_ADSENSE_ADCONFIG_REQUESTNUM_SELECTOR"], requestNum)
        self.base_driver.forced_wait(1)

        self.base_driver.clear_text(self.DAMADCONFIG_SELECTOR["DEVELOPER_ADSENSE_ADCONFIG_BIDDINGRATE_SELECTOR"])
        self.base_driver.type(self.DAMADCONFIG_SELECTOR["DEVELOPER_ADSENSE_ADCONFIG_BIDDINGRATE_SELECTOR"], bidding)
        self.base_driver.forced_wait(2)

        self.base_driver.click("x, /html/body/div[1]/div/form[1]/div[3]/div[4]/div/div/button")
        # self.base_driver.click(self.DAMADCONFIG_SELECTOR["DEVELOPER_ADSENSE_ADCONFIG_SAVEBUTTON1_SELECTOR"])
        self.base_driver.forced_wait(5)
        sql = "select request_num,bid_rate from ssp.pub_app_ad_dsp where pub_app_ad_id=1046 and dsp_app_id=261"
        mysql = MyDB()
        data = mysql.mysqlDB("192.168.0.223", "zzmanager", "iadMOB-2013@0622)",3306, "ssp", sql)
        return data

    # DSP搜索
    def search_dsp(self):
        """
        广告配置页面的dsp搜索功能，返回选择哪个dsp选项及该选项匹配的记录数，可以通过查数据库，验证筛选的数据是否正确
        遗留问题: 页面元素分离无法获取到元素，一直提示KeyError

        :return:
        """
        result = {}
        record = []
        # self.base_driver.click(self.DAMADCONFIG_SELECTOR["DEVELOPER_ADSENSE_ADCONFIG_SEARCH_DSP_SELECTOR"])
        self.base_driver.click("x, /html/body/div[1]/div/form[2]/div/div[1]/div/div/div/div[1]/div/input")
        # 点击第四个选项
        # self.base_driver.click(self.DAMADCONFIG_SELECTOR["DEVELOPER_ADSENSE_ADCONFIG_SEARCH_DSP_LI_SELECTOR"])
        self.base_driver.click("x, /html/body/div[1]/div/form[2]/div/div[1]/div/div/div/div[2]/ul[2]/li[4]")
        # 获取选项的文本信息
        # search_dsp_text = self.base_driver.get_text(self.DAMADCONFIG_SELECTOR["DEVELOPER_ADSENSE_ADCONFIG_SEARCH_DSP_LI_SELECTOR"])
        search_dsp_text = self.base_driver.get_text("x, /html/body/div[1]/div/form[2]/div/div[1]/div/div/div/div[2]/ul[2]/li[4]")
        print(f"选择{search_dsp_text}进行查询")

        self.base_driver.forced_wait(5)
        # 获取搜粟结果有多少条记录
        # dsp_rowcount = len(self.DAMADCONFIG_SELECTOR["DEVELOPER_ADSENSE_ADCONFIG_SEARCH_DSP_TBODY_SELECTOR"])
        dsp_rowcount = len(self.base_driver._locate_elements("x, /html/body/div[1]/div/div[1]/div/div[2]/table/tbody/tr"))
        print(f"查询符合数据记录:{dsp_rowcount}")

        for i in range(1,dsp_rowcount+1):
            # record.append(self.base_driver.get_text(self.DAMADCONFIG_SELECTOR["DEVELOPER_ADSENSE_ADCONFIG_SEARCH_DSP_RECORD_SELECTOR"] % i))
            record.append(self.base_driver.get_text("x, /html/body/div[1]/div/div[1]/div/div[2]/table/tbody/tr[%d]/td[2]/div/span" % i))
        result["search_dsp_text"] = search_dsp_text
        result["dsp_rowcount"] = dsp_rowcount
        result["record"] = record

        # 点击刷新按钮
        # self.base_driver.click(self.DAMADCONFIG_SELECTOR["DEVELOPER_ADSENSE_ADCONFIG_REFRESHBUTTON_SELECTOR"])
        self.base_driver.click("x, /html/body/div[1]/div/form[1]/div[3]/div[5]/div/div/button")
        self.base_driver.forced_wait(3)
        # 返回现在的选项名称和该选项下匹配的记录条数
        return result

    # DSP应用搜索
    def search_dsp_app(self):
        """
        广告配置页面的dsp应用搜索功能，返回选择哪个dsp应用选项及该选项匹配的记录数，可以通过查数据库，验证筛选的数据是否正确
        :return:
        """
        # result = {}
        # self.base_driver.click(self.DAMADCONFIG_SELECTOR["DEVELOPER_ADSENSE_ADCONFIG_SEARCH_DSP_APP_SELECTOR"])
        # # 点击第二个选项
        # self.base_driver.click(self.DAMADCONFIG_SELECTOR["DEVELOPER_ADSENSE_ADCONFIG_SEARCH_DSP_APP_LI_SELECTOR"])
        # # 获取选项的文本信息
        # search_dsp_app_text = self.base_driver.get_text(self.DAMADCONFIG_SELECTOR["DEVELOPER_ADSENSE_ADCONFIG_SEARCH_DSP_APP_LI_SELECTOR"])
        # self.base_driver.forced_wait(2)
        # # 获取搜粟结果有多少条记录
        # dsp_app_rowcount = len(self.DAMADCONFIG_SELECTOR["DEVELOPER_ADSENSE_ADCONFIG_SEARCH_DSP_TBODY_SELECTOR"])
        # # 点击刷新按钮
        # self.base_driver.click(self.DAMADCONFIG_SELECTOR["DEVELOPER_ADSENSE_ADCONFIG_REFRESHBUTTON_SELECTOR"])
        # result["search_dsp_app_text"] = search_dsp_app_text
        # result["dsp_app_rowcount"] = dsp_app_rowcount
        # self.base_driver.forced_wait(3)
        # # 返回现在的选项名称和该选项下匹配的记录条数
        result = {}
        record = []
        self.base_driver.click("x, /html/body/div[1]/div/form[2]/div/div[2]/div/div/div/div[1]/div/input")
        # 点击第二个选项
        self.base_driver.click("x, /html/body/div[1]/div/form[2]/div/div[2]/div/div/div/div[2]/ul[2]/li[2]")
        # 获取选项的文本信息
        search_dsp_text = self.base_driver.get_text("x, /html/body/div[1]/div/form[2]/div/div[2]/div/div/div/div[2]/ul[2]/li[2]")
        print(f"选择{search_dsp_text}进行查询")
        self.base_driver.forced_wait(5)

        # 获取搜粟结果有多少条记录
        dsp_rowcount = len(self.base_driver._locate_elements("x, /html/body/div[1]/div/div[1]/div/div[2]/table/tbody/tr"))
        print(f"查询符合数据记录:{dsp_rowcount}")

        for i in range(1, dsp_rowcount + 1):
            record.append(self.base_driver.get_text("x, /html/body/div[1]/div/div[1]/div/div[2]/table/tbody/tr[%d]/td[3]/div/span" % i))
        result["search_dsp_text"] = search_dsp_text
        result["dsp_rowcount"] = dsp_rowcount
        result["record"] = record

        # 点击刷新按钮
        self.base_driver.click("x, /html/body/div[1]/div/form[1]/div[3]/div[5]/div/div/button")
        self.base_driver.forced_wait(3)

        # 返回现在的选项名称和该选项下匹配的记录条数
        return result

    # DSP类型搜索
    def search_dsp_type(self):
        """
        广告配置页面的dsp类型搜索功能，返回选择哪个dsp类型选项及该选项匹配的记录数，可以通过查数据库，验证筛选的数据是否正确
        :return:
        """
        # result = {}
        # self.base_driver.click(self.DAMADCONFIG_SELECTOR["DEVELOPER_ADSENSE_ADCONFIG_SEARCH_DSP_TYPE_SELECTOR"])
        # # 点击第2个选项
        # self.base_driver.click(self.DAMADCONFIG_SELECTOR["DEVELOPER_ADSENSE_ADCONFIG_SEARCH_DSP_TYPE_LI_SELECTOR"])
        # # 获取选项的文本信息
        # search_dsp_type_text = self.base_driver.get_text(self.DAMADCONFIG_SELECTOR["DEVELOPER_ADSENSE_ADCONFIG_SEARCH_DSP_TYPE_LI_SELECTOR"])
        # self.base_driver.forced_wait(2)
        # # 获取搜粟结果有多少条记录
        # dsp_type_rowcount = len(self.DAMADCONFIG_SELECTOR["DEVELOPER_ADSENSE_ADCONFIG_SEARCH_DSP_TBODY_SELECTOR"])
        # # 点击刷新按钮
        # self.base_driver.click(self.DAMADCONFIG_SELECTOR["DEVELOPER_ADSENSE_ADCONFIG_REFRESHBUTTON_SELECTOR"])
        # result["search_dsp_type_text"] = search_dsp_type_text
        # result["dsp_type_rowcount"] = dsp_type_rowcount
        # self.base_driver.forced_wait(3)
        # # 返回现在的选项名称和该选项下匹配的记录条数
        # return result

        result = {}
        record = []
        self.base_driver.click("x, /html/body/div[1]/div/form[2]/div/div[3]/div/div/div/div[1]/div/span")
        # 点击第二个选项
        self.base_driver.click("x, /html/body/div[1]/div/form[2]/div/div[3]/div/div/div/div[2]/ul[2]/li[2]")
        # 获取选项的文本信息
        search_dsp_text = self.base_driver.get_text("x, /html/body/div[1]/div/form[2]/div/div[3]/div/div/div/div[2]/ul[2]/li[2]")
        print(f"选择{search_dsp_text}进行查询")
        self.base_driver.forced_wait(5)

        # 获取搜粟结果有多少条记录
        dsp_rowcount = len(
            self.base_driver._locate_elements("x, /html/body/div[1]/div/div[1]/div/div[2]/table/tbody/tr"))
        print(f"查询符合数据记录:{dsp_rowcount}")

        for i in range(1, dsp_rowcount + 1):
            record.append(self.base_driver.get_text("x, /html/body/div[1]/div/div[1]/div/div[2]/table/tbody/tr[%d]/td[4]/div/div/strong" % i))
        result["search_dsp_text"] = search_dsp_text
        result["dsp_rowcount"] = dsp_rowcount
        result["record"] = record

        # 点击刷新按钮
        self.base_driver.click("x, /html/body/div[1]/div/form[1]/div[3]/div[5]/div/div/button")
        self.base_driver.forced_wait(3)

        # 返回现在的选项名称和该选项下匹配的记录条数
        return result

    # 是否全时间段搜索
    def search_is_fullTime(self):
        """
        广告配置页面的dsp类型搜索功能，返回选择哪个dsp类型选项及该选项匹配的记录数，可以通过查数据库，验证筛选的数据是否正确
        :return:
        """
        # result = {}
        # self.base_driver.click(self.DAMADCONFIG_SELECTOR["DEVELOPER_ADSENSE_ADCONFIG_SEARCH_DSP_ISFULLTIME_SELECTOR"])
        # # 点击第3个选项
        # self.base_driver.click(self.DAMADCONFIG_SELECTOR["DEVELOPER_ADSENSE_ADCONFIG_SEARCH_DSP_ISFULLTIME_LI_SELECTOR"])
        # # 获取选项的文本信息
        # search_isfulltime_text = self.base_driver.get_text(self.DAMADCONFIG_SELECTOR["DEVELOPER_ADSENSE_ADCONFIG_SEARCH_DSP_ISFULLTIME_LI_SELECTOR"])
        # self.base_driver.forced_wait(2)
        # # 获取搜粟结果有多少条记录
        # isfulltime_rowcount = len(self.DAMADCONFIG_SELECTOR["DEVELOPER_ADSENSE_ADCONFIG_SEARCH_DSP_TBODY_SELECTOR"])
        # # 点击刷新按钮
        # self.base_driver.click(self.DAMADCONFIG_SELECTOR["DEVELOPER_ADSENSE_ADCONFIG_REFRESHBUTTON_SELECTOR"])
        # result["search_isfulltime_text"] = search_isfulltime_text
        # result["isfulltime_rowcount"] = isfulltime_rowcount
        # self.base_driver.forced_wait(3)
        # # 返回现在的选项名称和该选项下匹配的记录条数
        # return result

        result = {}
        record = []
        self.base_driver.click("x, /html/body/div[1]/div/form[2]/div/div[4]/div/div/div/div[1]")
        # 点击第二个选项
        self.base_driver.click("x, /html/body/div[1]/div/form[2]/div/div[4]/div/div/div/div[2]/ul[2]/li[3]")
        # 获取选项的文本信息
        search_dsp_text = self.base_driver.get_text("x, /html/body/div[1]/div/form[2]/div/div[4]/div/div/div/div[2]/ul[2]/li[3]")
        print(f"选择{search_dsp_text}进行查询")
        self.base_driver.forced_wait(5)

        # 获取搜粟结果有多少条记录
        dsp_rowcount = len(
            self.base_driver._locate_elements("x, /html/body/div[1]/div/div[1]/div/div[2]/table/tbody/tr"))
        print(f"查询符合数据记录:{dsp_rowcount}")

        for i in range(1, dsp_rowcount + 1):
            record.append(self.base_driver.get_text(
                "x, /html/body/div[1]/div/div[1]/div/div[2]/table/tbody/tr[%d]/td[8]/div/div/strong" % i))
        result["search_dsp_text"] = search_dsp_text
        result["dsp_rowcount"] = dsp_rowcount
        result["record"] = record

        # 点击刷新按钮
        self.base_driver.click("x, /html/body/div[1]/div/form[1]/div[3]/div[5]/div/div/button")
        self.base_driver.forced_wait(3)

        # 返回现在的选项名称和该选项下匹配的记录条数
        return result

    # DSP应用的保存
    def open_dsp_app(self):
        value = self.base_driver.get_attribute("x,/html/body/div[1]/div/div[1]/div/div[2]/table/tbody/tr[1]/td[12]/div/div/span/input","value")
        print(f"点击前的开关状态:{value}")
        if value == "false":
            self.base_driver.click("x,/html/body/div[1]/div/div[1]/div/div[2]/table/tbody/tr[1]/td[12]/div/div/span/span/span")
            self.base_driver.forced_wait(3)
            self.base_driver.click('x,//*[@id="saveAButton + {index}"]/span')
            self.base_driver.forced_wait(3)
            value = self.base_driver.get_attribute("x,/html/body/div[1]/div/div[1]/div/div[2]/table/tbody/tr[1]/td[12]/div/div/span/input","value")
        else:
            pass
        print(f"点击后的开关状态:{value}")
        return value

    # RTB 的DSP要有竞价低价
        """
        数据库查询出所有RTB的dsp，然后获取列表中的dsp，如果dsp匹配的，则需要有input标签
        """
    # 竞价低价的保存


    # SYP

    # 广告配置(新)1级页面,遍历顶部展示的广告位信息
    def get_adconfig_adsense_info(self):
        """
        广告配置(新)1级页面,获取顶部展示的广告位信息
        :param
        :return: 返回遍历到的展示信息
        """
        adconfig_adsense_info_list = self.base_driver.get_table_cell_text_list(
            self.DAMADCONFIG_SELECTOR["DEVELOPER_ADSENSE_ADCONFIG_TITLEBAR_SELECTOR2"], 1, 5, 1, 1)
        return adconfig_adsense_info_list

    # 广告配置(新)1级页面, 获取4个下拉框定位
    def get_dropdown_box_selector(self, dropdown_box_name):
        """
        广告配置(新)1级页面,获取4个下拉框定位
        :param dropdown_box_name: 下拉框名称
        :return: 下拉框定位
        """
        if dropdown_box_name == "DSP":
            local = self.DAMADCONFIG_SELECTOR["DEVELOPER_ADSENSE_ADCONFIG_DROPDOWNBOX1_SELECTOR"] % 1
        elif dropdown_box_name == "DSPApp":
            local = self.DAMADCONFIG_SELECTOR["DEVELOPER_ADSENSE_ADCONFIG_DROPDOWNBOX1_SELECTOR"] % 2
        elif dropdown_box_name == "DSPType":
            local = self.DAMADCONFIG_SELECTOR["DEVELOPER_ADSENSE_ADCONFIG_DROPDOWNBOX2_SELECTOR"] % 3
        elif dropdown_box_name == "isFullTime":
            local = self.DAMADCONFIG_SELECTOR["DEVELOPER_ADSENSE_ADCONFIG_DROPDOWNBOX2_SELECTOR"] % 4
        else:
            local = "error dropdownbox name"
        return local

    # 广告配置(新)1级页面,筛选DSP应用
    def select_dsp_app(self, dsp_app_name):
        """
        广告配置(新)1级页面,筛选DSP应用
        :param dsp_app_name: DSP应用名称

        """
        dsp_app_selector = self.get_dropdown_box_selector("DSPApp")
        self.base_driver.type(dsp_app_selector, dsp_app_name)
        self.base_driver.forced_wait(1)
        self.base_driver.click(self.DAMADCONFIG_SELECTOR["DEVELOPER_ADSENSE_ADCONFIG_DROPDOWNLIST_DSPAPP_SELECTOR"])
        self.base_driver.forced_wait(1)

    # 广告配置(新)1级页面,遍历列表,获取指定的DSP广告源的信息
    def get_dsp_info(self):
        """
        广告配置(新)1级页面,遍历列表,获取指定的DSP广告源的信息
        :param
        :return: 获取到的广告源信息
        """
        dsp_info_list = []
        # result_list = []
        selector1 = self.DAMADCONFIG_SELECTOR["DEVELOPER_ADSENSE_ADCONFIG_TBFEILD_SELECTOR1"]
        selector2 = self.DAMADCONFIG_SELECTOR["DEVELOPER_ADSENSE_ADCONFIG_TBFEILD_SELECTOR2"]
        for i in range(1, 2):
            for j in range(2, 4):
                locate = self.base_driver._locate_element(str(selector1).format(i, j))
                dsp_info_list.append(locate.text)
        for m in range(1, 2):
            for n in range(4, 6):
                locate = self.base_driver._locate_element(str(selector2).format(m, n))
                dsp_info_list.append(locate.text)
        result_list = ['DSP: '+dsp_info_list[0], 'DSP应用: '+dsp_info_list[1], 'DSP类型: '+dsp_info_list[2], 'DSP最高点击率: '+dsp_info_list[3]]
        return result_list

    # 广告配置(新)1级页面,获取列表中开闭字段的属性
    def get_switch_attribute(self):
        """
        广告配置(新)1级页面,获取列表中开闭字段的属性
        :return: 获取到的元素的对应属性
        """
        switch_selector = str(self.DAMADCONFIG_SELECTOR["DEVELOPER_ADSENSE_ADCONFIG_SWITCH_SELECTOR"])
        switch_attribute = self.base_driver.get_text(switch_selector)
        if switch_attribute == "关":
            switch_attribute = "闭"
        switch_attribute = '开闭: ' + switch_attribute
        return [switch_attribute]

    # 广告配置(新)1级页面,进入2级页面
    def checkin_ad2trafficconfig_page(self):
        """
        广告配置(新)1级页面,进入2级页面
        """
        self.base_driver.click(self.DAMADCONFIG_SELECTOR["DEVELOPER_ADSENSE_ADCONFIG_CONFIG_BTN_SELECTOR"])
        self.base_driver.forced_wait(3)

    # 广告配置(新)1级页面,进入指定的DSP应用的2级页面
    def checkin_ad2trafficconfig_page_withdspapp(self, dsp_app_name):
        """
        广告配置(新)1级页面,进入指定的DSP应用的2级页面
        """
        self.select_dsp_app(dsp_app_name)
        self.checkin_ad2trafficconfig_page()