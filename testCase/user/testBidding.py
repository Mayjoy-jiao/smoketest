"""
测试S2S竞价
广告位：bzaddftc  设置竞价比例为100%

１.设置　勾选　MockA-自用　竞价价格(eCPM)：40   ----MockA的不判断底价
２.设置　勾选　测试RTB（自用）　　　　竞价底价:33　　　　　　　　---程序设定返回价钱为33
３.设置　勾选　自动化测试－S2S脚本测试　竞价价格(eCPM)：35
RTB超过底价的和PDB的Dsp做竞价，挑选最高的　自动化测试－S2S脚本测试，下发广告
Author: Zhang Jiaojiao
date: 2019-06-27

"""
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
from common import configDB as ConfigDB

import requests

adx_xls = common.get_xls("adx.xlsx", "adx")
localReadConfig = readConfig.ReadConfig()
configHttp = ConfigHttp.ConfigHttp()
configPG = ConfigPG.PGDB()
configDB = ConfigDB.MyDB()
proDir = readConfig.proDir
info = {}


@paramunittest.parametrized(adx_xls[13])
class Bidding(unittest.TestCase):
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
        print("第一步：设置广告位bzaddftc竞价相关的配置值")
        self.Bidingseting()


        url = adx_xls[13][3]
        print("第二步：设置url  "+self.url)

        # set headers
        header = localReadConfig.get_headers("header")
        header = {"header": str(header)}
        print(header)
        configHttp.set_headers(header)
        print("第三步：设置header等")

        # set params
        json_path = os.path.join(readConfig.proDir, "testFile","json","bidding.json")
        json = configHttp.load_json(json_path)
        print("第四步：设置发送请求的参数")

        self.return_json = requests.request("POST", url, json = json)
        print(self.return_json.json())

        method = str(self.return_json.request)[int(str(self.return_json.request).find('['))+1:int(str(self.return_json.request).find(']'))]
        print("第五步：发送请求\n\t\t请求方法："+method)

        self.checkResult()
        print("第六步：检查Http请求结果")



    def Bidingseting(self):
        """
        勾选　MockA-自用　竞价价格(eCPM)：40   竞价底价:40
        :return:
        """
        sql = "update pub_app_ad set s2s_sort_rate=100 where app_ad_id='bzaddftc'"
        dbresult = configDB.mysqlDB( "113.31.86.153", "zzmanager", "iadMOB-2013@0622)", 3306, "ssp", sql)
        # self.sql = "update pub_app_ad_dsp set open_is=1 , floor_price=40 where dsp_app_id=115 and pub_app_ad_id=1072"
        # dbresult = configDB.mysqlDB( "113.31.86.153", "zzmanager", "iadMOB-2013@0622)", 3306, "ssp", self.sql)
        self.sql = "update pub_app_ad_dsp_config set ecpm=40,effective_time='0:00,24:00' where pub_app_ad_id=1072 and dsp_app_id=115"
        dbresult = configDB.mysqlDB( "113.31.86.153", "zzmanager", "iadMOB-2013@0622)", 3306, "ssp", self.sql)


        self.sql = "update pub_app_ad_dsp set open_is=1 , floor_price=35 where dsp_app_id=139 and pub_app_ad_id=1072"
        dbresult = configDB.mysqlDB("113.31.86.153", "zzmanager", "iadMOB-2013@0622)", 3306, "ssp", self.sql)


        self.sql = "update pub_app_ad_dsp set open_is=1 where dsp_app_id in (148,115) and pub_app_ad_id=1072"
        dbresult = configDB.mysqlDB("113.31.86.153", "zzmanager", "iadMOB-2013@0622)", 3306, "ssp", self.sql)
        self.sql = "update pub_app_ad_dsp_config set ecpm=35,effective_time='0:00,24:00' where pub_app_ad_id=1072 and dsp_app_id=148"
        dbresult = configDB.mysqlDB("113.31.86.153", "zzmanager", "iadMOB-2013@0622)", 3306, "ssp", self.sql)

        #其他的为非勾选状态
        self.sql = "update pub_app_ad_dsp set open_is=0 where dsp_app_id not in (148,115,139) and pub_app_ad_id=1072"
        dbresult = configDB.mysqlDB("113.31.86.153", "zzmanager", "iadMOB-2013@0622)", 3306, "ssp", self.sql)

        time.sleep(660)


    def checkResult(self):
        """
        check test result
        :return:
        """
        self.info = self.return_json.json()
        # show return message
        common.show_return_msg(self.return_json)

        self.assertEqual(self.info['ads'][0]['configId'],'adxDsp_115_3')


    def tearDown(self):
        """

        :return:
        """
        self.sql = "update pub_app_ad_dsp set floor_price=0 where dsp_app_id in (115,139) and pub_app_ad_id=1072"
        dbresult = configDB.mysqlDB("113.31.86.153", "zzmanager", "iadMOB-2013@0622)", 3306, "ssp", self.sql)

        sql = "update pub_app_ad_dsp_config set ecpm=0,effective_time='0:00,24:00' where pub_app_ad_id =1072 and dsp_app_id in (148,115)"
        dbresult = configDB.mysqlDB("113.31.86.153", "zzmanager", "iadMOB-2013@0622)", 3306, "ssp", sql)

        print("测试结束，输出log完结\n\n")
