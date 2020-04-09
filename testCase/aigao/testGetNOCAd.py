"""
NOC广告拉取前提：
    1.【渠道列表-选择渠道-其他广告设置-NOC广告设置】，“NOC广告开关：打开”，且未被屏蔽省市
    2.【NOC广告管理】广告运行，且当前日期有下发流量
5.1.3.208-5需求
1.补充5.1.3.208-4需求，广告下发拉活配置信息
2.5.1.3.208-5需求，NOC广告下发，下发广告媒体体包的包名和版本号
3.5.1.3.208-5需求，投放渠道规则生效，广告选择的规则中包含渠道，则该渠道可以拉取该媒体包广告，否则拉取不到该媒体包

测试相关数据：
使用渠道：CL88_0001
使用mid：ssiddca98c74423142258b994801ed9f7794
投放noc规则：NOC规则_自动化脚本 id=23
使用NOC广告：NOC广告_自动化脚本 id=44

"""

import unittest
import paramunittest
from common import common
from common.configDB import MyDB
from common.Log import MyLog
import datetime
import time

aigao_xls = common.get_xls("aigao.xlsx", "aigao")
# @paramunittest.parametrized(aigao_xls[1])

class TestGetNocAd(unittest.TestCase):
    def setParameters(self, case_name, url, method, token, goods_id, result, code, msg):
        """

        :param case_name:
        :param url:
        :param method:
        :param token:
        :param goods_id:
        :param result:
        :param code:
        :param msg:
        :return:
        """
        self.case_name = str(case_name)
        self.url = str(url)
        self.method = str(method)
        self.token = str(token)
        self.goodsId = str(goods_id)
        self.result = str(result)
        self.code = str(code)
        self.msg = str(msg)
        self.response = None
        self.info = None

    def description(self):
        self.case_name

    def setUp(self):
        self.log = MyLog.get_log()
        self.logger = self.log.get_logger()

    def tearDown(self):
        pass

    def set_NOCAd_switch(self,switch):
        """
        NOC广告开光：
        switch=on，打开开关
        switch=off，关闭开关
        :param switch:
        :return:
        """
        if switch=="on":
            sql = "update ad_channel_new_noc set newNocAdSwitch=1 where config_id='645';"
            MyDB().mysqlDB("113.31.86.153", "zzmanager", "iadMOB-2013@0622)", 3306, "iadsupport", sql)
        elif switch=="off":
            sql = "update ad_channel_new_noc set newNocAdSwitch=0 where config_id='645';"
            MyDB().mysqlDB("113.31.86.153", "zzmanager", "iadMOB-2013@0622)", 3306, "iadsupport", sql)
        else:
            raise Exception("开关操作失败")

    def set_shield_proAndcity(self,shield):
        """
        因为只有imsi深圳的，所以此处屏蔽广东省深圳市
        shield=0,屏蔽深圳市
        shield=1，不屏蔽深圳市
        :return:
        """
        if shield==0:
            sql = "update ad_channel_new_noc set province='020',city=164 where config_id='645';"
            MyDB().mysqlDB("113.31.86.153", "zzmanager", "iadMOB-2013@0622)", 3306, "iadsupport", sql)
        elif shield==1:
            sql = "update ad_channel_new_noc set province=null,city=null where config_id='645';"
            MyDB().mysqlDB("113.31.86.153", "zzmanager", "iadMOB-2013@0622)", 3306, "iadsupport", sql)
        else:
            print("屏蔽操作有误！")

    def set_flow(self):
        """
        设置NOC广告下发流量
        :return:
        """
        sql1 = "select ad_id from new_noc_ad where ad_name='NOC广告_自动化脚本';"
        # NocAd_id = MyDB().mysqlDB("113.31.86.153", "zzmanager", "iadMOB-2013@0622)", 3306, "iadsupport", sql1)
        # 获取当前年月日
        dt = "'"+str(datetime.datetime.now()).split(' ')[0]+"'"
        sql2= f"update new_noc_ad_limit set date={dt} where ad_id =44;"
        print(sql2)
        MyDB().mysqlDB("113.31.86.153", "zzmanager", "iadMOB-2013@0622)", 3306, "iadsupport", sql2)

    def set_wake_switch(self,switch):
        """
        设置NOC广告拉活设置的开关
        :param switch:
        :return:
        """
        if switch=='on':
            sql = 'update new_noc_ad set wake_switch = 1 where ad_id = 44'
            MyDB().mysqlDB("113.31.86.153", "zzmanager", "iadMOB-2013@0622)", 3306, "iadsupport", sql)
        elif switch=='off':
            sql = 'update new_noc_ad set wake_switch = 0 where ad_id = 44'
            MyDB().mysqlDB("113.31.86.153", "zzmanager", "iadMOB-2013@0622)", 3306, "iadsupport", sql)

    def test_01switch_on(self):
        """
                打开NOC开关
                :return:
                """
        print("第一步：打开NOC广告设置的开关")
        self.set_NOCAd_switch("on")
        print("第二步：取消屏蔽广东省深圳市")
        self.set_shield_proAndcity(1)
        time.sleep(300)
        print("第三步：设置NOC广告下发流量")
        self.set_flow()
        print("第步：拉取NOC广告")
        data = {
            "channelId": "CL88",
            "mid": "ssiddca98c74423142258b994801ed9f7794",
            "imei": "865625020257042",
            "version": "2.4.5",
            "subChannelId": "0001",
            "appid": "1139",
            "imsi": "355440079021985",
            "adList": [3, 5],
            "waitInstallAds": [],
            "installedAds": [],
            "uninstallAds": []
        }
        # common.runJVM()
        NOCAd_info = common.runaigaoapi(data, 'http://test.iad.zzay.net/ps/getNewNocAd.do')["data"]
        print(NOCAd_info)
        self.assertIsNotNone(NOCAd_info)
        print("打开noc广告开关，可以正常拉取广告")

    def test_02PkgAndVerson(self):
        """
        208-5需求，NOC广告下发徐下发包名和版本号
        :return:
        """
        print("第一步：打开NOC广告设置的开关")
        self.set_NOCAd_switch("on")
        print("第二步：取消屏蔽广东省深圳市")
        self.set_shield_proAndcity(1)
        print("第三步：设置NOC广告下发流量")
        self.set_flow()
        print("第四步：拉取NOC广告")
        data = {
            "channelId": "CL88",
            "mid": "ssiddca98c74423142258b994801ed9f7794",
            "imei": "865625020257042",
            "version": "2.4.5",
            "subChannelId": "0001",
            "appid": "1139",
            "imsi": "355440079021985",
            "adList": [3, 5],
            "waitInstallAds": [],
            "installedAds": [],
            "uninstallAds": []
        }
        NOCAd_info = common.runaigaoapi(data, 'http://test.iad.zzay.net/ps/getNewNocAd.do')["data"]
        print(NOCAd_info)
        pkg = NOCAd_info["adList"][0]["pkgName"]
        version = NOCAd_info["adList"][0]["verCode"]
        self.assertIsNotNone(pkg)
        print("媒体包名随广告下发")
        self.assertIsNotNone(version)
        print("媒体包版本号随广告下发")

    def test_03switch_off(self):
        """
                关闭NOC开关
                :return:
                """
        print("第一步：关闭NOC广告设置的开关")
        self.set_NOCAd_switch("off")
        print("第二步：取消屏蔽广东省深圳市")
        self.set_shield_proAndcity(1)
        time.sleep(300)
        print("第三步：设置NOC广告下发流量")
        self.set_flow()
        print("第步：拉取NOC广告")
        data = {
            "channelId": "CL88",
            "mid": "ssiddca98c74423142258b994801ed9f7794",
            "imei": "865625020257042",
            "version": "2.4.5",
            "subChannelId": "0001",
            "appid": "1139",
            "imsi": "355440079021985",
            "adList": [3, 5],
            "waitInstallAds": [],
            "installedAds": [],
            "uninstallAds": []
        }
        NOCAd_info = common.runaigaoapi(data, 'http://test.iad.zzay.net/ps/getNewNocAd.do')["data"]
        print(NOCAd_info)
        self.assertIsNone(NOCAd_info)
        print("关闭noc广告开关，不能拉取广告")

    def test_04shield_proAndcity01(self):
        """
        屏蔽广东省深圳市
        :return:
        """
        print("第一步：打开NOC广告设置的开关")
        self.set_NOCAd_switch("on")
        print("第二步：屏蔽广东省深圳市")
        self.set_shield_proAndcity(0)
        time.sleep(480)
        print("第三步：设置NOC广告下发流量")
        self.set_flow()
        print("第步：拉取NOC广告")
        data = {
            "channelId": "CL88",
            "mid": "ssiddca98c74423142258b994801ed9f7794",
            "imei": "865625020257042",
            "version": "2.4.5",
            "subChannelId": "0001",
            "appid": "1139",
            "imsi": "355440079021985",
            "adList": [3, 5],
            "waitInstallAds": [],
            "installedAds": [],
            "uninstallAds": []
        }
        NOCAd_info = common.runaigaoapi(data, 'http://test.iad.zzay.net/ps/getNewNocAd.do')["data"]
        print(NOCAd_info)
        self.assertIsNone(NOCAd_info)
        print("屏蔽广东深圳，imsi为深圳的用户不能拉取广告")

    def test_05shield_proAndcity02(self):
        """
        取消屏蔽广东省深圳市
        :return:
        """
        print("第一步：打开NOC广告设置的开关")
        self.set_NOCAd_switch("on")
        print("第二步：取消屏蔽广东省深圳市")
        self.set_shield_proAndcity(1)
        time.sleep(300)
        print("第三步：设置NOC广告下发流量")
        self.set_flow()
        print("第步：拉取NOC广告")
        data={
        "channelId": "CL88",
        "mid": "ssiddca98c74423142258b994801ed9f7794",
        "imei": "865625020257042",
        "version": "2.4.5",
        "subChannelId": "0001",
        "appid": "1139",
        "imsi": "355440079021985",
        "adList": [3,5],
        "waitInstallAds": [],
        "installedAds": [],
        "uninstallAds": []
        }
        NOCAd_info=common.runaigaoapi(data,'http://test.iad.zzay.net/ps/getNewNocAd.do')["data"]
        print(NOCAd_info)
        self.assertIsNotNone(NOCAd_info)
        print("取消屏蔽广东深圳，imsi为深圳的用户可以正常拉取广告")

    def test_06wake_on(self):
        """
            打开NOC广告的拉活配置开关
            :return:
        """
        print("第一步：打开NOC广告设置的开关")
        self.set_NOCAd_switch("on")
        print("第二步：取消屏蔽广东省深圳市")
        self.set_shield_proAndcity(1)
        print("第三步：设置NOC广告下发流量")
        self.set_flow()
        print("第四步：打开NOC广告的拉活配置开关")
        self.set_wake_switch("on")
        time.sleep(200)
        print("第五步：拉取NOC广告")
        data = {
            "channelId": "CL88",
            "mid": "ssiddca98c74423142258b994801ed9f7794",
            "imei": "865625020257042",
            "version": "2.4.5",
            "subChannelId": "0001",
            "appid": "1139",
            "imsi": "355440079021985",
            "adList": [3, 5],
            "waitInstallAds": [],
            "installedAds": [],
            "uninstallAds": []
        }
        NOCAd_info = common.runaigaoapi(data, 'http://test.iad.zzay.net/ps/getNewNocAd.do')["data"]["wakeList"]
        print(NOCAd_info)
        self.assertIsNotNone(NOCAd_info)
        print("打开NOC广告的拉活配置开关,可以拉取到NOC广告的拉活配置")

    def test_07wake_off(self):
        """
            打开NOC广告的拉活配置开关
            :return:
        """
        print("第一步：打开NOC广告设置的开关")
        self.set_NOCAd_switch("on")
        print("第二步：取消屏蔽广东省深圳市")
        self.set_shield_proAndcity(1)
        print("第三步：设置NOC广告下发流量")
        self.set_flow()
        print("第四步：打开NOC广告的拉活配置开关")
        self.set_wake_switch("off")
        time.sleep(200)
        print("第五步：拉取NOC广告")
        data = {
            "channelId": "CL88",
            "mid": "ssiddca98c74423142258b994801ed9f7794",
            "imei": "865625020257042",
            "version": "2.4.5",
            "subChannelId": "0001",
            "appid": "1139",
            "imsi": "355440079021985",
            "adList": [3, 5],
            "waitInstallAds": [],
            "installedAds": [],
            "uninstallAds": []
        }
        NOCAd_info = common.runaigaoapi(data, 'http://test.iad.zzay.net/ps/getNewNocAd.do')["data"]["wakeList"]
        print(NOCAd_info)
        self.assertIsNotNone(NOCAd_info)
        print("关闭NOC广告的拉活配置开关,拉取不到NOC广告的拉活配置")

    def test_08limit01(self):
        """
        NOC广告id在请求上行等安装列表waitInstallAds中，不下发广告给客户端
        :return:
        """
        print("第一步：打开NOC广告设置的开关")
        self.set_NOCAd_switch("on")
        print("第二步：取消屏蔽广东省深圳市")
        self.set_shield_proAndcity(1)
        # time.sleep(300)
        print("第三步：设置NOC广告下发流量")
        self.set_flow()
        print("第四步：拉取NOC广告")
        data = {
            "channelId": "CL88",
            "mid": "ssiddca98c74423142258b994801ed9f7794",
            "imei": "865625020257042",
            "version": "2.4.5",
            "subChannelId": "0001",
            "appid": "1139",
            "imsi": "355440079021985",
            "adList": [3, 5],
            "waitInstallAds": [44],
            "installedAds": [],
            "uninstallAds": []
        }
        NOCAd_info = common.runaigaoapi(data, 'http://test.iad.zzay.net/ps/getNewNocAd.do')["data"]["adList"]
        if len(NOCAd_info) == 0:
            print(NOCAd_info)
            self.assertEqual(NOCAd_info, [])
            print("媒体待安装的渠道用户，不再下发广告")
        else:
            print(NOCAd_info)
            adId_list = []
            for i in NOCAd_info:
                adId_list.append(i["adId"])
            self.assertNotIn(44, adId_list)
            print("媒体待安装的渠道用户，不再下发广告")

    def test_09limit02(self):
        """
        NOC广告id在请求上行已安装列表installedAds中，不下发广告给客户端
        :return:
        """
        print("第一步：打开NOC广告设置的开关")
        self.set_NOCAd_switch("on")
        print("第二步：取消屏蔽广东省深圳市")
        self.set_shield_proAndcity(1)
        print("第三步：设置NOC广告下发流量")
        self.set_flow()
        print("第步：拉取NOC广告")
        data = {
            "channelId": "CL88",
            "mid": "ssiddca98c74423142258b994801ed9f7794",
            "imei": "865625020257042",
            "version": "2.4.5",
            "subChannelId": "0001",
            "appid": "1139",
            "imsi": "355440079021985",
            "adList": [3, 5],
            "waitInstallAds": [],
            "installedAds": [44],
            "uninstallAds": []
        }
        NOCAd_info = common.runaigaoapi(data, 'http://test.iad.zzay.net/ps/getNewNocAd.do')["data"]["adList"]
        if len(NOCAd_info) == 0:
            print(NOCAd_info)
            self.assertEqual(NOCAd_info, [])
            print("媒体已安装的渠道用户，不再下发广告")
        else:
            adId_list = []
            for i in NOCAd_info:
                adId_list.append(i["adId"])
            print(NOCAd_info)
            self.assertNotIn(44, adId_list)
            print("媒体已安装的渠道用户，不再下发广告")

    def test_10limit03(self):
        """
        NOC广告id在请求上行已卸载列表installedAds中，不下发广告给客户端
        :return:
        """
        print("第一步：打开NOC广告设置的开关")
        self.set_NOCAd_switch("on")
        print("第二步：取消屏蔽广东省深圳市")
        self.set_shield_proAndcity(1)
        print("第三步：设置NOC广告下发流量")
        self.set_flow()
        print("第四步：打开NOC广告拉活配置开关")
        self.set_wake_switch("on")
        print("第四步：拉取NOC广告")
        data = {
            "channelId": "CL88",
            "mid": "ssiddca98c74423142258b994801ed9f7794",
            "imei": "865625020257042",
            "version": "2.4.5",
            "subChannelId": "0001",
            "appid": "1139",
            "imsi": "355440079021985",
            "adList": [3, 5],
            "waitInstallAds": [],
            "installedAds": [],
            "uninstallAds": [44]
        }
        NOCAd_info = common.runaigaoapi(data, 'http://test.iad.zzay.net/ps/getNewNocAd.do')["data"]
        print(NOCAd_info)
        if len(NOCAd_info["adList"])==0:
            self.assertEqual(NOCAd_info["adList"], [])
            print("媒体已卸载的渠道用户，不再下发广告")

            self.assertEqual(NOCAd_info["wakeList"], [])
            print("媒体已卸载的渠道用户，不下拉活配置")
        else:
            adId_list = []
            wakeList = []
            for i in NOCAd_info["adList"]:
                adId_list.append(i["adId"])
            for i in NOCAd_info["wakeList"]:
                wakeList.append(i["adId"])

            self.assertNotIn(44, adId_list)
            print("媒体已卸载的渠道用户，不再下发广告")
            self.assertNotIn('44', wakeList)
            print("媒体已卸载的渠道用户，不下拉活配置")








