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
class S2s1(unittest.TestCase):
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
        configPG.connectPG("adx_report")
        self.sql = "select publisher_request from public.stats where ad_group_id='46'and ad_channel_id='645' and ad_customer_id='14257' and dsp_app_id='0' order by timestamp desc"
        self.cursor = configPG.executeSQL(self.sql)
        self.result = configPG.get_one(self.cursor)

        self.assertEqual(self.result[0], 1)

        self.sql = "select adx_issued,to_dsp_request from public.stats where dsp_app_id='172'and ad_type='2' and ad_group_id='46'and ad_channel_id='645' and ad_customer_id='14257' and imp_type= '1'order by timestamp DESC"
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
            self.assertEqual(self.info["statusCode"], self.code)
            self.assertEqual(self.info['ads'][0]['configId'],'adxDsp_172_2')

        if self.result == '1':
            self.assertEqual(self.info['statusCode'], self.code)
            self.assertEqual(self.info['ads'][0]['configId'], 'adxDsp_172_2')


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

        beaurl = self.info['ads'][0]['adxBeaconUrl']
        self.url = self.info['ads'][0]['callUrl3']['show'][0]['parameters']
        self.url = beaurl + self.url
        time.sleep(1)
        self.code = requests.request('GET', self.url)

        code = str(self.code)[int(str(self.code).find('[')) +1 :int(str(self.code).find(']'))]
        self.assertEqual(code, '204')
        print("show url is ",self.url)

        time.sleep(2)
        configPG.connectPG("adx_report")
        self.sql = "select impressions from public.stats where dsp_app_id='172'and ad_type='2'and ad_group_id='46'and ad_channel_id='645' and ad_customer_id='14257' and imp_type= '1' order by timestamp DESC"
        self.cursor = configPG.executeSQL(self.sql)
        self.result = configPG.get_one(self.cursor)
        print(self.result)

        if self.result[0] == 1:
            self.assertEqual(self.result[0], 1)
            print("PGdb impressions is test seccussfully!")
        else:
            self.assertEqual(self.result[0], 1)
            print("PGdb impressions test failed")

    def checkClick(self):
        """
        test data collection of beaconhub
        :return:
        """
        self.info = self.return_json.json()
        time.sleep(1)

        beaurl = self.info['ads'][0]['adxBeaconUrl']
        time.sleep(1)
        self.url = self.info['ads'][0]['callUrl3']['click'][1]['parameters']
        self.url = beaurl + self.url

        self.code = requests.request('GET', self.url)
        code = str(self.code)[int(str(self.code).find('[')) + 1:int(str(self.code).find(']'))]
        self.assertEqual(code, '204')

        time.sleep(1)
        configPG.connectPG("adx_report")
        self.sql = "select click from public.stats where dsp_app_id='172' and ad_type='2'and ad_group_id='46'and ad_channel_id='645' and ad_customer_id='14257'and imp_type= '1'order by timestamp DESC"
        self.cursor = configPG.executeSQL(self.sql)
        self.result = configPG.get_one(self.cursor)
        print(self.result)

        if self.result[0] == 1:
            self.assertEqual(self.result[0], 1)
            print("PGdb click is test seccussfully!")
        else:
            self.assertEqual(self.result[0], 1)
            print("PGdb click test failed")


    def checkDown(self):
        """
        test download_start data collection of beaconhub
        :return:
        """
        self.info = self.return_json.json()
        time.sleep(1)

        beaurl = self.info['ads'][0]['adxBeaconUrl']
        time.sleep(1)
        self.url = self.info['ads'][0]['callUrl3']['down'][0]['parameters']
        self.url = beaurl + self.url

        self.code = requests.request('GET', self.url)
        code = str(self.code)[int(str(self.code).find('[')) + 1:int(str(self.code).find(']'))]
        self.assertEqual(code, '204')

        time.sleep(1)
        configPG.connectPG("adx_report")
        self.sql = "select download_start from public.stats where dsp_app_id='172' and ad_type='2'and ad_group_id='46'and ad_channel_id='645' and ad_customer_id='14257'and imp_type= '1'order by timestamp DESC"
        self.cursor = configPG.executeSQL(self.sql)
        self.result = configPG.get_one(self.cursor)
        print(self.result)

        if self.result[0] == 1:
            self.assertEqual(self.result[0], 1)
            print("PGdb download_start is test seccussfully!")
        else:
            self.assertEqual(self.result[0], 1)
            print("PGdb download_start test failed")

    def checkDowns(self):
        """
        test download_completed data collection of beaconhub
        :return:
        """
        self.info = self.return_json.json()
        time.sleep(1)

        beaurl = self.info['ads'][0]['adxBeaconUrl']
        time.sleep(1)
        self.url = self.info['ads'][0]['callUrl3']['downs'][0]['parameters']
        self.url = beaurl + self.url

        self.code = requests.request('GET', self.url)
        code = str(self.code)[int(str(self.code).find('[')) + 1:int(str(self.code).find(']'))]
        self.assertEqual(code, '204')

        time.sleep(1)
        configPG.connectPG("adx_report")
        self.sql = "select download_completed from public.stats where dsp_app_id='172' and ad_type='2'and ad_group_id='46'and ad_channel_id='645' and ad_customer_id='14257'and imp_type= '1'order by timestamp DESC"
        self.cursor = configPG.executeSQL(self.sql)
        self.result = configPG.get_one(self.cursor)
        print(self.result)

        if self.result[0] == 1:
            self.assertEqual(self.result[0], 1)
            print("PGdb download_completed is test seccussfully!")
        else:
            self.assertEqual(self.result[0], 1)
            print("PGdb download_completed test failed")

    def checkInstl(self):
        """
        test install_start data collection of beaconhub
        :return:
        """
        self.info = self.return_json.json()
        time.sleep(1)

        beaurl = self.info['ads'][0]['adxBeaconUrl']
        time.sleep(1)
        self.url = self.info['ads'][0]['callUrl3']['instl'][0]['parameters']
        self.url = beaurl + self.url

        self.code = requests.request('GET', self.url)
        code = str(self.code)[int(str(self.code).find('[')) + 1:int(str(self.code).find(']'))]
        self.assertEqual(code, '204')

        time.sleep(1)
        configPG.connectPG("adx_report")
        self.sql = "select install_start from public.stats where dsp_app_id='172' and ad_type='2'and ad_group_id='46'and ad_channel_id='645' and ad_customer_id='14257'and imp_type= '1'order by timestamp DESC"
        self.cursor = configPG.executeSQL(self.sql)
        self.result = configPG.get_one(self.cursor)
        print(self.result)

        if self.result[0] == 1:
            self.assertEqual(self.result[0], 1)
            print("PGdb install_start is test seccussfully!")
        else:
            self.assertEqual(self.result[0], 1)
            print("PGdb install_start test failed")

    def checkOpenexists(self):
        """
        test app_open data collection of beaconhub
        :return:
        """
        self.info = self.return_json.json()
        time.sleep(1)

        beaurl = self.info['ads'][0]['adxBeaconUrl']
        time.sleep(1)
        self.url = self.info['ads'][0]['callUrl3']['openexists'][0]['parameters']
        self.url = beaurl + self.url

        self.code = requests.request('GET', self.url)
        code = str(self.code)[int(str(self.code).find('[')) + 1:int(str(self.code).find(']'))]
        self.assertEqual(code, '204')

        time.sleep(1)
        configPG.connectPG("adx_report")
        self.sql = "select app_open from public.stats where dsp_app_id='172' and ad_type='2'and ad_group_id='46'and ad_channel_id='645' and ad_customer_id='14257'and imp_type= '1'order by timestamp DESC"
        self.cursor = configPG.executeSQL(self.sql)
        self.result = configPG.get_one(self.cursor)
        print(self.result)

        if self.result[0] == 1:
            self.assertEqual(self.result[0], 1)
            print("PGdb app_open is test seccussfully!")
        else:
            self.assertEqual(self.result[0], 1)
            print("PGdb app_open test failed")

    def checkInsls(self):
        """
        test install_completed data collection of beaconhub
        :return:
        """
        self.info = self.return_json.json()
        time.sleep(1)

        beaurl = self.info['ads'][0]['adxBeaconUrl']
        time.sleep(1)
        self.url = self.info['ads'][0]['callUrl3']['insls'][0]['parameters']
        self.url = beaurl + self.url

        self.code = requests.request('GET', self.url)
        code = str(self.code)[int(str(self.code).find('[')) + 1:int(str(self.code).find(']'))]
        self.assertEqual(code, '204')

        time.sleep(1)
        configPG.connectPG("adx_report")
        self.sql = "select install_completed from public.stats where dsp_app_id='172' and ad_type='2'and ad_group_id='46'and ad_channel_id='645' and ad_customer_id='14257'and imp_type= '1'order by timestamp DESC"
        self.cursor = configPG.executeSQL(self.sql)
        self.result = configPG.get_one(self.cursor)
        print(self.result)

        if self.result[0] == 1:
            self.assertEqual(self.result[0], 1)
            print("PGdb install_completed is test seccussfully!")
        else:
            self.assertEqual(self.result[0], 1)
            print("PGdb install_completed test failed")

    def checkOpen(self):
        """
        test app_activated data collection of beaconhub
        :return:
        """
        self.info = self.return_json.json()
        time.sleep(1)

        beaurl = self.info['ads'][0]['adxBeaconUrl']
        time.sleep(1)
        self.url = self.info['ads'][0]['callUrl3']['open'][0]['parameters']
        self.url = beaurl + self.url

        self.code = requests.request('GET', self.url)
        code = str(self.code)[int(str(self.code).find('[')) + 1:int(str(self.code).find(']'))]
        self.assertEqual(code, '204')

        time.sleep(1)
        configPG.connectPG("adx_report")
        self.sql = "select app_activated from public.stats where dsp_app_id='172' and ad_type='2'and ad_group_id='46'and ad_channel_id='645' and ad_customer_id='14257'and imp_type= '1'order by timestamp DESC"
        self.cursor = configPG.executeSQL(self.sql)
        self.result = configPG.get_one(self.cursor)
        print(self.result)

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

        beaurl = self.info['ads'][0]['adxBeaconUrl']
        time.sleep(1)
        self.url = self.info['ads'][0]['callUrl3']['active2'][0]['parameters']
        self.url = beaurl + self.url

        self.code = requests.request('GET', self.url)
        code = str(self.code)[int(str(self.code).find('[')) + 1:int(str(self.code).find(']'))]
        self.assertEqual(code, '204')

        time.sleep(1)
        configPG.connectPG("adx_report")
        self.sql = "select active2 from public.stats where dsp_app_id='172' and ad_type='2'and ad_group_id='46'and ad_channel_id='645' and ad_customer_id='14257'and imp_type= '1'order by timestamp DESC"
        self.cursor = configPG.executeSQL(self.sql)
        self.result = configPG.get_one(self.cursor)
        print(self.result)

        if self.result[0] == 1:
            self.assertEqual(self.result[0], 1)
            print("PGdb active2 is test seccussfully!")
        else:
            self.assertEqual(self.result[0], 1)
            print("PGdb active2 test failed")

    def checkTodsprequest(self):
        """
        test c2s_dsp_request data collection of beaconhub
        :return:
        """
        self.info = self.return_json.json()
        time.sleep(1)

        beaurl = self.info['ads'][0]['adxBeaconUrl']
        time.sleep(1)
        self.url = self.info['ads'][0]['callUrl3']['todsprequest'][0]['parameters']
        self.url = beaurl + self.url

        self.code = requests.request('GET', self.url)
        code = str(self.code)[int(str(self.code).find('[')) + 1:int(str(self.code).find(']'))]
        self.assertEqual(code, '204')

        time.sleep(1)
        configPG.connectPG("adx_report")
        self.sql = "select c2s_dsp_request from public.stats where dsp_app_id='172' and ad_type='2'and ad_group_id='46'and ad_channel_id='645' and ad_customer_id='14257'and imp_type= '1'order by timestamp DESC"
        self.cursor = configPG.executeSQL(self.sql)
        self.result = configPG.get_one(self.cursor)
        print(self.result)

        if self.result[0] == 1:
            self.assertEqual(self.result[0], 1)
            print("PGdb c2s_dsp_request is test seccussfully!")
        else:
            self.assertEqual(self.result[0], 1)
            print("PGdb c2s_dsp_request test failed")

    def checkDspissued(self):
        """
        test c2s_dsp_issued data collection of beaconhub
        :return:
        """
        self.info = self.return_json.json()
        time.sleep(1)

        beaurl = self.info['ads'][0]['adxBeaconUrl']
        time.sleep(1)
        self.url = self.info['ads'][0]['callUrl3']['dspissued'][0]['parameters']
        self.url = beaurl + self.url

        self.code = requests.request('GET', self.url)
        code = str(self.code)[int(str(self.code).find('[')) + 1:int(str(self.code).find(']'))]
        self.assertEqual(code, '204')

        time.sleep(1)
        configPG.connectPG("adx_report")
        self.sql = "select c2s_dsp_issued from public.stats where dsp_app_id='172' and ad_type='2'and ad_group_id='46'and ad_channel_id='645' and ad_customer_id='14257' and imp_type= '1'order by timestamp DESC"
        self.cursor = configPG.executeSQL(self.sql)
        self.result = configPG.get_one(self.cursor)
        print(self.result)

        if self.result[0] == 1:
            self.assertEqual(self.result[0], 1)
            print("PGdb c2s_dsp_issued is test seccussfully!")
        else:
            self.assertEqual(self.result[0], 1)
            print("PGdb c2s_dsp_issued test failed")

    def checkPicdownloadstart(self):
        """
        test pic_download_start data collection of beaconhub
        :return:
        """
        self.info = self.return_json.json()
        time.sleep(1)

        beaurl = self.info['ads'][0]['adxBeaconUrl']
        time.sleep(1)
        self.url = self.info['ads'][0]['callUrl3']['picdownloadstart'][0]['parameters']
        self.url = beaurl + self.url

        self.code = requests.request('GET', self.url)
        code = str(self.code)[int(str(self.code).find('[')) + 1:int(str(self.code).find(']'))]
        self.assertEqual(code, '204')

        time.sleep(1)
        configPG.connectPG("adx_report")
        self.sql = "select pic_download_start from public.stats where dsp_app_id='172' and ad_type='2'and ad_group_id='46'and ad_channel_id='645' and ad_customer_id='14257'and imp_type= '1'order by timestamp DESC"
        self.cursor = configPG.executeSQL(self.sql)
        self.result = configPG.get_one(self.cursor)
        print(self.result)

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

        beaurl = self.info['ads'][0]['adxBeaconUrl']
        time.sleep(1)
        self.url = self.info['ads'][0]['callUrl3']['picdownloadcompleted'][0]['parameters']
        self.url = beaurl + self.url

        self.code = requests.request('GET', self.url)
        code = str(self.code)[int(str(self.code).find('[')) + 1:int(str(self.code).find(']'))]
        self.assertEqual(code, '204')

        time.sleep(1)
        configPG.connectPG("adx_report")
        self.sql = "select pic_download_completed from public.stats where dsp_app_id='172' and ad_type='2'and ad_group_id='46'and ad_channel_id='645' and ad_customer_id='14257'and imp_type= '1'order by timestamp DESC"
        self.cursor = configPG.executeSQL(self.sql)
        self.result = configPG.get_one(self.cursor)
        print(self.result)

        if self.result[0] == 1:
            self.assertEqual(self.result[0], 1)
            print("PGdb pic_download_completed is test seccussfully!")
        else:
            self.assertEqual(self.result[0], 1)
            print("PGdb pic_download_completed test failed")

    def checkPicdownloadfailed(self):
        """
        test pic_download_failed data collection of beaconhub
        :return:
        """
        self.info = self.return_json.json()
        time.sleep(1)

        beaurl = self.info['ads'][0]['adxBeaconUrl']
        time.sleep(1)
        self.url = self.info['ads'][0]['callUrl3']['picdownloadfailed'][0]['parameters']
        self.url = beaurl + self.url

        self.code = requests.request('GET', self.url)
        code = str(self.code)[int(str(self.code).find('[')) + 1:int(str(self.code).find(']'))]
        self.assertEqual(code, '204')

        time.sleep(1)
        configPG.connectPG("adx_report")
        self.sql = "select pic_download_failed from public.stats where dsp_app_id='172' and ad_type='2'and ad_group_id='46'and ad_channel_id='645' and ad_customer_id='14257'and imp_type= '1'order by timestamp DESC"
        self.cursor = configPG.executeSQL(self.sql)
        self.result = configPG.get_one(self.cursor)
        print(self.result)

        if self.result[0] == 1:
            self.assertEqual(self.result[0], 1)
            print("PGdb pic_download_failed is test seccussfully!")
        else:
            self.assertEqual(self.result[0], 1)
            print("PGdb pic_download_failed test failed")

    def checkGiveup(self):
        """
        test give_up data collection of beaconhub
        :return:
        """
        self.info = self.return_json.json()
        time.sleep(1)

        beaurl = self.info['ads'][0]['adxBeaconUrl']
        time.sleep(1)
        self.url = self.info['ads'][0]['callUrl3']['giveup'][0]['parameters']
        self.url = beaurl + self.url

        self.code = requests.request('GET', self.url)
        code = str(self.code)[int(str(self.code).find('[')) + 1:int(str(self.code).find(']'))]
        self.assertEqual(code, '204')

        time.sleep(1)
        configPG.connectPG("adx_report")
        self.sql = "select give_up from public.stats where dsp_app_id='172' and ad_type='2'and ad_group_id='46'and ad_channel_id='645' and ad_customer_id='14257'and imp_type= '1'order by timestamp DESC"
        self.cursor = configPG.executeSQL(self.sql)
        self.result = configPG.get_one(self.cursor)
        print(self.result)

        if self.result[0] == 1:
            self.assertEqual(self.result[0], 1)
            print("PGdb give_up is test seccussfully!")
        else:
            self.assertEqual(self.result[0], 1)
            print("PGdb give_up test failed")

    def checkUrljump(self):
        """
        test url_jump data collection of beaconhub
        :return:
        """
        self.info = self.return_json.json()
        time.sleep(1)

        beaurl = self.info['ads'][0]['adxBeaconUrl']
        time.sleep(1)
        self.url = self.info['ads'][0]['callUrl3']['urljump'][0]['parameters']
        self.url = beaurl + self.url

        self.code = requests.request('GET', self.url)
        code = str(self.code)[int(str(self.code).find('[')) + 1:int(str(self.code).find(']'))]
        self.assertEqual(code, '204')

        time.sleep(1)
        configPG.connectPG("adx_report")
        self.sql = "select url_jump from public.stats where dsp_app_id='172' and ad_type='2'and ad_group_id='46'and ad_channel_id='645' and ad_customer_id='14257'and imp_type= '1'order by timestamp DESC"
        self.cursor = configPG.executeSQL(self.sql)
        self.result = configPG.get_one(self.cursor)
        print(self.result)

        if self.result[0] == 1:
            self.assertEqual(self.result[0], 1)
            print("PGdb url_jump is test seccussfully!")
        else:
            self.assertEqual(self.result[0], 1)
            print("PGdb url_jump test failed")

    def checkManualclosebutton(self):
        """
        test menual_close_button data collection of beaconhub
        :return:
        """
        self.info = self.return_json.json()
        time.sleep(1)

        beaurl = self.info['ads'][0]['adxBeaconUrl']
        time.sleep(1)
        self.url = self.info['ads'][0]['callUrl3']['manualclosebutton'][0]['parameters']
        self.url = beaurl + self.url

        self.code = requests.request('GET', self.url)
        code = str(self.code)[int(str(self.code).find('[')) + 1:int(str(self.code).find(']'))]
        self.assertEqual(code, '204')

        time.sleep(1)
        configPG.connectPG("adx_report")
        self.sql = "select menual_close_button from public.stats where dsp_app_id='172' and ad_type='2'and ad_group_id='46'and ad_channel_id='645' and ad_customer_id='14257'and imp_type= '1'order by timestamp DESC"
        self.cursor = configPG.executeSQL(self.sql)
        self.result = configPG.get_one(self.cursor)
        print(self.result)

        if self.result[0] == 1:
            self.assertEqual(self.result[0], 1)
            print("PGdb menual_close_button is test seccussfully!")
        else:
            self.assertEqual(self.result[0], 1)
            print("PGdb menual_close_button test failed")

    def checkAutoclosebutton(self):
        """
        test auto_close_button data collection of beaconhub
        :return:
        """
        self.info = self.return_json.json()
        time.sleep(1)

        beaurl = self.info['ads'][0]['adxBeaconUrl']
        time.sleep(1)
        self.url = self.info['ads'][0]['callUrl3']['autoclosebutton'][0]['parameters']
        self.url = beaurl + self.url

        self.code = requests.request('GET', self.url)
        code = str(self.code)[int(str(self.code).find('[')) + 1:int(str(self.code).find(']'))]
        self.assertEqual(code, '204')

        time.sleep(1)
        configPG.connectPG("adx_report")
        self.sql = "select auto_close_button from public.stats where dsp_app_id='172' and ad_type='2'and ad_group_id='46'and ad_channel_id='645' and ad_customer_id='14257'and imp_type= '1'order by timestamp DESC"
        self.cursor = configPG.executeSQL(self.sql)
        self.result = configPG.get_one(self.cursor)
        print(self.result)

        if self.result[0] == 1:
            self.assertEqual(self.result[0], 1)
            print("PGdb auto_close_button is test seccussfully!")
        else:
            self.assertEqual(self.result[0], 1)
            print("PGdb auto_close_button test failed")

    def checkInstallremindfailed(self):
        """
        test install_remind_failed data collection of beaconhub
        :return:
        """
        self.info = self.return_json.json()
        time.sleep(1)

        beaurl = self.info['ads'][0]['adxBeaconUrl']
        time.sleep(1)
        self.url = self.info['ads'][0]['callUrl3']['installremindfailed'][0]['parameters']
        self.url = beaurl + self.url

        self.code = requests.request('GET', self.url)
        code = str(self.code)[int(str(self.code).find('[')) + 1:int(str(self.code).find(']'))]
        self.assertEqual(code, '204')

        time.sleep(1)
        configPG.connectPG("adx_report")
        self.sql = "select install_remind_failed from public.stats where dsp_app_id='172' and ad_type='2'and ad_group_id='46'and ad_channel_id='645' and ad_customer_id='14257'and imp_type= '1'order by timestamp DESC"
        self.cursor = configPG.executeSQL(self.sql)
        self.result = configPG.get_one(self.cursor)
        print(self.result)

        if self.result[0] == 1:
            self.assertEqual(self.result[0], 1)
            print("PGdb install_remind_failed is test seccussfully!")
        else:
            self.assertEqual(self.result[0], 1)
            print("PGdb install_remind_failed test failed")

    def checkNewsimpression(self):
        """
        test news_impression data collection of beaconhub
        :return:
        """
        self.info = self.return_json.json()
        time.sleep(1)

        beaurl = self.info['ads'][0]['adxBeaconUrl']
        time.sleep(1)
        self.url = self.info['ads'][0]['callUrl3']['newsimpression'][0]['parameters']
        self.url = beaurl + self.url

        self.code = requests.request('GET', self.url)
        code = str(self.code)[int(str(self.code).find('[')) + 1:int(str(self.code).find(']'))]
        self.assertEqual(code, '204')

        time.sleep(1)
        configPG.connectPG("adx_report")
        self.sql = "select news_impression from public.stats where dsp_app_id='172' and ad_type='2'and ad_group_id='46'and ad_channel_id='645' and ad_customer_id='14257'and imp_type= '1'order by timestamp DESC"
        self.cursor = configPG.executeSQL(self.sql)
        self.result = configPG.get_one(self.cursor)
        print(self.result)

        if self.result[0] == 1:
            self.assertEqual(self.result[0], 1)
            print("PGdb news_impression is test seccussfully!")
        else:
            self.assertEqual(self.result[0], 1)
            print("PGdb news_impression test failed")

    def checkNewsclick(self):
        """
        test news_click data collection of beaconhub
        :return:
        """
        self.info = self.return_json.json()
        time.sleep(1)

        beaurl = self.info['ads'][0]['adxBeaconUrl']
        time.sleep(1)
        self.url = self.info['ads'][0]['callUrl3']['newsclick'][0]['parameters']
        self.url = beaurl + self.url

        self.code = requests.request('GET', self.url)
        code = str(self.code)[int(str(self.code).find('[')) + 1:int(str(self.code).find(']'))]
        self.assertEqual(code, '204')

        time.sleep(1)
        configPG.connectPG("adx_report")
        self.sql = "select news_click from public.stats where dsp_app_id='172' and ad_type='2'and ad_group_id='46'and ad_channel_id='645' and ad_customer_id='14257'and imp_type= '1'order by timestamp DESC"
        self.cursor = configPG.executeSQL(self.sql)
        self.result = configPG.get_one(self.cursor)
        print(self.result)

        if self.result[0] == 1:
            self.assertEqual(self.result[0], 1)
            print("PGdb news_click is test seccussfully!")
        else:
            self.assertEqual(self.result[0], 1)
            print("PGdb news_click test failed")

    def checkDownloadfailed(self):
        """
        test download_failed data collection of beaconhub
        :return:
        """
        self.info = self.return_json.json()
        time.sleep(1)

        beaurl = self.info['ads'][0]['adxBeaconUrl']
        time.sleep(1)
        self.url = self.info['ads'][0]['callUrl3']['downloadfailed'][0]['parameters']
        self.url = beaurl + self.url

        self.code = requests.request('GET', self.url)
        code = str(self.code)[int(str(self.code).find('[')) + 1:int(str(self.code).find(']'))]
        self.assertEqual(code, '204')

        time.sleep(1)
        configPG.connectPG("adx_report")
        self.sql = "select download_failed from public.stats where dsp_app_id='172' and ad_type='2'and ad_group_id='46'and ad_channel_id='645' and ad_customer_id='14257'and imp_type= '1'order by timestamp DESC"
        self.cursor = configPG.executeSQL(self.sql)
        self.result = configPG.get_one(self.cursor)
        print(self.result)

        if self.result[0] == 1:
            self.assertEqual(self.result[0], 1)
            print("PGdb download_failed is test seccussfully!")
        else:
            self.assertEqual(self.result[0], 1)
            print("PGdb download_failed test failed")


    def checkInstallfailed(self):
        """
        test install_failed data collection of beaconhub
        :return:
        """
        self.info = self.return_json.json()
        time.sleep(1)

        beaurl = self.info['ads'][0]['adxBeaconUrl']
        time.sleep(1)
        self.url = self.info['ads'][0]['callUrl3']['installfailed'][0]['parameters']
        self.url = beaurl + self.url

        self.code = requests.request('GET', self.url)
        code = str(self.code)[int(str(self.code).find('[')) + 1:int(str(self.code).find(']'))]
        self.assertEqual(code, '204')

        time.sleep(1)
        configPG.connectPG("adx_report")
        self.sql = "select install_failed from public.stats where dsp_app_id='172' and ad_type='2'and ad_group_id='46'and ad_channel_id='645' and ad_customer_id='14257'and imp_type= '1'order by timestamp DESC"
        self.cursor = configPG.executeSQL(self.sql)
        self.result = configPG.get_one(self.cursor)
        print(self.result)

        if self.result[0] == 1:
            self.assertEqual(self.result[0], 1)
            print("PGdb install_failed is test seccussfully!")
        else:
            self.assertEqual(self.result[0], 1)
            print("PGdb install_failed test failed")

    def checkActive2failed(self):
        """
        test install_failed data collection of beaconhub
        :return:
        """
        self.info = self.return_json.json()
        time.sleep(1)

        beaurl = self.info['ads'][0]['adxBeaconUrl']
        time.sleep(1)
        self.url = self.info['ads'][0]['callUrl3']['active2failed'][0]['parameters']
        self.url = beaurl + self.url

        self.code = requests.request('GET', self.url)
        code = str(self.code)[int(str(self.code).find('[')) + 1:int(str(self.code).find(']'))]
        self.assertEqual(code, '204')

        time.sleep(1)
        configPG.connectPG("adx_report")
        self.sql = "select active2_failed from public.stats where dsp_app_id='172' and ad_type='2'and ad_group_id='46'and ad_channel_id='645' and ad_customer_id='14257'and imp_type= '1'order by timestamp DESC"
        self.cursor = configPG.executeSQL(self.sql)
        self.result = configPG.get_one(self.cursor)
        print(self.result)

        if self.result[0] == 1:
            self.assertEqual(self.result[0], 1)
            print("PGdb active2_failed is test seccussfully!")
        else:
            self.assertEqual(self.result[0], 1)
            print("PGdb active2_failed test failed")

    def checkActive3(self):
        """
        test install_failed data collection of beaconhub
        :return:
        """
        self.info = self.return_json.json()
        time.sleep(1)

        beaurl = self.info['ads'][0]['adxBeaconUrl']
        time.sleep(1)
        self.url = self.info['ads'][0]['callUrl3']['active3'][0]['parameters']
        self.url = beaurl + self.url

        self.code = requests.request('GET', self.url)
        code = str(self.code)[int(str(self.code).find('[')) + 1:int(str(self.code).find(']'))]
        self.assertEqual(code, '204')

        time.sleep(1)
        configPG.connectPG("adx_report")
        self.sql = "select active3 from public.stats where dsp_app_id='172' and ad_type='2'and ad_group_id='46'and ad_channel_id='645' and ad_customer_id='14257'and imp_type= '1'order by timestamp DESC"
        self.cursor = configPG.executeSQL(self.sql)
        self.result = configPG.get_one(self.cursor)
        print(self.result)

        if self.result[0] == 1:
            self.assertEqual(self.result[0], 1)
            print("PGdb active3 is test seccussfully!")
        else:
            self.assertEqual(self.result[0], 1)
            print("PGdb active3 test failed")

    def checkActive3failed(self):
        """
        test install_failed data collection of beaconhub
        :return:
        """
        self.info = self.return_json.json()
        time.sleep(1)

        beaurl = self.info['ads'][0]['adxBeaconUrl']
        time.sleep(1)
        self.url = self.info['ads'][0]['callUrl3']['active3failed'][0]['parameters']
        self.url = beaurl + self.url

        self.code = requests.request('GET', self.url)
        code = str(self.code)[int(str(self.code).find('[')) + 1:int(str(self.code).find(']'))]
        self.assertEqual(code, '204')

        time.sleep(1)
        configPG.connectPG("adx_report")
        self.sql = "select active3_failed from public.stats where dsp_app_id='172' and ad_type='2'and ad_group_id='46'and ad_channel_id='645' and ad_customer_id='14257'and imp_type= '1'order by timestamp DESC"
        self.cursor = configPG.executeSQL(self.sql)
        self.result = configPG.get_one(self.cursor)
        print(self.result)

        if self.result[0] == 1:
            self.assertEqual(self.result[0], 1)
            print("PGdb active3_failed is test seccussfully!")
        else:
            self.assertEqual(self.result[0], 1)
            print("PGdb active3_failed test failed")

    def testS2s1(self):
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
        json_path = os.path.join(readConfig.proDir, "testFile","json","s2s1.json")
        json = configHttp.load_json(json_path)
        print("第三步：设置发送请求的参数")

        self.return_json = requests.request("POST", url, json = json)
        print(self.return_json.json())

        method = str(self.return_json.request)[int(str(self.return_json.request).find('['))+1:int(str(self.return_json.request).find(']'))]
        print("第四步：发送请求\n\t\t请求方法："+method)

        # check result
        print("第五步：检查Http请求结果")
        self.checkResult()

        print("第六步：校验PGdb数据")
        self.checkPGdb()

        print("第七步：检验Show节点上报数据")
        self.checkShow()

        print("第八步：检验Click节点上报数据")
        self.checkClick()

        print("第九步：检验Down节点上报数据")
        self.checkDown()

        print("第十步：检验Downs节点上报数据")
        self.checkDowns()

        print("第十一步:检验Instal节点上报数据")
        self.checkInstl()

        print("第十二步:检验Insls节点上报数据")
        self.checkInsls()

        print("第十三步:检验openexists节点上报数据")
        self.checkOpenexists()

        print("第十四步:检验open节点上报数据")
        self.checkOpen()

        print("第十五步:检验active2节点上报数据")
        self.checkActive2()

        print("第十六步:检验todsprequest节点上报数据")
        self.checkTodsprequest()

        print("第十七步:检验dspissued节点上报数据")
        self.checkDspissued()

        print("第十八步:检验picdownloadstart节点上报数据")
        self.checkPicdownloadstart()

        print("第十九步:检验picdownloadcompleted节点上报数据")
        self.checkPicdownloadcompleted()

        print("第二十步:检验picdownloadfailed节点上报数据")
        self.checkPicdownloadfailed()

        print("第二十一步:检验giveup节点上报数据")
        self.checkGiveup()

        print("第二十二步:检验urljump节点上报数据")
        self.checkUrljump()

        print("第二十三步:检验manualclosebutton节点上报数据")
        self.checkManualclosebutton()

        print("第二十四步:检验autoclosebutton节点上报数据")
        self.checkAutoclosebutton()

        print("第二十五步:检验installremindfailed节点上报数据")
        self.checkInstallremindfailed()

        print("第二十六步:检验newsimpression节点上报数据")
        self.checkNewsimpression()

        print("第二十七步:检验newsclick节点上报数据")
        self.checkNewsclick()

        print("第二十八步:检验downloadfailed节点上报数据")
        self.checkDownloadfailed()

        print("第二十九步:检验installfailed节点上报数据")
        self.checkInstallfailed()

        print("第三十步:检验active2_failed节点上报数据")
        self.checkActive2failed()

        print("第三十一步:检验active3节点上报数据")
        self.checkActive3()

        print("第三十二步:检验active3_failed节点上报数据")
        self.checkActive3failed()


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

    def checkcode(self):
        """
        check test result
        :return:
        """
        if self.code == '204':
            self.assertEqual(self.code, '204')
        print("Http request code is 204")

















