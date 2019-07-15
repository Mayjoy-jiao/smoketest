# -*- coding: utf-8 -*-

import unittest
import paramunittest
import readConfig as readConfig
import os
import time
import requests
from common import Log as Log
from common import common
from common import configHttp as ConfigHttp
from common import configPG as ConfigPG


adx_xls = common.get_xls("adx.xlsx", "adx")
localReadConfig = readConfig.ReadConfig()
configHttp = ConfigHttp.ConfigHttp()
configPG = ConfigPG.PGDB()
proDir = readConfig.proDir
info = {}

@paramunittest.parametrized(adx_xls[0])
class Expiry_click(unittest.TestCase):
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

    def testExpiryclick(self):
        """
        test body: test more than 5min click url,vaild_type = 5
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
        json_path = os.path.join(readConfig.proDir, "testFile","json","s2s1.json")
        json = configHttp.load_json(json_path)
        print("第三步：设置发送请求的参数")

        self.return_json = requests.request("POST", url, json = json)
        print(self.return_json.json())

        method = str(self.return_json.request)[int(str(self.return_json.request).find('['))+1:int(str(self.return_json.request).find(']'))]
        print("第四步：发送请求\n\t\t请求方法："+method)

        # check result
        self.checkResult()
        print("第五步：检查Http请求结果")

        print("第六步：校验PGdb数据")
        self.checkPGdb()

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
            self.assertEqual(self.info['ads'][0]['configId'],'adxDsp_148_2')

        if self.result == '1':
            self.assertEqual(self.info['statusCode'], self.code)
            self.assertEqual(self.info['ads'][0]['configId'], 'adxDsp_148_2')

        adxBeaconUrl = self.info['ads'][0]['adxBeaconUrl']
        print("1111111111111111111",adxBeaconUrl)
        self.url = adxBeaconUrl + self.info['ads'][0]['callUrl3']['show'][0]['parameters']
        self.code = requests.request('GET', self.url)

        self.url = adxBeaconUrl+ self.info['ads'][0]['callUrl3']['click'][1]['parameters']
        time.sleep(360)
        self.code = requests.request('GET', self.url)

    def checkPGdb(self):
        #去掉了异常节点
        time.sleep(3)
        configPG.connectPG("adxroot", "adxroot321", "65432","113.31.86.153", "adx_report")
        self.sql = "select valid_type,ex_click,ex_download_click from public.stats where dsp_app_id='148'and ad_type='2' and ad_group_id='28'and ad_channel_id='677' and ad_customer_id='15158' and imp_type= '1' order by timestamp desc"
        self.cursor = configPG.executeSQL(self.sql)
        self.result = configPG.get_one(self.cursor)
        print(self.result)

        if self.result[0] == 0:
            self.assertEqual(self.result[0], 0)
            print("PGdb expiry click is test seccussfully!")
        else:
            self.assertEqual(self.result[0], 0)
            print("PGdb expiry click test failed")

        if self.result[1] == 1:
            self.assertEqual(self.result[1], 0)
            print("PGdb expiry click is test seccussfully!")
        else:
            self.assertEqual(self.result[1], 0)
            print("PGdb expiry click test failed")

        if self.result[2] == 1:
            self.assertEqual(self.result[2], 0)
            print("PGdb expiry click download_start is test seccussfully!")
        else:
            self.assertEqual(self.result[2], 0)
            print("PGdb expiry click download_start test failed")

    def tearDown(self):
        """

        :return:
        """
        info = self.info
        if info['statusCode'] == 0:
            pass
        else:
            pass
        print("测试结束，输出log完结\n\n")