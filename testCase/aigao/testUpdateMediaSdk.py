"""
测试媒体包升级

用例运行前,后台页面设置如下:
1.[SDK广告管理_媒体管理]选择:联调媒体包

2.确保联调媒体包的媒体包管理中各控制版本号有对应的正式运行的媒体包

Author: Sun Yaping
date: 2019-08-21

"""

# -*- coding: utf-8 -*-
import time
import unittest
import paramunittest
from common import common
from common.Log import MyLog
import readConfig as readConfig
from common import configHttp as configHttp
from common import configDB as configDB
import requests

aigao_xls = common.get_xls("aigao.xlsx", "aigao")
localReadConfig = readConfig.ReadConfig()
localConfigHttp = configHttp.ConfigHttp()
ConfigDB = configDB.MyDB()


@paramunittest.parametrized(aigao_xls[2])
class UpdateMediaSdk(unittest.TestCase):
    def setParameters(self, case_name, url, method, token, goods_id, result, code, msg):
        """
        set params
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
        """

        :return:
        """
        self.case_name

    def setUp(self):
        """

        :return:
        """
        self.log = MyLog.get_log()
        self.logger = self.log.get_logger()

    def postdata(self, controlversion, mediapkgversion, version, androidversion):
        """
        媒体包升级接口
        :param controlversion: 媒体包控制版本号
        :param mediapkgversion: 媒体包版本号
        :param version: 爱告SDK协议版本号
        :param androidversion: 客户端安卓版本号
        :return:
        """
        data = {
            "appid": "1139",
            "channelId": "suny999",
            "subChannelId": "1",
            "mid": "ssiddca98c74423142258b994801ed9f1111",
            "imei": "865625020257042",
            "imsi": "460011207707575",
            "controlVersion": controlversion,
            "mediaPkgName": "com.android.test",
            "mediaPkgVersion": mediapkgversion,
            "version": str(version),
            "androidVersion": androidversion
        }
        # url = 'http://test.iad.zzay.net/ps/updateMediaSdk.do'
        # res = common.runaigaoapi_1(data, url)
        return data

    def checkResult(self, req_controlversion, req_androidversion, updatemediasdk_res):
        """
        check test result
        :return:
        """
        # 数据库查询当前正式运行的包名为'com.android.test'的控制版本号为3的媒体包版本号最高的媒体包的URL和MD5
        if req_androidversion == 23:
            self.sql = "select media_pkg_version,download_pkg,MD5 from sdk_media_pkg where control_version = '%s' and state = '3' and media_pkg_name = 'com.android.test' AND android_version = '23' order by CAST(media_pkg_version as SIGNED) desc limit 1" % (
                req_controlversion)
        else:
            self.sql = "select media_pkg_version,download_pkg,MD5 from sdk_media_pkg where control_version = '%s' and state = '3' and media_pkg_name = 'com.android.test' AND android_version = '19,20,21,22,24,25,26,27,28,29' order by CAST(media_pkg_version as SIGNED) desc limit 1" % (
                req_controlversion)
        dbresult = ConfigDB.mysqlDB("113.31.86.153", "zzmanager", "iadMOB-2013@0622)", 3306, "iadsupport", self.sql)
        print(f"当前正式运行的包名为'com.android.test'的控制版本号为{req_controlversion}的支持安卓{req_androidversion}的最高媒体包版本号为: {dbresult[0]}")
        time.sleep(3)

        current_downloadurl = updatemediasdk_res['data']['url']
        current_md5 = updatemediasdk_res['data']['md5']
        self.assertEqual(dbresult[1], current_downloadurl)
        self.assertEqual(dbresult[2], current_md5)

    # @unittest.skip("该用例暂不执行")
    def testControlVersion1_firsttime(self):
        """
        用户首次拉取控制版本号1的媒体包
        :return:
        """
        # set url
        self.url = aigao_xls[2][3]
        print("第一步：设置url:\n" + self.url)
        # set post data
        print("第二步：设置请求上行:\n")
        data = self.postdata(1, 0, "1.0.6", 23)
        print("媒体包升级请求上行:\n", data)
        # 请求接口
        # common.runJVM()
        res = common.runaigaoapi(data, self.url)
        print("媒体包升级请求下行:\n", res)
        # check result
        self.checkResult(1, 23, res)

    # @unittest.skip("该用例暂不执行")
    def testControlVersion1_notfirsttime(self):
        """
        用户非首次拉取控制版本号1的媒体包
        :return:
        """
        # set url
        self.url = aigao_xls[2][3]
        print("第一步：设置url:\n" + self.url)
        # set post data
        print("第二步：设置请求上行:\n")
        data = self.postdata(1, 45, "1.0.6", 24)
        print("媒体包升级请求上行:\n", data)
        # 请求接口
        res = common.runaigaoapi(data, self.url)
        print("媒体包升级请求下行:\n", res)
        # check result
        self.checkResult(1, 24, res)

    # @unittest.skip("该用例暂不执行")
    def testControlVersion2_firsttime(self):
        """
        用户首次拉取控制版本号2的媒体包
        :return:
        """
        # set url
        self.url = aigao_xls[2][3]
        print("第一步：设置url:\n" + self.url)
        # set post data
        print("第二步：设置请求上行:\n")
        data = self.postdata(2, 0, "1.0.7", 23)
        print("媒体包升级请求上行:\n", data)
        # 请求接口
        res = common.runaigaoapi(data, self.url)
        print("媒体包升级请求下行:\n", res)
        # check result
        self.checkResult(2, 23, res)

    # @unittest.skip("该用例暂不执行")
    def testControlVersion2_notfirsttime(self):
        """
        用户非首次拉取控制版本号2的媒体包
        :return:
        """
        # set url
        self.url = aigao_xls[2][3]
        print("第一步：设置url:\n" + self.url)
        # set post data
        print("第二步：设置请求上行:\n")
        data = self.postdata(2, 19082100, "1.0.7", 25)
        print("媒体包升级请求上行:\n", data)
        # 请求接口
        res = common.runaigaoapi(data, self.url)
        print("媒体包升级请求下行:\n", res)
        # check result
        self.checkResult(2, 25, res)

    # @unittest.skip("该用例暂不执行")
    def testControlVersion3_firsttime(self):
        """
        用户首次拉取控制版本号3的媒体包
        :return:
        """
        # set url
        self.url = aigao_xls[2][3]
        print("第一步：设置url:\n" + self.url)
        # set post data
        print("第二步：设置请求上行:\n")
        data = self.postdata(3, 0, "1.0.7", 23)
        print("媒体包升级请求上行:\n", data)
        # 请求接口
        res = common.runaigaoapi(data, self.url)
        print("媒体包升级请求下行:\n", res)
        # check result
        self.checkResult(3, 23, res)

    # @unittest.skip("该用例暂不执行")
    def testControlVersion3_notfirsttime(self):
        """
        用户非首次拉取控制版本号3的媒体包
        :return:
        """
        # set url
        self.url = aigao_xls[2][3]
        print("第一步：设置url:\n" + self.url)
        # set post data
        print("第二步：设置请求上行:\n")
        data = self.postdata(3, 19083000, "1.0.7", 29)
        print("媒体包升级请求上行:\n", data)
        # 请求接口
        res = common.runaigaoapi(data, self.url)
        print("媒体包升级请求下行:\n", res)
        # check result
        self.checkResult(3, 29, res)

    # @unittest.skip("该用例暂不执行")
    def testControlVersion4_firsttime(self):
        """
        用户首次拉取控制版本号4的媒体包
        :return:
        """
        # set url
        self.url = aigao_xls[2][3]
        print("第一步：设置url:\n" + self.url)
        # set post data
        print("第二步：设置请求上行:\n")
        data = self.postdata(4, 0, "1.0.7", 23)
        print("媒体包升级请求上行:\n", data)
        # 请求接口
        res = common.runaigaoapi(data, self.url)
        print("媒体包升级请求下行:\n", res)
        # check result
        self.checkResult(4, 23, res)

    # @unittest.skip("该用例暂不执行")
    def testControlVersion4_notfirsttime(self):
        """
        用户非首次拉取控制版本号4的媒体包
        :return:
        """
        # set url
        self.url = aigao_xls[2][3]
        print("第一步：设置url:\n" + self.url)
        # set post data
        print("第二步：设置请求上行:\n")
        data = self.postdata(4, 19090300, "1.0.7", 28)
        print("媒体包升级请求上行:\n", data)
        # 请求接口
        res = common.runaigaoapi(data, self.url)
        print("媒体包升级请求下行:\n", res)
        # check result
        self.checkResult(4, 28, res)

    def tearDown(self):
        """

        :return:
        """
        print("测试结束，输出log完结\n\n")
