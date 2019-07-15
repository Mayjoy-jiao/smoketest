# -*- coding: utf-8 -*-

import unittest
import paramunittest
import readConfig as readConfig
import os
import time
import requests
import pymysql
from common import Log as Log
from common import common
from common import configHttp as ConfigHttp
from common import configDB as ConfigDB


adx_xls = common.get_xls("adx.xlsx", "adx")
localReadConfig = readConfig.ReadConfig()
configHttp = ConfigHttp.ConfigHttp()
configDB = ConfigDB.MyDB
proDir = readConfig.proDir
info = {}

@paramunittest.parametrized(adx_xls[9])
class NonMockAwithoutAds(unittest.TestCase):
    def setParameters(self, case_name, method, header, url, cursor, result, code, msg, sql):
        """
        set params
        :param case_name:
        :param method:
        :param header:
        :param url:
        :param cursor
        :param result:
        :param code:
        :param msg:
        :param sql:
        :return:
        """
        self.case_name = str(case_name)
        self.method = str(method)
        self.header = str(header)
        self.url = str(url)
        self.cursor = str(cursor)
        self.result = str(result)
        self.code = int(code)
        self.msg = int(msg)
        self.sql = str(sql)
        self.info = None


    def description(self):
        """
        test report description
        :return:
        """
        self.case_name

    def setUp(self):
        """

        :return:
        """
        self.log = Log.MyLog.get_log()
        self.logger = self.log.get_logger()
        print(self.case_name+"测试开始前准备")

    def testNonMockAwithoutAds(self):
        """
        test body: test more than 5min click url,vaild_type = 5
        :return:
        """
        #设置广告位　wt7zilsc　勾选的为非MockA的应用，没有勾选测试广告

        print("第一步：设置广告位’wt7zilsc‘的为非MockA的应用：MockA-自用")
        self.setNonMockA()

        # set url
        url = adx_xls[8][3]
        print("第二步：设置url  "+self.url)

        # set headers
        header = localReadConfig.get_headers("header")
        header = {"header": str(header)}
        print(header)
        configHttp.set_headers(header)
        print("第三步：设置header等")

        # set params
        json_path = os.path.join(readConfig.proDir, "testFile","json","MockA.json")
        json = configHttp.load_json(json_path)
        print("第四步：设置发送请求的参数")

        self.return_json = requests.request("POST", url, json = json)
        print(self.return_json.json())

        method = str(self.return_json.request)[int(str(self.return_json.request).find('['))+1:int(str(self.return_json.request).find(']'))]
        print("第五步：发送请求\n\t\t请求方法："+method)

        # check result
        print("第六步：检查Http请求结果")
        self.checkResult()


    def checkResult(self):
        """
        check test result
        :return:
        """
        self.info = self.return_json.json()
        # show return message
        common.show_return_msg(self.return_json)
        result = self.assertEqual(self.info['ads'][0]['configId'],'adxDsp_176_4')



    def setNonMockA(self):
        time.sleep(3)
        #设置　非MockA的应用:今日头条-验证POST上报　为勾选状态，且没有勾选测试广告
        self.sql = "update ssp.pub_app_ad_dsp SET open_is=0 where pub_app_ad_id=1073 and dsp_app_id not in (176)"
        dbresult = configDB.mysqlDB(self,"113.31.86.153","zzmanager","iadMOB-2013@0622)",3306,"ssp", self.sql)
        self.sql = "update ssp.pub_app_ad_dsp SET open_is=1 where pub_app_ad_id=1073 and dsp_app_id=176"
        dbresult = configDB.mysqlDB(self, "113.31.86.153", "zzmanager", "iadMOB-2013@0622)", 3306, "ssp", self.sql)
        self.sql = 'update pub_app_ad set creative_id="" where app_ad_id="wt7zilsc"'
        dbresult = configDB.mysqlDB(self, "113.31.86.153", "zzmanager", "iadMOB-2013@0622)", 3306, "ssp", self.sql)
        time.sleep(660)

    def tearDown(self):
        """

        :return:
        """
        print("测试结束，输出log完结\n\n")