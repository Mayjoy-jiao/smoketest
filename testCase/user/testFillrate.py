# -*- coding: utf-8 -*-

import unittest
import paramunittest
import readConfig as readConfig
import os
import time
import datetime
from common import Log as Log
from common import common
from common import configHttp as ConfigHttp
from common import configPG as ConfigPG

import requests

adx_xls = common.get_xls("adx.xlsx", "adx")
localReadConfig = readConfig.ReadConfig()
configHttp = ConfigHttp.ConfigHttp()
configPG = ConfigPG.PGDB()
proDir = readConfig.proDir
info = {}


@paramunittest.parametrized(adx_xls[0])
class FillRate(unittest.TestCase):
    def setParameters(self, case_name, method, header, url, cursor, now, code, count, sql):
        """
        set params
        :param case_name:
        :param method:
        :param header:
        :param url:
        :param cursor
        :param now:
        :param code:
        :param count:
        :param sql:
        :return:
        """
        self.case_name = str(case_name)
        self.method = str(method)
        self.header = str(header)
        self.url = str(url)
        self.cursor = str(cursor)
        self.now = str(now)
        self.code = int(code)
        self.count = int(count)
        self.sql = str(sql)
        self.info = None
        global reqId



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

    def testFillRate(self):
        """
        test body
        :return:
        """
        # set url
        url = adx_xls[0][3]
        print("第一步：设置url  "+self.url)

        # set headers
        header = localReadConfig.get_headers("header")
        header = {"header": str(header)}
        print(header)
        configHttp.set_headers(header)
        print("第二步：设置header等")

        # set params
        print("第三步：设置多次循环发送请求并且1min后重复循环发送请求")
        self.multisend()
        time.sleep(60)
        self.multisend()

        method = str(self.return_json.request)[int(str(self.return_json.request).find('['))+1:int(str(self.return_json.request).find(']'))]
        print("第四步：发送请求\n\t\t请求方法："+method)

        # check result
        self.checkResult()
        print("第五步：检查Http请求结果")

        print("第六步：校验PGdb数据")
        self.checkPGdb()

    def multisend(self):
        """
        send multi request
        :return:
        """
        url = adx_xls[0][3]
        json_path = os.path.join(readConfig.proDir, "testFile", "json", "Fillrate.json")
        json = configHttp.load_json(json_path)
        i = datetime.datetime.now()
        print("curent second is ",i.second)
        while i.second > 30:
            time.sleep(5)
            i = datetime.datetime.now()
            print("curent second is ", i.second)

        self.count = 5

        while self.count > 0:
            self.return_json = requests.request("POST", url, json=json)
            time.sleep(2)
            print(self.return_json.json())
            self.count = self.count - 1


    def tearDown(self): 
        """

        :return:
        """
        if self.result[0] == 0:
            pass
        else:
            pass
        print("测试结束，输出log完结\n\n")


    def checkResult(self):
        """
        check test result
        :return:
        """
        if self.code == '200':
            self.assertEqual(self.code, '200')



    def checkPGdb(self):
        """
        check postgre sql result
        :return:
        """
        time.sleep(40)
        configPG.connectPG("adx_report")
        self.sql = "select to_dsp_request,timestamp from stats where dsp_app_id = '172' and ad_type='1' order by timestamp desc"
        self.cursor = configPG.executeSQL(self.sql)
        self.result = configPG.get_one(self.cursor)
        print(self.result)

        if self.result[0] == 0:
            self.assertEqual(self.result[0], 2)
            print("PGdb to_dsp_request is test seccussfully!")
        else:
            self.assertEqual(self.result[0], 2)
            print("PGdb to_dsp_request test failed")













