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
class C2s2(unittest.TestCase):
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

    def checkPGdb(self):
        time.sleep(2)
        configPG.connectPG("root","aszx","5432","192.168.0.66","adx_report")
        self.sql = "select publisher_request from public.stats where ad_group_id='46'and ad_channel_id='645' and ad_customer_id='14257' and dsp_app_id='0' order by timestamp desc"
        self.cursor = configPG.executeSQL(self.sql)
        self.result = configPG.get_one(self.cursor)
        print("1111111111111111111111",self.result)

        if self.result[0] == 1:
            self.assertEqual(self.result[0], 1)
            print("PGdb adx_issued is test seccussfully!")
        else:
            self.assertEqual(self.result[0], 1)
            print("PGdb adx_issued test failed")

        self.sql = "select adx_issued,to_dsp_request from public.stats where dsp_app_id='210'and ad_type='4' and ad_group_id='46'and ad_channel_id='645' and ad_customer_id='14257' order by timestamp DESC"
        self.cursor = configPG.executeSQL(self.sql)
        self.result = configPG.get_one(self.cursor)
        print(self.result)

        if self.result[0] == 1:
            self.assertEqual(self.result[0], 1)
            self.assertEqual(self.result[1], 1)
            print("PGdb adx_issued is test seccussfully!")
        else:
            self.assertEqual(self.result[0], 1)
            self.assertEqual(self.result[1], 1)
            print("PGdb adx_issued test failed")


    def checkResult(self):
        """
        check test result
        :return:
        """
        self.info = self.return_json.json()
        # show return message
        common.show_return_msg(self.return_json)

        if self.result == '0':
            #print(self.info)
            #self.assertEqual(self.info["statusCode"], self.code)
            self.assertEqual(self.info['rcs'][0]['configid'],'adxDsp_210_4')

        if self.result == '1':
            #self.assertEqual(self.info['statusCode'], self.code)
            self.assertEqual(self.info['rcs'][0]['configId'], 'adxDsp_210_4')


    def checkShow(self):
        """
        test data collection of beaconhub
        :return:
        """
        self.info = self.return_json.json()
        i = datetime.datetime.now()
        while i.second > 5:
            time.sleep(5)
            i = datetime.datetime.now()
            print("curent second is ", i.second)
        time.sleep(1)

        beaurl = self.info['rcs'][0]['beaconurl']
        self.url = self.info['rcs'][0]['beacon']['impression'][0]['parameters']
        self.url = beaurl + self.url
        time.sleep(1)
        self.code = requests.request('GET', self.url)

        time.sleep(1)
        configPG.connectPG("root","aszx","5432","192.168.0.66","adx_report")
        self.sql = "select impression2 from public.stats where dsp_app_id='210'and ad_type='4'and ad_group_id='25' and ad_channel_id=451 and ad_customer_id=14207  order by timestamp DESC"
        self.cursor = configPG.executeSQL(self.sql)
        self.result = configPG.get_one(self.cursor)
        print(self.result)
        if self.result[0] == 1:
            self.assertEqual(self.result[0], 1)
            print("PGdb impressions is test seccussfully!")
        else:
            self.assertEqual(self.result[0], 1)
            print("PGdb impressions test failed")
        time.sleep(60)

    def checkClick(self):
        """
        test data collection of beaconhub
        :return:
        """
        self.info = self.return_json.json()
        time.sleep(1)

        beaurl = self.info['rcs'][0]['beaconurl']
        time.sleep(1)
        self.url = self.info['rcs'][0]['beacon']['click'][0]['parameters']
        self.url = beaurl + self.url
        json_path = os.path.join(readConfig.proDir, "testFile","json","show_clike_post.json")
        json = configHttp.load_json(json_path)
        self.code = requests.request('POST', self.url,json=json)
        self.assertEqual(self.code.status_code,204)
        time.sleep(1)
        configPG.connectPG("root","aszx","5432","192.168.0.66","adx_report")
        self.sql = "select click from public.stats where dsp_app_id='210' and ad_type='4'and ad_group_id='25' and ad_channel_id=451 and ad_customer_id=14207  order by timestamp DESC"
        self.cursor = configPG.executeSQL(self.sql)
        self.result = configPG.get_one(self.cursor)

        if self.result[0] == 1:
            self.assertEqual(self.result[0], 1)
            print("PGdb click is test seccussfully!")
        else:
            self.assertEqual(self.result[0], 1)
            print("PGdb click test failed")


    def checkDownloadstarted(self):
        """
        test download_start data collection of beaconhub
        :return:
        """
        self.info = self.return_json.json()
        time.sleep(1)

        beaurl = self.info['rcs'][0]['beaconurl']
        time.sleep(1)
        self.url = self.info['rcs'][0]['beacon']['downloadstarted'][0]['parameters']
        self.url = beaurl + self.url
        self.code = requests.request('GET', self.url)
        print(self.url)
        time.sleep(1)
        configPG.connectPG("root","aszx","5432","192.168.0.66","adx_report")
        self.sql = "select download_start from public.stats where dsp_app_id='210' and ad_type='4'and ad_group_id='25' and ad_channel_id=451 and ad_customer_id=14207 order by timestamp DESC"
        self.cursor = configPG.executeSQL(self.sql)
        self.result = configPG.get_one(self.cursor)

        if self.result[0] == 1:
            self.assertEqual(self.result[0], 1)
            print("PGdb download_start is test seccussfully!")
        else:
            self.assertEqual(self.result[0], 1)
            print("PGdb download_start test failed")
    def checkDownloadcompleted(self):
        """
        test download_start data collection of beaconhub
        :return:
        """
        self.info = self.return_json.json()
        time.sleep(1)

        beaurl = self.info['rcs'][0]['beaconurl']
        time.sleep(1)
        self.url = self.info['rcs'][0]['beacon']['downloadcompleted'][0]['parameters']
        self.url = beaurl + self.url
        self.code = requests.request('GET', self.url)

        time.sleep(1)
        configPG.connectPG("root","aszx","5432","192.168.0.66","adx_report")
        self.sql = "select download_completed from public.stats where dsp_app_id='210' and ad_type='4'and ad_group_id='25' and ad_channel_id=451 and ad_customer_id=14207 order by timestamp DESC"
        self.cursor = configPG.executeSQL(self.sql)
        self.result = configPG.get_one(self.cursor)

        if self.result[0] == 1:
            self.assertEqual(self.result[0], 1)
            print("PGdb download_completed is test seccussfully!")
        else:
            self.assertEqual(self.result[0], 1)
            print("PGdb download_completed test failed")
    def checkDownloadfailed(self):
        """
        test download_failed data collection of beaconhub
        :return:
        """
        self.info = self.return_json.json()
        time.sleep(1)

        beaurl = self.info['rcs'][0]['beaconurl']
        time.sleep(1)
        self.url = self.info['rcs'][0]['beacon']['downloadfailed'][0]['parameters']
        self.url = beaurl + self.url
        self.code = requests.request('GET', self.url)

        time.sleep(1)
        configPG.connectPG("root","aszx","5432","192.168.0.66","adx_report")
        self.sql = "select download_failed  from public.stats where dsp_app_id='210' and ad_type='4'and ad_group_id='25' and ad_channel_id=451 and ad_customer_id=14207 order by timestamp DESC"
        self.cursor = configPG.executeSQL(self.sql)
        self.result = configPG.get_one(self.cursor)

        if self.result[0] == 1:
            self.assertEqual(self.result[0], 1)
            print("PGdb download_failed is test seccussfully!")
        else:
            self.assertEqual(self.result[0], 1)
            print("PGdb download_failed test failed")
    def checkInstallstarted(self):
        """
        test install_started data collection of beaconhub
        :return:
        """
        self.info = self.return_json.json()
        time.sleep(1)

        beaurl = self.info['rcs'][0]['beaconurl']
        time.sleep(1)
        self.url = self.info['rcs'][0]['beacon']['installstarted'][0]['parameters']
        self.url = beaurl + self.url
        self.code = requests.request('GET', self.url)

        time.sleep(1)
        configPG.connectPG("root","aszx","5432","192.168.0.66","adx_report")
        self.sql = "select install_start  from public.stats where dsp_app_id='210' and ad_type='4'and ad_group_id='25' and ad_channel_id=451 and ad_customer_id=14207 order by timestamp DESC"
        self.cursor = configPG.executeSQL(self.sql)
        self.result = configPG.get_one(self.cursor)

        if self.result[0] == 1:
            self.assertEqual(self.result[0], 1)
            print("PGdb install_start is test seccussfully!")
        else:
            self.assertEqual(self.result[0], 1)
            print("PGdb install_start test failed")
    def checkInstallcompleted(self):
        """
        test installcompleted data collection of beaconhub
        :return:
        """
        self.info = self.return_json.json()
        time.sleep(1)

        beaurl = self.info['rcs'][0]['beaconurl']
        time.sleep(1)
        self.url = self.info['rcs'][0]['beacon']['installcompleted'][0]['parameters']
        self.url = beaurl + self.url
        self.code = requests.request('GET', self.url)

        time.sleep(1)
        configPG.connectPG("root","aszx","5432","192.168.0.66","adx_report")
        self.sql = "select install_completed  from public.stats where dsp_app_id='210' and ad_type='4'and ad_group_id='25' and ad_channel_id=451 and ad_customer_id=14207 order by timestamp DESC"
        self.cursor = configPG.executeSQL(self.sql)
        self.result = configPG.get_one(self.cursor)

        if self.result[0] == 1:
            self.assertEqual(self.result[0], 1)
            print("PGdb install_completed is test seccussfully!")
        else:
            self.assertEqual(self.result[0], 1)
            print("PGdb install_completed test failed")
    def checkInstallfailed(self):
        """
        test install_failed data collection of beaconhub
        :return:
        """
        self.info = self.return_json.json()
        time.sleep(1)

        beaurl = self.info['rcs'][0]['beaconurl']
        time.sleep(1)
        self.url = self.info['rcs'][0]['beacon']['installfailed'][0]['parameters']
        self.url = beaurl + self.url
        self.code = requests.request('GET', self.url)

        time.sleep(1)
        configPG.connectPG("root","aszx","5432","192.168.0.66","adx_report")
        self.sql = "select install_failed  from public.stats where dsp_app_id='210' and ad_type='4'and ad_group_id='25' and ad_channel_id=451 and ad_customer_id=14207 order by timestamp DESC"
        self.cursor = configPG.executeSQL(self.sql)
        self.result = configPG.get_one(self.cursor)

        if self.result[0] == 1:
            self.assertEqual(self.result[0], 1)
            print("PGdb install_failed is test seccussfully!")
        else:
            self.assertEqual(self.result[0], 1)
            print("PGdb install_failed test failed")
    def checkPicdownloadstart(self):
        """
        test pic_download_start data collection of beaconhub
        :return:
        """
        self.info = self.return_json.json()
        time.sleep(1)

        beaurl = self.info['rcs'][0]['beaconurl']
        time.sleep(1)
        self.url = self.info['rcs'][0]['beacon']['picdownloadstart'][0]['parameters']
        self.url = beaurl + self.url
        self.code = requests.request('GET', self.url)

        time.sleep(1)
        configPG.connectPG("root","aszx","5432","192.168.0.66","adx_report")
        self.sql = "select pic_download_start  from public.stats where dsp_app_id='210' and ad_type='4'and ad_group_id='25' and ad_channel_id=451 and ad_customer_id=14207 order by timestamp DESC"
        self.cursor = configPG.executeSQL(self.sql)
        self.result = configPG.get_one(self.cursor)

        if self.result[0] == 1:
            self.assertEqual(self.result[0], 1)
            print("PGdb pic_download_start is test seccussfully!")
        else:
            self.assertEqual(self.result[0], 1)
            print("PGdb pic_download_start test failed")
    def checkPicdownloadcompleted(self):
        """
        test pic_download_completed data collection of beaconhub
        :return:
        """
        self.info = self.return_json.json()
        time.sleep(1)

        beaurl = self.info['rcs'][0]['beaconurl']
        time.sleep(1)
        self.url = self.info['rcs'][0]['beacon']['picdownloadcompleted'][0]['parameters']
        self.url = beaurl + self.url
        self.code = requests.request('GET', self.url)

        time.sleep(1)
        configPG.connectPG("root","aszx","5432","192.168.0.66","adx_report")
        self.sql = "select pic_download_completed  from public.stats where dsp_app_id='210' and ad_type='4'and ad_group_id='25' and ad_channel_id=451 and ad_customer_id=14207 order by timestamp DESC"
        self.cursor = configPG.executeSQL(self.sql)
        self.result = configPG.get_one(self.cursor)

        if self.result[0] == 1:
            self.assertEqual(self.result[0], 1)
            print("PGdb pic_download_completed is test seccussfully!")
        else:
            self.assertEqual(self.result[0], 1)
            print("PGdb pic_download_completed test failed")
    def checkPicdownloadfailed(self):
        """
        test pic_download_start data collection of beaconhub
        :return:
        """
        self.info = self.return_json.json()
        time.sleep(1)

        beaurl = self.info['rcs'][0]['beaconurl']
        time.sleep(1)
        self.url = self.info['rcs'][0]['beacon']['picdownloadfailed'][0]['parameters']
        self.url = beaurl + self.url
        self.code = requests.request('GET', self.url)

        time.sleep(1)
        configPG.connectPG("root","aszx","5432","192.168.0.66","adx_report")
        self.sql = "select pic_download_failed  from public.stats where dsp_app_id='210' and ad_type='4'and ad_group_id='25' and ad_channel_id=451 and ad_customer_id=14207 order by timestamp DESC"
        self.cursor = configPG.executeSQL(self.sql)
        self.result = configPG.get_one(self.cursor)

        if self.result[0] == 1:
            self.assertEqual(self.result[0], 1)
            print("PGdb pic_download_failed is test seccussfully!")
        else:
            self.assertEqual(self.result[0], 1)
            print("PGdb pic_download_failed test failed")

    def checkInstallremindfailed(self):
        """
        test install_remind_failed data collection of beaconhub
        :return:
        """
        self.info = self.return_json.json()
        time.sleep(1)

        beaurl = self.info['rcs'][0]['beaconurl']
        time.sleep(1)
        self.url = self.info['rcs'][0]['beacon']['installremindfailed'][0]['parameters']
        self.url = beaurl + self.url
        self.code = requests.request('GET', self.url)

        time.sleep(1)
        configPG.connectPG("root","aszx","5432","192.168.0.66","adx_report")
        self.sql = "select install_remind_failed  from public.stats where dsp_app_id='210' and ad_type='4'and ad_group_id='25' and ad_channel_id=451 and ad_customer_id=14207 order by timestamp DESC"
        self.cursor = configPG.executeSQL(self.sql)
        self.result = configPG.get_one(self.cursor)

        if self.result[0] == 1:
            self.assertEqual(self.result[0], 1)
            print("PGdb install_remind_failed is test seccussfully!")
        else:
            self.assertEqual(self.result[0], 1)
            print("PGdb install_remind_failed test failed")
    def checkAppopen(self):
        """
        test app_activated data collection of beaconhub
        :return:
        """
        self.info = self.return_json.json()
        time.sleep(1)

        beaurl = self.info['rcs'][0]['beaconurl']
        time.sleep(1)
        self.url = self.info['rcs'][0]['beacon']['appopen'][0]['parameters']
        self.url = beaurl + self.url
        self.code = requests.request('GET', self.url)

        time.sleep(1)
        configPG.connectPG("root","aszx","5432","192.168.0.66","adx_report")
        self.sql = "select app_activated  from public.stats where dsp_app_id='210' and ad_type='4'and ad_group_id='25' and ad_channel_id=451 and ad_customer_id=14207 order by timestamp DESC"
        self.cursor = configPG.executeSQL(self.sql)
        self.result = configPG.get_one(self.cursor)

        if self.result[0] == 1:
            self.assertEqual(self.result[0], 1)
            print("PGdb app_activated is test seccussfully!")
        else:
            self.assertEqual(self.result[0], 1)
            print("PGdb app_activated test failed")

    def checkActive2(self):
        """
        test active2 data collection of beaconhub
        :return:
        """
        self.info = self.return_json.json()
        time.sleep(1)

        beaurl = self.info['rcs'][0]['beaconurl']
        time.sleep(1)
        self.url = self.info['rcs'][0]['beacon']['active2'][0]['parameters']
        self.url = beaurl + self.url
        self.code = requests.request('GET', self.url)

        time.sleep(1)
        configPG.connectPG("root","aszx","5432","192.168.0.66","adx_report")
        self.sql = "select active2  from public.stats where dsp_app_id='210' and ad_type='4'and ad_group_id='25' and ad_channel_id=451 and ad_customer_id=14207 order by timestamp DESC"
        self.cursor = configPG.executeSQL(self.sql)
        self.result = configPG.get_one(self.cursor)

        if self.result[0] == 1:
            self.assertEqual(self.result[0], 1)
            print("PGdb active2 is test seccussfully!")
        else:
            self.assertEqual(self.result[0], 1)
            print("PGdb active2 test failed")

    def checkAutoclosebutton(self):
        """
        test auto_close_button data collection of beaconhub
        :return:
        """
        self.info = self.return_json.json()
        time.sleep(1)

        beaurl = self.info['rcs'][0]['beaconurl']
        time.sleep(1)
        self.url = self.info['rcs'][0]['beacon']['autoclosebutton'][0]['parameters']
        self.url = beaurl + self.url
        self.code = requests.request('GET', self.url)

        time.sleep(1)
        configPG.connectPG("root","aszx","5432","192.168.0.66","adx_report")
        self.sql = "select auto_close_button  from public.stats where dsp_app_id='210' and ad_type='4'and ad_group_id='25' and ad_channel_id=451 and ad_customer_id=14207 order by timestamp DESC"
        self.cursor = configPG.executeSQL(self.sql)
        self.result = configPG.get_one(self.cursor)

        if self.result[0] == 1:
            self.assertEqual(self.result[0], 1)
            print("PGdb auto_close_button is test seccussfully!")
        else:
            self.assertEqual(self.result[0], 1)
            print("PGdb auto_close_button test failed")
    def checkDspissued(self):
        """
        test c2s_dsp_issued data collection of beaconhub
        :return:
        """
        self.info = self.return_json.json()
        time.sleep(1)

        beaurl = self.info['rcs'][0]['beaconurl']
        time.sleep(1)
        self.url = self.info['rcs'][0]['beacon']['dspissued'][0]['parameters']
        self.url = beaurl + self.url
        self.code = requests.request('GET', self.url)

        time.sleep(1)
        configPG.connectPG("root","aszx","5432","192.168.0.66","adx_report")
        self.sql = "select c2s_dsp_issued  from public.stats where dsp_app_id='210' and ad_type='4'and ad_group_id='25' and ad_channel_id=451 and ad_customer_id=14207 order by timestamp DESC"
        self.cursor = configPG.executeSQL(self.sql)
        self.result = configPG.get_one(self.cursor)

        if self.result[0] == 1:
            self.assertEqual(self.result[0], 1)
            print("PGdb c2s_dsp_issued is test seccussfully!")
        else:
            self.assertEqual(self.result[0], 1)
            print("PGdb c2s_dsp_issued test failed")

    def checkGiveup(self):
        """
        test give_up data collection of beaconhub
        :return:
        """
        self.info = self.return_json.json()
        time.sleep(1)

        beaurl = self.info['rcs'][0]['beaconurl']
        time.sleep(1)
        self.url = self.info['rcs'][0]['beacon']['giveup'][0]['parameters']
        self.url = beaurl + self.url
        self.code = requests.request('GET', self.url)

        time.sleep(1)
        configPG.connectPG("root","aszx","5432","192.168.0.66","adx_report")
        self.sql = "select give_up  from public.stats where dsp_app_id='210' and ad_type='4'and ad_group_id='25' and ad_channel_id=451 and ad_customer_id=14207 order by timestamp DESC"
        self.cursor = configPG.executeSQL(self.sql)
        self.result = configPG.get_one(self.cursor)

        if self.result[0] == 1:
            self.assertEqual(self.result[0], 1)
            print("PGdb give_up is test seccussfully!")
        else:
            self.assertEqual(self.result[0], 1)
            print("PGdb give_up test failed")

    def checkManualclosebutton(self):
        """
        test menual_close_button data collection of beaconhub
        :return:
        """
        self.info = self.return_json.json()
        time.sleep(1)

        beaurl = self.info['rcs'][0]['beaconurl']
        time.sleep(1)
        self.url = self.info['rcs'][0]['beacon']['manualclosebutton'][0]['parameters']
        self.url = beaurl + self.url
        self.code = requests.request('GET', self.url)

        time.sleep(1)
        configPG.connectPG("root","aszx","5432","192.168.0.66","adx_report")
        self.sql = "select menual_close_button  from public.stats where dsp_app_id='210' and ad_type='4'and ad_group_id='25' and ad_channel_id=451 and ad_customer_id=14207 order by timestamp DESC"
        self.cursor = configPG.executeSQL(self.sql)
        self.result = configPG.get_one(self.cursor)

        if self.result[0] == 1:
            self.assertEqual(self.result[0], 1)
            print("PGdb menual_close_button is test seccussfully!")
        else:
            self.assertEqual(self.result[0], 1)
            print("PGdb menual_close_button test failed")

    def checkNewsclick(self):
        """
        test news_click data collection of beaconhub
        :return:
        """
        self.info = self.return_json.json()
        time.sleep(1)

        beaurl = self.info['rcs'][0]['beaconurl']
        time.sleep(1)
        self.url = self.info['rcs'][0]['beacon']['newsclick'][0]['parameters']
        self.url = beaurl + self.url
        self.code = requests.request('GET', self.url)

        time.sleep(1)
        configPG.connectPG("root","aszx","5432","192.168.0.66","adx_report")
        self.sql = "select news_click  from public.stats where dsp_app_id='210' and ad_type='4'and ad_group_id='25' and ad_channel_id=451 and ad_customer_id=14207 order by timestamp DESC"
        self.cursor = configPG.executeSQL(self.sql)
        self.result = configPG.get_one(self.cursor)

        if self.result[0] == 1:
            self.assertEqual(self.result[0], 1)
            print("PGdb news_click is test seccussfully!")
        else:
            self.assertEqual(self.result[0], 1)
            print("PGdb news_click test failed")

    def checkNewsimpression(self):
        """
        test news_impression data collection of beaconhub
        :return:
        """
        self.info = self.return_json.json()
        time.sleep(1)

        beaurl = self.info['rcs'][0]['beaconurl']
        time.sleep(1)
        self.url = self.info['rcs'][0]['beacon']['newsimpression'][0]['parameters']
        self.url = beaurl + self.url
        self.code = requests.request('GET', self.url)

        time.sleep(1)
        configPG.connectPG("root","aszx","5432","192.168.0.66","adx_report")
        self.sql = "select news_impression  from public.stats where dsp_app_id='210' and ad_type='4'and ad_group_id='25' and ad_channel_id=451 and ad_customer_id=14207 order by timestamp DESC"
        self.cursor = configPG.executeSQL(self.sql)
        self.result = configPG.get_one(self.cursor)

        if self.result[0] == 1:
            self.assertEqual(self.result[0], 1)
            print("PGdb news_impression is test seccussfully!")
        else:
            self.assertEqual(self.result[0], 1)
            print("PGdb news_impression test failed")

    def checkUrljump(self):
        """
        test url_jump data collection of beaconhub
        :return:
        """
        self.info = self.return_json.json()
        time.sleep(1)

        beaurl = self.info['rcs'][0]['beaconurl']
        time.sleep(1)
        self.url = self.info['rcs'][0]['beacon']['urljump'][0]['parameters']
        self.url = beaurl + self.url
        self.code = requests.request('GET', self.url)

        time.sleep(1)
        configPG.connectPG("root","aszx","5432","192.168.0.66","adx_report")
        self.sql = "select url_jump  from public.stats where dsp_app_id='210' and ad_type='4'and ad_group_id='25' and ad_channel_id=451 and ad_customer_id=14207 order by timestamp DESC"
        self.cursor = configPG.executeSQL(self.sql)
        self.result = configPG.get_one(self.cursor)

        if self.result[0] == 1:
            self.assertEqual(self.result[0], 1)
            print("PGdb url_jump is test seccussfully!")
        else:
            self.assertEqual(self.result[0], 1)
            print("PGdb url_jump test failed")

    def checkTodsprequest(self):
        """
        test to_dsp_request data collection of beaconhub
        :return:
        """
        self.info = self.return_json.json()
        time.sleep(1)

        beaurl = self.info['rcs'][0]['beaconurl']
        time.sleep(1)
        self.url = self.info['rcs'][0]['beacon']['todsprequest'][0]['parameters']
        self.url = beaurl + self.url
        self.code = requests.request('GET', self.url)
        print(self.url)
        time.sleep(1)
        configPG.connectPG("root","aszx","5432","192.168.0.66","adx_report")
        self.sql = "select to_dsp_request  from public.stats where dsp_app_id='210' and ad_type='4'and ad_group_id='25' and ad_channel_id=451 and ad_customer_id=14207 order by timestamp DESC"
        self.cursor = configPG.executeSQL(self.sql)
        self.result = configPG.get_one(self.cursor)

        if self.result[0] == 1:
            self.assertEqual(self.result[0], 1)
            print("PGdb to_dsp_request is test seccussfully!")
        else:
            self.assertEqual(self.result[0], 1)
            print("PGdb to_dsp_request test failed")

    def checkOpenexists(self):
        """
        test app_open data collection of beaconhub
        :return:
        """
        self.info = self.return_json.json()
        time.sleep(1)

        beaurl = self.info['rcs'][0]['beaconurl']
        time.sleep(1)
        self.url = self.info['rcs'][0]['beacon']['openexists'][0]['parameters']
        self.url = beaurl + self.url
        self.code = requests.request('GET', self.url)
        print(self.url)
        time.sleep(1)
        configPG.connectPG("root","aszx","5432","192.168.0.66","adx_report")
        self.sql = "select app_open  from public.stats where dsp_app_id='210' and ad_type='4'and ad_group_id='25' and ad_channel_id=451 and ad_customer_id=14207 order by timestamp DESC"
        self.cursor = configPG.executeSQL(self.sql)
        self.result = configPG.get_one(self.cursor)

        if self.result[0] == 1:
            self.assertEqual(self.result[0], 1)
            print("PGdb app_open is test seccussfully!")
        else:
            self.assertEqual(self.result[0], 1)
            print("PGdb app_open test failed")
    def active2_failed(self):
        """
        test active2_failed data collection of beaconhub
        :return:
        """
        self.info = self.return_json.json()
        time.sleep(1)

        beaurl = self.info['rcs'][0]['beaconurl']
        time.sleep(1)
        self.url = self.info['rcs'][0]['beacon']['active2_failed'][0]['parameters']
        self.url = beaurl + self.url
        self.code = requests.request('GET', self.url)
        print(self.url)
        time.sleep(1)
        configPG.connectPG("root","aszx","5432","192.168.0.66","adx_report")
        self.sql = "select active2_failed  from public.stats where dsp_app_id='210' and ad_type='4'and ad_group_id='25' and ad_channel_id=451 and ad_customer_id=14207 order by timestamp DESC"
        self.cursor = configPG.executeSQL(self.sql)
        self.result = configPG.get_one(self.cursor)
        if self.result[0] == 1:
            self.assertEqual(self.result[0], 1)
            print("PGdb active2_failed is test seccussfully!")
        else:
            self.assertEqual(self.result[0], 1)
            print("PGdb active2_failed test failed")
    def active3(self):
        """
        test active3 data collection of beaconhub
        :return:
        """
        self.info = self.return_json.json()
        time.sleep(1)

        beaurl = self.info['rcs'][0]['beaconurl']
        time.sleep(1)
        self.url = self.info['rcs'][0]['beacon']['active3'][0]['parameters']
        self.url = beaurl + self.url
        self.code = requests.request('GET', self.url)
        print(self.url)
        time.sleep(1)
        configPG.connectPG("root","aszx","5432","192.168.0.66","adx_report")
        self.sql = "select active3  from public.stats where dsp_app_id='210' and ad_type='4'and ad_group_id='25' and ad_channel_id=451 and ad_customer_id=14207 order by timestamp DESC"
        self.cursor = configPG.executeSQL(self.sql)
        self.result = configPG.get_one(self.cursor)
        if self.result[0] == 1:
            self.assertEqual(self.result[0], 1)
            print("PGdb active3 is test seccussfully!")
        else:
            self.assertEqual(self.result[0], 1)
            print("PGdb active3 test failed")

    def active3_failed(self):
        """
        test active2_failed data collection of beaconhub
        :return:
        """
        self.info = self.return_json.json()
        time.sleep(1)

        beaurl = self.info['rcs'][0]['beaconurl']
        time.sleep(1)
        self.url = self.info['rcs'][0]['beacon']['active3_failed'][0]['parameters']
        self.url = beaurl + self.url
        self.code = requests.request('GET', self.url)
        print(self.url)
        time.sleep(1)
        configPG.connectPG("root","aszx","5432","192.168.0.66","adx_report")
        self.sql = "select active3_failed  from public.stats where dsp_app_id='210' and ad_type='4'and ad_group_id='25' and ad_channel_id=451 and ad_customer_id=14207 order by timestamp DESC"
        self.cursor = configPG.executeSQL(self.sql)
        self.result = configPG.get_one(self.cursor)
        if self.result[0] == 1:
            self.assertEqual(self.result[0], 1)
            print("PGdb active3_failed is test seccussfully!")
        else:
            self.assertEqual(self.result[0], 1)
            print("PGdb active3_failed test failed")
    def sendUrl2Beaconhub(self):
        """
        send get request to beaconhub service
        :return:
        """
        # self.info = self.return_json.json()
        # i = datetime.datetime.now()
        # while i.second > 5:
        #     time.sleep(5)
        #     i = datetime.datetime.now()
        #     print("curent second is ", i.second)
        # time.sleep(2)
        #
        beaurl = self.info['rcs'][0]['beaconurl']
        # self.url = self.info['rcs'][0]['beacon']['show'][1]['parameters']
        # self.url = beaurl + self.url
        # time.sleep(1)
        # self.code = requests.request('GET', self.url)

        # time.sleep(1)
        # self.url = self.info['rcs'][0]['beacon']['click'][0]['parameters']
        # self.url = beaurl + self.url
        # self.code = requests.request('GET', self.url)

        time.sleep(1)
        self.url = self.info['rcs'][0]['beacon']['down'][1]['parameters']
        self.url = beaurl + self.url
        self.code = requests.request('GET', self.url)

        time.sleep(1)
        self.url = self.info['rcs'][0]['beacon']['downs'][1]['parameters']
        self.url = beaurl + self.url
        self.code = requests.request('GET', self.url)

        time.sleep(1)
        self.url = self.info['rcs'][0]['beacon']['instl'][0]['parameters']
        self.url = beaurl + self.url
        self.code = requests.request('GET', self.url)

        time.sleep(1)
        self.url = self.info['rcs'][0]['beacon']['insls'][1]['parameters']
        self.url = beaurl + self.url
        self.code = requests.request('GET', self.url)

        time.sleep(1)
        self.url = self.info['rcs'][0]['beacon']['openexists'][0]['parameters']
        self.url = beaurl + self.url
        self.code = requests.request('GET', self.url)

        time.sleep(1)
        self.url = self.info['rcs'][0]['beacon']['open'][0]['parameters']
        self.url = beaurl + self.url
        self.code = requests.request('GET', self.url)

        time.sleep(1)
        self.url = self.info['rcs'][0]['beacon']['active2'][0]['parameters']
        self.url = beaurl + self.url
        self.code = requests.request('GET', self.url)

        time.sleep(1)
        self.url = self.info['rcs'][0]['beacon']['todsprequest'][0]['parameters']
        self.url = beaurl + self.url
        self.code = requests.request('GET', self.url)

        time.sleep(1)
        self.url = self.info['rcs'][0]['beacon']['dspissued'][0]['parameters']
        self.url = beaurl + self.url
        self.code = requests.request('GET', self.url)

        time.sleep(1)
        self.url = self.info['rcs'][0]['beacon']['picdownlorcstart'][0]['parameters']
        self.url = beaurl + self.url
        self.code = requests.request('GET', self.url)

        time.sleep(1)
        self.url = self.info['rcs'][0]['beacon']['picdownloadcompleted'][0]['parameters']
        self.url = beaurl + self.url
        self.code = requests.request('GET', self.url)

        time.sleep(1)
        self.url = self.info['rcs'][0]['beacon']['picdownloadfailed'][0]['parameters']
        self.url = beaurl + self.url
        self.code = requests.request('GET', self.url)

        time.sleep(1)
        self.url = self.info['rcs'][0]['beacon']['giveup'][0]['parameters']
        self.url = beaurl + self.url
        self.code = requests.request('GET', self.url)

        time.sleep(1)
        self.url = self.info['rcs'][0]['beacon']['urljump'][0]['parameters']
        self.url = beaurl + self.url
        self.code = requests.request('GET', self.url)

        time.sleep(1)
        self.url = self.info['rcs'][0]['beacon']['manualclosebutton'][0]['parameters']
        self.url = beaurl + self.url
        self.code = requests.request('GET', self.url)

        time.sleep(1)
        self.url = self.info['rcs'][0]['beacon']['autoclosebutton'][0]['parameters']
        self.url = beaurl + self.url
        self.code = requests.request('GET', self.url)

        time.sleep(1)
        self.url = self.info['rcs'][0]['beacon']['installremindfailed'][0]['parameters']
        self.url = beaurl + self.url
        self.code = requests.request('GET', self.url)

        time.sleep(1)
        self.url = self.info['rcs'][0]['beacon']['newsimpression'][0]['parameters']
        self.url = beaurl + self.url
        self.code = requests.request('GET', self.url)

        time.sleep(1)
        self.url = self.info['rcs'][0]['beacon']['newsclick'][0]['parameters']
        self.url = beaurl + self.url
        self.code = requests.request('GET', self.url)

        time.sleep(1)
        self.url = self.info['rcs'][0]['beacon']['downloadfailed'][0]['parameters']
        self.url = beaurl + self.url
        self.code = requests.request('GET', self.url)

        time.sleep(1)
        self.url = self.info['rcs'][0]['beacon']['installfailed'][0]['parameters']
        self.url = beaurl + self.url
        self.code = requests.request('GET', self.url)

    def testC2s2(self):
        """
        test body
        :return:
        """
        # set url
        url = adx_xls[2][3]
        print(url)
        print("第一步：设置url  "+self.url)

        # set headers
        header = localReadConfig.get_headers("header")
        header = {"header": str(header)}
        #print(header)
        configHttp.set_headers(header)
        print("第二步：设置header等")

        # set params
        json_path = os.path.join(readConfig.proDir, "testFile","json","c2s2.json")
        json = configHttp.load_json(json_path)
        print("第三步：设置发送请求的参数")

        self.return_json = requests.request("POST", url, json = json)
        #print(self.return_json.json())

        method = str(self.return_json.request)[int(str(self.return_json.request).find('['))+1:int(str(self.return_json.request).find(']'))]
        print("第四步：发送请求\n\t\t请求方法："+method)

        # check result
        self.checkResult()
        print("第五步：检查Http请求结果")

        print("第六步：校验PGdb数据")
        #self.checkPGdb()

        self.checkShow()
        # self.checkClick()
        # self.checkDownloadstarted()
        # self.checkDownloadcompleted()
        # self.checkDownloadfailed()
        # self.checkInstallstarted()
        # self.checkInstallcompleted()
        # self.checkInstallfailed()
        # self.checkPicdownloadstart()
        # self.checkPicdownloadcompleted()
        # self.checkPicdownloadfailed()
        # self.checkInstallremindfailed()
        # self.checkDspissued()
        # self.checkGiveup()
        # self.checkManualclosebutton()
        # self.checkAppopen()
        # #self.checkActive2()
        # self.checkAutoclosebutton()
        # self.checkUrljump()
        # self.checkNewsclick()
        # self.checkNewsimpression()
        # #self.checkTodsprequest()
        # self.checkOpenexists()
        print("第七步：发送get请求给Beaconhub服务")
        # self.sendUrl2Beaconhub()

    def tearDown(self):
        """s

        :return:
        """
        #info = self.info
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

if __name__ == '__main__':
    unittest.main()















