#测试一级展示量上限，展示超过设定的值3次，不下发广告
#Author: Zhang Jiaojiao
# -*- coding: utf-8 -*-

import unittest
import paramunittest
import readConfig as readConfig
import os
import time
import datetime
from common import Log as Log
from common import common
from time import localtime
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


@paramunittest.parametrized(adx_xls[12])
class LimitDisplay(unittest.TestCase):
    def setParameters(self, case_name, method, header, url, cursor, result, return_result, count, sql):
        """
        set params
        :param case_name:
        :param method:
        :param header:
        :param url:
        :param cursor
        :param result:
        :param return_result:
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
        self.return_result = str(return_result)
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
        self.sql = "update pub_app_ad_dsp_config SET show_cap=0 where dsp_app_id=176 and pub_app_ad_id=1073"
        dbresult = configDB.mysqlDB("113.31.86.153", "zzmanager", "iadMOB-2013@0622)", 3306, "ssp", self.sql)

    def testLimitDisplay(self):
        """
        test body
        :return:
        """
        print("第一步：设置广告位’wt7zilsc‘的应用的展示量上限为3")
        self.setLimitDisplay()

        # set url
        url = adx_xls[12][3]
        print("第二步：设置url  "+self.url)

        # set headers
        header = localReadConfig.get_headers("header")
        header = {"header": str(header)}
        print(header)
        configHttp.set_headers(header)
        print("第三步：设置header等")

        # set params
        print("第四步：设置多次循环发送请求达到展示量的上限值")
        self.return_result = self.multisend()

        method = str(self.return_json.request)[int(str(self.return_json.request).find('['))+1:int(str(self.return_json.request).find(']'))]
        print("第五步：发送请求\n\t\t请求方法："+method)

        # check result
        self.checkResult()
        print("第六步：检查Http请求结果")

        self.checkPGdb()

    def multisend(self):
        """
        send multi request
        :return:
        """
        url = adx_xls[12][3]
        json_path = os.path.join(readConfig.proDir, "testFile", "json", "MockA.json")
        json = configHttp.load_json(json_path)

        # i = datetime.datetime.now()
        # while i.second > 30:
        #     time.sleep(5)
        #     i = datetime.datetime.now()
        #     print("curent second is ", i.second)

        self.count = 5
        while self.count > 0:
            time.sleep(60)
            self.return_json = requests.request("POST", url, json=json)
            self.info = self.return_json.json()
            print("return json is: ",self.return_json.json())

            if self.count > 2:
                time.sleep(60)
                adxBeaconUrl = self.info['ads'][0]['adxBeaconUrl']
                self.url = adxBeaconUrl + self.info['ads'][0]['callUrl3']['show'][1]['parameters']
                print("GET url is: ",self.url)
                self.code = requests.request('GET', self.url)
            self.count = self.count - 1
        return self.return_json

    def setLimitDisplay(self):
        #设置　非MockA的应用:今日头条-验证POST上报　为勾选状态，且设置一级展示量上限为３次
        self.sql = "update ssp.pub_app_ad_dsp SET open_is=0 where pub_app_ad_id=1073 and dsp_app_id not in (176)"
        dbresult = configDB.mysqlDB("113.31.86.153","zzmanager","iadMOB-2013@0622)",3306,"ssp", self.sql)
        self.sql = "update ssp.pub_app_ad_dsp SET open_is=1 where pub_app_ad_id=1073 and dsp_app_id=176"
        dbresult = configDB.mysqlDB("113.31.86.153", "zzmanager", "iadMOB-2013@0622)", 3306, "ssp", self.sql)
        # self.sql = 'update pub_app_ad set creative_id="145" where app_ad_id="wt7zilsc"'
        # dbresult = configDB.mysqlDB("113.31.86.153", "zzmanager", "iadMOB-2013@0622)", 3306, "ssp", self.sql)
        self.tim = time.strftime('%H', localtime())
        print("current time is ", self.tim)
        self.tim = self.tim + ":00,22:00"

        self.sql = "update pub_app_ad_dsp_config set ecpm=38,effective_time='%s' where pub_app_ad_id=1073 and dsp_app_id=176" % self.tim
        dbresult = configDB.mysqlDB("113.31.86.153", "zzmanager", "iadMOB-2013@0622)", 3306, "ssp", self.sql)

        self.sql = "update pub_app_ad_dsp_config SET show_cap=3 where dsp_app_id=176 and pub_app_ad_id=1073"
        dbresult = configDB.mysqlDB("113.31.86.153", "zzmanager", "iadMOB-2013@0622)", 3306, "ssp", self.sql)
        time.sleep(800)


    def checkResult(self):
        """
        check test result
        :return:
        """
        info = self.return_json.json()['statusCode']
        print("status code is ",info)
        self.assertEqual(info,5)


    def checkPGdb(self):
        """
        check postgre sql result
        :return:
        """
        time.sleep(3)
        configPG.connectPG("adxroot", "adxroot321", "65432","113.31.86.153", "adx_report")
        self.sql = "select to_dsp_request from stats where dsp_app_id='176' and ad_type='4' and ad_group_id='28'and ad_channel_id='677' and ad_customer_id='15158' and imp_type= '1' order by timestamp desc"
        self.cursor = configPG.executeSQL(self.sql)
        self.result = configPG.get_one(self.cursor)
        print("return result is",self.result)
        self.assertEqual(self.result[0], 0)


    def tearDown(self):
        """

        :return:
        """
        self.sql = "update pub_app_ad_dsp_config SET show_cap=0 where dsp_app_id=176 and pub_app_ad_id=1073"
        dbresult = configDB.mysqlDB("113.31.86.153", "zzmanager", "iadMOB-2013@0622)", 3306, "ssp", self.sql)

        self.sql = "update pub_app_ad_dsp_config set effective_time='0:00,24:00' where pub_app_ad_id=1073 and dsp_app_id=176"
        dbresult = configDB.mysqlDB("113.31.86.153", "zzmanager", "iadMOB-2013@0622)", 3306, "ssp", self.sql)
        print("测试结束，输出log完结\n\n")
