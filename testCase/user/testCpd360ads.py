# -*- encoding = utf-8 -*-
import os
import unittest
import requests
import paramunittest
import readConfig as readConfig
from common import common
from common import Log as Log
from common import configHttp as ConfigHttp
from common import configPG as ConfigPG

configHttp = ConfigHttp.ConfigHttp()
configPG = ConfigPG.PGDB()
localReadConfig = readConfig.ReadConfig()

adx_xls = common.get_xls("adx.xlsx", "adx")

@paramunittest.parametrized(adx_xls[6])
class Cpd360ads(unittest.TestCase):
    def setParameters(self, case_name, header, sql, url, cursor, cpd360ads1, result, code, cpd360ads2):
        """set parames
        :param case_name:
        :param header
        :param mothod:
        :param url:
        :param result
        :param code:
        :param msg:
        :param return_code
        :return
        """
        self.case_name = str(case_name)
        self.header = str(header)
        # self.method = str(method)
        # self.database = str(database)
        self.sql = str(sql)
        self.url = str(url)
        self.cursor = str(cursor)
        self.cpd360ads1 = str(cpd360ads1)
        self.result = str(result)
        self.code = str(code)
        self.cpd360ads2 = str(cpd360ads2)
        # self.return_code = str(return_code)


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

    def testCpd(self):
        """

        test body
        :return:
        """
        # set url
        try:
            self.url = adx_xls[7][3]
            print(self.url)
        except IndexError:
            pass
        print("第一步获取有360广告的列表"+ self.url)
        self.header = localReadConfig.get_headers("header")
        self.header = {"header": str(self.header)}
        print(self.header)
        configHttp.set_headers(self.header)

        #get request

        json_path = os.path.join(readConfig.proDir, "testFile", "json", "cpd360ads.json")
        json = configHttp.load_json(json_path)

        # self.return_json = requests.request("POST", self.url, json=json)
        # print(self.return_json.json())
        # method = str(self.return_json.request)[int(str(self.return_json.request).find('[')) + 1:int(str(self.return_json.request).find(']'))]
        # print("请求广告的\n\t\t请求方法：" + method)
        # self.cpd360ads1 = self.return_json.json()['ads'][0]['pkgName']
        # self.cpd360ads2 = self.return_json.json()['ads'][1]['pkgName']
        self.cpd360ads1 ="com.wuba"
        # get return status code
        self.code = str(self.code)[int(str(self.code).find('[')) + 1: int(str(self.code).find(']'))]

        print("360有广告的包分别有",self.cpd360ads1)
        # print("\n\t\t\t",self.cpd360ads2)
        self.dayflow()

        print("第三步设置广告当天的流量值-安装流量:100　打开流量:100 下发流量:100 展示流量：100\n")


    def tearDown(self):
        """

        :return:
        """
        if self.result == 0:
            pass
        else:
            pass
        print("测试结束，输出log完结\n\n")


    def getadid(self):
        """
        get ad id of cpd
        :return:
        """
        configPG.connectPG("root","aszx","5432","192.168.0.66","cpd")
        # self.sql = "update cpd_app_ad_config SET impression_priority='5'where status='1' and impression_priority='10'"
        # self.cursor = configPG.executeSQL(self.sql)

        self.sql = "select id from public.cpd_ad_warehouse where cpd_app_id='42' and ad_pkg='%s'" % self.cpd360ads1
        self.cursor = configPG.executeSQL(self.sql)
        self.result = configPG.get_one(self.cursor)
        cpd_ad_id_1 = self.result[0]
        self.sql = "update public.cpd_app_ad_config SET status='1' ,impression_priority='10' where cpd_ad_id='%s'" % cpd_ad_id_1
        self.cursor = configPG.executeSQL(self.sql)

        self.sql = "update public.cpd_app_ad_config SET status='0' where cpd_ad_id not in ('%s')" % cpd_ad_id_1
        self.cursor = configPG.executeSQL(self.sql)

        # self.sql = "select id from public.cpd_ad_warehouse where cpd_app_id='42' and ad_pkg='%s'" % self.cpd360ads2
        # self.cursor = configPG.executeSQL(self.sql)
        # self.result = configPG.get_one(self.cursor)
        # cpd_ad_id_2 = self.result[0]
        # self.sql = "update public.cpd_app_ad_config SET status='1', impression_priority='10' where cpd_ad_id='%s'" % cpd_ad_id_2
        # self.cursor = configPG.executeSQL(self.sql)
        return cpd_ad_id_1


    def dayflow(self):
        """
        test today's flow of issued　install and so on
        :return:
        """
        configPG.connectPG("root","aszx","5432","192.168.0.66","cpd")
        self.sql = "select current_date"
        self.cursor = configPG.executeSQL(self.sql)
        current_date = configPG.get_one(self.cursor)[0]

        cpd_ad_id_1 = self.getadid()
        # cpd_ad_id_2 = self.getadid()[1]
        print("第二步查询广告库的id,并将其设置为运行状态\n")
        print("360 cpd_ad _id_1 is ",cpd_ad_id_1)
        # print("360 cpd_ad_id_2 is ",cpd_ad_id_2)
        self.sql = "select id from cpd_ad_traffic_config where ts='%s'and cpd_ad_id='%s'" % (current_date, cpd_ad_id_1)
        self.cursor = configPG.executeSQL(self.sql)
        self.result = configPG.get_one(self.cursor)
        #
        # if self.result:
        #     print("今天360cpd已有流量的包：", self.cpd360ads1)
        # else:
        #     self.sql = "select id from cpd_ad_traffic_config where cpd_ad_id='%s'" % cpd_ad_id_1
        #     self.cursor = configPG.executeSQL(self.sql)
        #     id_1 = configPG.get_one(self.cursor)[0]
        #
        #     self.sql = "update public.cpd_ad_traffic_config SET issueds='100', impressions='100', installs='100', opens='100', ts='%s' where id='%s'" % (
        #     current_date, id_1)
        #     self.cursor = configPG.executeSQL(self.sql)
        self.sql = "select id from cpd_ad_traffic_config where cpd_ad_id='%s'" % cpd_ad_id_1
        id_1 = configPG.get_one(self.cursor)
        self.sql = "update public.cpd_ad_traffic_config SET issueds='100', impressions='100', installs='100', opens='100', ts='%s' where id='%s'" % (
            current_date, "2876514")
        self.cursor = configPG.executeSQL(self.sql)

        # self.sql = "select id from cpd_ad_traffic_config where ts='%s'and cpd_ad_id='%s'" % (current_date, cpd_ad_id_2)
        # self.cursor = configPG.executeSQL(self.sql)
        # self.result = configPG.get_one(self.cursor)
        #
        # if self.result:
        #     print("今天360cpd已有流量的包：", self.cpd360ads2)
        # else:
        #     self.sql = "select id from cpd_ad_traffic_config where cpd_ad_id='%s'" % cpd_ad_id_2
        #     self.cursor = configPG.executeSQL(self.sql)
        #     id_2 = configPG.get_one(self.cursor)[0]
        #
        #     self.sql = "update public.cpd_ad_traffic_config SET issueds='100', impressions='100', installs='100', opens='100', ts='%s' where id='%s'" % (
        #     current_date, id_2)
        #     self.cursor = configPG.executeSQL(self.sql)
