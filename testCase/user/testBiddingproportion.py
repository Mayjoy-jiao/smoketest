# -*- coding: utf-8 -*-
import unittest
import paramunittest
import readConfig as readConfig
import os
import time
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
class Bidding_Proportion(unittest.TestCase):
    def setParameters(self, case_name, method, header, url, cursor, result, code, count, sql):
        """
        set params
        :param case_name:
        :param method:
        :param header:
        :param url:
        :param cursor
        :param result:
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
        self.result = str(result)
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

    def testBid(self):
        """
        test Bidding main test case
        :return:
        """
        url = adx_xls[0][3]
        print("第一步：设置url  "+self.url)

        # set headers
        header = localReadConfig.get_headers("header")
        header = {"header": str(header)}
        print(header)
        configHttp.set_headers(header)
        print("第二步：设置header等")

        # set params
        json_path = os.path.join(readConfig.proDir, "testFile","json","Biddingproportion.json")
        json = configHttp.load_json(json_path)
        print("第三步：设置发送请求的参数")

        self.return_json = requests.request("POST", url, json = json)
        print(self.return_json.json())

        method = str(self.return_json.request)[int(str(self.return_json.request).find('['))+1:int(str(self.return_json.request).find(']'))]
        print("第四步：发送请求\n\t\t请求方法："+method)

        self.checkResult()
        print("第五步：检查Http请求结果")


    def checkResult(self):
        """
        check test result
        :return:
        """
        url = adx_xls[0][3]
        json_path = os.path.join(readConfig.proDir, "testFile", "json", "Biddingproportion.json")
        json = configHttp.load_json(json_path)

        self.count = 0
        while self.count >= 0:
            self.return_json = requests.request("POST", url, json=json)
            self.info = self.return_json.json()

            if self.info['ads'][0]['configId'] == 'adxDsp_181_3':
                self.return_json = requests.request("POST", url, json=json)
                self.info = self.return_json.json()
                if self.info['ads'][0]['configId'] == 'adxDsp_172_3':
                    self.count = self.count - 1
                else:
                    self.return_json = requests.request("POST", url, json=json)
                    self.info = self.return_json.json()

            elif self.info['ads'][0]['configId'] == 'adxDsp_172_3':
                self.return_json = requests.request("POST", url, json=json)
                self.info = self.return_json.json()

                if self.info['ads'][0]['configId'] == 'adxDsp_181_3':
                    self.count = self.count - 1
                else:
                    self.return_json = requests.request("POST", url, json=json)
                    self.info = self.return_json.json()

        print(self.count)
        self.assertLessEqual(self.count,0,"test Biddingproportion is test failed")