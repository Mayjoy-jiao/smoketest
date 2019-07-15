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
class TheSecond_issued(unittest.TestCase):
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
        self.msg = str(msg)
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

    def checkResult(self):
        """
        check test result
        :return:
        """
        self.info = self.return_json.json()
        # show return message
        common.show_return_msg(self.return_json)

        if self.result == '0':
            self.assertEqual(self.info["statusCode"], self.code)
            self.assertEqual(self.info['ads'][0]['configId'],'adxDsp_174_1')

        if self.result == '1':
            self.assertEqual(self.info['statusCode'], self.code)
            self.assertEqual(self.info['ads'][0]['configId'], 'adxDsp_174_1')

        self.url = self.info['ads'][0]['callUrl']['show'][0]
        self.code = requests.request('GET', self.url)

        self.url = self.info['ads'][0]['callUrl']['click'][0]
        self.code = requests.request('GET', self.url)

        time.sleep(10)
        url = adx_xls[1][3]
        print("url is ", url)
        self.return_json = requests.request("POST", url)
        print(self.return_json.json())
        self.info = self.return_json.json()

        time.sleep(10)
        self.assertEqual(self.info['adxDspSim'][0]['configId'], 'adxDsp_174_1')
        self.assertEqual(self.info['adxDspSim'][0]['count'], 1)


    def testThesecond_issued(self):
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
        json_path = os.path.join(readConfig.proDir, "testFile","json","Thesecondissued.json")
        json = configHttp.load_json(json_path)
        print("第三步：设置发送请求的参数")

        self.return_json = requests.request("POST", url, json = json)
        print(self.return_json.json())

        method = str(self.return_json.request)[int(str(self.return_json.request).find('['))+1:int(str(self.return_json.request).find(']'))]
        print("第四步：发送请求\n\t\t请求方法："+method)

        # check result
        self.checkResult()
        print("第五步：检查Http请求结果")

        print("第六步：校验广告位模拟量正确性")
        # self.checkPGdb()


    def tearDown(self):
        """

        :return:
        """
        # info = self.info
        # if info['statusCode'] == 0:
        #     pass
        # else:
        #     pass
        print("测试结束，输出log完结\n\n")

    def checkResultAll(self):
        """
        check test result
        :return:
        """
        if self.code == '204':
            self.assertEqual(self.code, '204')
            print("Http request code is 204")


