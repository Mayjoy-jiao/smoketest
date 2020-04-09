"""
    测试内容
        1.点击率下限（全天）和点击率下限（分钟）的限制，当实际点击率（天）小于设置的点击率下限（全天） 或 5分钟内点击率小于设置点击率下限（分钟） 停止二类任务
        2.请求预下发二类广告时需要带当天时间，其他时间无法请求广告
    测试环境：与发布
    使用开发者广告为：kbf98iko
    dsp应用：adxDsp_363_4
"""
import unittest
import paramunittest
import psycopg2
import json
import readConfig as readConfig
import os
import time
import requests
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
class Test_click_lower_limit(unittest.TestCase):

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

    def tearDown(self):
        print("测试结束，输出log完结\n\n")

    def get_5min_section(self, n):
        """
        获取5分钟倍数的时间段
        :param n: 分钟
        :return: 返回时间段
        """
        star_end__min_time = []
        for i in range(0, 12):
            min = range(5 * i, 5 * (i + 1))
            if n in min:
                start = n - (n - 5 * i)
                end = n + (5 * (i + 1) - n)
                if end == 60:
                    end=59
                    star_end__min_time.append(start)
                    star_end__min_time.append(end)
                else:
                    star_end__min_time.append(start)
                    star_end__min_time.append(end)

                return star_end__min_time

    def get_star_end_time(self):
        """
        获取当前时间在最近的5分钟的时间区间，如：11：04 ，返回时间段为【11：00-11：05）
        :return:
        """
        star_end__time = []
        data = time.localtime(time.time())
        data1 = time.strftime("%Y-%m-%d", data)
        star_min_time = self.get_5min_section(data.tm_min)[0]
        end_min_time = self.get_5min_section(data.tm_min)[1]
        star_time = '{} {}:{}:00'.format(data1, data.tm_hour, star_min_time)
        end_time = '{} {}:{}:59'.format(data1, data.tm_hour, end_min_time)
        star_end__time.append(star_time)
        star_end__time.append(end_time)
        return star_end__time

    def construct_click_rate(self, n, payload_1, payload_2, url_1, url_2):  # ,payload_1,payload_2,url_1,url_2
        """
        构造点击率
        :param n:执行几次循环，一次循环：申请1次一类广告，上报1次展示，上报一次点击；申请一次2类，上报1次2类展示
        :param payload_1: 一类广告请求的上行
        :param payload_2: 二类广告请求的上行
        :param url_1: 一类广告请求的接口地址
        :param url_2: 二类类广告请求的接口地址
        :return:
        """
        for i in range(n):
            res_1 = requests.post(url_1, json=payload_1).json()
            reqId_1 = res_1['reqId']
            print(f"一类{res_1}")
            if len(res_1['ads']) == 0:
                print("没有一类广告返回")
            else:
                # report_show_url = "https://beaconhub-dev.iadmob.com/api/v1/adx/beacon?id={}&ag_template=:ZZ_TEMPLATE:&ag_img_width=:ZZ_IMG_WIDTH:&ag_img_height=:ZZ_IMG_HEIGHT:&ag_placement_width=:ZZ_PLACEMENT_WIDTH:&ag_placement_height=:ZZ_PLACEMENT_HEIGHT:&t=7&ad_id=1".format(
                #     reqId_1)
                report_show_url = "https://beaconhub-stage.iadmob.com/api/v1/adx/beacon?id={}&ag_template=:ZZ_TEMPLATE:&ag_img_width=:ZZ_IMG_WIDTH:&ag_img_height=:ZZ_IMG_HEIGHT:&ag_placement_width=:ZZ_PLACEMENT_WIDTH:&ag_placement_height=:ZZ_PLACEMENT_HEIGHT:&t=7&ad_id=1".format(
                    reqId_1)
                requests.get(report_show_url)
                print("一类展示")
                time.sleep(2)
                # report_click_url = "https://beaconhub-dev.iadmob.com/api/v1/adx/beacon?id={}&ag_template=:ZZ_TEMPLATE:&ag_img_width=:ZZ_IMG_WIDTH:&ag_img_height=:ZZ_IMG_HEIGHT:&ag_placement_width=:ZZ_PLACEMENT_WIDTH:&ag_placement_height=:ZZ_PLACEMENT_HEIGHT:&t=9&ad_id=1&ag_dx_a=:ZZ_DX_A:&ag_dy_a=:ZZ_DY_A:&ag_ux_a=:ZZ_UX_A:&ag_uy_a=:ZZ_UY_A:&ag_dx_r=:ZZ_DX_R:&ag_dy_r=:ZZ_DY_R:&ag_ux_r=:ZZ_UX_R:&ag_uy_r=:ZZ_UY_R:&time=:ZZ_TIME_S:&ag_width=:ZZ_WIDTH:&ag_height=:ZZ_HEIGHT:".format(
                #     reqId_1)
                report_click_url = "https://beaconhub-stage.iadmob.com/api/v1/adx/beacon?id={}&ag_template=:ZZ_TEMPLATE:&ag_img_width=:ZZ_IMG_WIDTH:&ag_img_height=:ZZ_IMG_HEIGHT:&ag_placement_width=:ZZ_PLACEMENT_WIDTH:&ag_placement_height=:ZZ_PLACEMENT_HEIGHT:&t=9&ad_id=1&ag_dx_a=:ZZ_DX_A:&ag_dy_a=:ZZ_DY_A:&ag_ux_a=:ZZ_UX_A:&ag_uy_a=:ZZ_UY_A:&ag_dx_r=:ZZ_DX_R:&ag_dy_r=:ZZ_DY_R:&ag_ux_r=:ZZ_UX_R:&ag_uy_r=:ZZ_UY_R:&time=:ZZ_TIME_S:&ag_width=:ZZ_WIDTH:&ag_height=:ZZ_HEIGHT:".format(
                    reqId_1)
                requests.get(report_click_url)
                print("一类点击")
                time.sleep(2)

            res_2 = requests.post(url_2, json=payload_2).json()
            print(f"二类{res_2}")
            reqId_2 = res_2['reqId']
            if len(res_2['ads']) == 0:
                print("没有二类广告返回")
            else:
                time.sleep(3)
                # report_show_url_2 = "https://beaconhub-dev.iadmob.com/api/v1/adx/beacon?id={}&ag_template=:ZZ_TEMPLATE:&ag_img_width=:ZZ_IMG_WIDTH:&ag_img_height=:ZZ_IMG_HEIGHT:&ag_placement_width=:ZZ_PLACEMENT_WIDTH:&ag_placement_height=:ZZ_PLACEMENT_HEIGHT:&t=8&ad_id=1".format(
                #     reqId_2)
                report_show_url_2 = "https://beaconhub-stage.iadmob.com/api/v1/adx/beacon?id={}&ag_template=:ZZ_TEMPLATE:&ag_img_width=:ZZ_IMG_WIDTH:&ag_img_height=:ZZ_IMG_HEIGHT:&ag_placement_width=:ZZ_PLACEMENT_WIDTH:&ag_placement_height=:ZZ_PLACEMENT_HEIGHT:&t=8&ad_id=1".format(
                    reqId_2)
                requests.get(report_show_url_2)
                print("二类展示")
                time.sleep(2)

    def get_click_rate(self, dsp_app_id, ad_type):
        """
        获取全天和最近5分钟的点击率
        :return:
        """
        click_rate_by_day_and_min = []
        # payload_1 = {
        #     "id": "554af654-99f1-4de2-9663-65d4f487f29a",
        #     "apiVersion": "10",
        #     "app": {
        #         "id": "lghdc2bl",
        #         "name": "com.zzcm.wtwd",
        #         "version": "1.0.0"
        #     },
        #     "device": {
        #         "did": "864230036377784",
        #         "type": 1,
        #         "os": 1,
        #         "osVersion": "6.0",
        #         "vendor": "HONOR",
        #         "model": "NEM-AL10",
        #         "ua": "Mozilla/5.0 (Linux; Android 5.1.1; vivo X7 Build/LMY47V) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/39.0.0.0 Mobile Safari/537.36",
        #         "connType": 1,
        #         "androidId": "2b1822e7afaab2e4",
        #         "imsi": "",
        #         "height": 1812,
        #         "width": 1080,
        #         "carrier": 1,
        #         "dpi": 480,
        #         "mac": "44:c3:46:f4:6b:05",
        #         "ip": "112.95.161.57",
        #         "isForeignIp": 0
        #     },
        #     "geo": {
        #         "latitude": 22.544177,
        #         "longitude": 113.944334,
        #         "timestamp": 1515034624700
        #     },
        #     "adSlot": {
        #         "id": "tikv1jna",
        #         "size": {
        #             "width": 640,
        #             "height": 100
        #         },
        #         "minCpm": 0,
        #         "orientation": 1
        #     },
        #     "adSources": [
        #         {
        #             "dspCode": "",
        #             "dspAppId": -1,
        #             "adSlotId": ""
        #         }
        #     ],
        #     "extInfo": {
        #         "channelId": "QD_001",
        #         "subChannelId": "QDS_001",
        #         "mid": "ssiddca98c74423142258b994801ed9f7726",
        #         "sdkVersion": "V.1.17071700(ZZ)",
        #         "adGroupId": 39
        #     }
        # }
        # payload_2 = {
        #     "id": "2add876779da45b29a2c6c6e04be9879",
        #     "apiVersion": "10.0",
        #     "app": {
        #         "id": "lghdc2bl",
        #         "name": "com.guaguagua.com",
        #         "version": "4.0"
        #     },
        #     "device": {
        #         "did": "86339602226431586339602226431500",
        #         "type": 1,
        #         "os": 1,
        #         "osVersion": "4.2.2",
        #         "vendor": "nubia",
        #         "model": "NX403A",
        #         "ua": "Mozilla/5.0 (Linux; U; Android 4.2.2; zh-cn; NX403A Build/JDQ39) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.32",
        #         "connType": 1,
        #         "androidId": "d1cd48fa22550f89",
        #         "imsi": "460016756228219",
        #         "height": 1280,
        #         "width": 720,
        #         "carrier": 2,
        #         "dpi": 320,
        #         "mac": "98:6c:f5:26:6a:d3",
        #         "ip": "199.168.0.6",
        #         "isForeignIp": 0
        #     },
        #     "geo": {
        #         "latitude": 0.0,
        #         "longitude": 0.0,
        #         "timestamp": 1562860799
        #     },
        #     "adSlot": {
        #         "id": "adxDsp_156_1",
        #         "size": {
        #             "width": 640,
        #             "height": 960
        #         },
        #         "minCpm": 0,
        #         "orientation": 0
        #     },
        #     "adSign": 0,
        #     "extInfo": {
        #         "channelId": "QD_001",
        #         "subChannelId": "QDS_001",
        #         "mid": "ssiddca98c74423142258b994801ed9f7726",
        #         "sdkVersion": "V.1.17071700(ZZ)",
        #         "adGroupId": 39,
        #         "preRequestTs": 1563206400000
        #     }
        # }
        # payload_1 = common.get_request_json("s2s_1_json",appid="x0sgbymi", channelId="CL88", subChannelId="0001", mid="ssiddca98c74423142258b994801ed9f7794", adid="kbf98iko")
        # payload_2 = common.get_request_json("s2s_2_json",appid="x0sgbymi", channelId="CL88", subChannelId="0001", mid="ssiddca98c74423142258b994801ed9f7794",  confingid="adxDsp_363_4")
        payload_1 = common.get_request_json("s2s_1_json",appid="x0sgbymi", channelId="CL88", subChannelId="0001", mid="ssiddca98c74423142258b994801ed9f7794", adid="kbf98iko")
        payload_2 = common.get_request_json("s2s_2_json",appid="x0sgbymi", channelId="CL88", subChannelId="0001", mid="ssiddca98c74423142258b994801ed9f7794", confingid="adxDsp_363_4")
        # url_1 = "http://192.168.0.77:4400/api/v1/adx/1"
        # url_2= "http://192.168.0.77:4400/api/v1/adx/2"
        url_1 = "https://bid-stage.iadmob.com/api/v1/adx/1"
        url_2 = "https://bid-stage.iadmob.com/api/v1/adx/2"
        self.construct_click_rate(1, payload_1, payload_2, url_1, url_2)  # 调用构造点击率方法

        search_time = self.get_star_end_time()  # 获取当前时间段的5分钟区间值

        show_count_min_sql = "select sum(impressions),sum(impression2)as sum2 ,sum(click) as click from stats_b where dsp_app_id={0} and ad_type={1} and timestamp >= '{2}' and timestamp < '{3}';".format(
            dsp_app_id, ad_type, str(search_time[0]), str(search_time[1]))
        click_count_min_sql = "select sum(click) from stats_b where dsp_app_id={0} and ad_type={1} and timestamp >= '{2}' and timestamp < '{3}';".format(
            dsp_app_id, ad_type, str(search_time[0]), str(search_time[1]))
        # conn = psycopg2.connect(database="adx_report", user="root", password="aszx", host="192.168.0.66",
        #                         port="5432")
        conn = psycopg2.connect(database="adx_report", user="adxroot", password="adxroot321", host="113.31.86.153",
                                port="65432")
        cur = conn.cursor()
        cur.execute(show_count_min_sql)
        show = cur.fetchall()
        print(show)
        show_count = int(show[0][0]) + int(show[0][1])  # 不能直接相加？
        print(f"5分钟之内的展示数{show_count}次")

        cur.execute(click_count_min_sql)
        click_count = cur.fetchall()[0][0]
        if click_count == None:
            click_count = 0

        if click_count == 0:
            click_rate = 0
        else:
            print("最近5分钟的点击数为{}".format(float(click_count)))
            click_rate_by_min = float(click_count) / float(show_count)
            print("最近5分钟的点击率为{}".format(click_rate_by_min))
            click_rate_by_day_and_min.append(click_rate_by_min)

        show_count_day_sql = "select  sum(impressions),sum(impression2) from stats_b_by_day where dsp_app_id={0} and ad_type={1} and timestamp >='{2} 00:00:00';".format(
            dsp_app_id, ad_type, time.strftime("%Y-%m-%d", time.localtime(time.time())))
        click_count_day_sql = "select  sum(click) from stats_b_by_day where dsp_app_id={0} and ad_type={1} and timestamp >='{2} 00:00:00';".format(
            dsp_app_id, ad_type, time.strftime("%Y-%m-%d", time.localtime(time.time())))
        # print(click_count_min_sql)
        cur.execute(show_count_day_sql)
        show_day = cur.fetchall()
        show_count_by_day = show_day[0][0] + show_day[0][1]  # 不能直接相加？
        print("一天的展示数为{}".format(show_count_by_day))

        cur.execute(click_count_day_sql)
        click_count_day = cur.fetchall()[0][0]
        if click_count_day == None:
            click_count = 0
        if click_count == 0:
            click_rate_by_day = 0
        else:
            print("全天点击数:{}".format(float(click_count_day)))
            click_rate_by_day = float(click_count_day) / float(show_count_by_day)
        print("全天点击率:{}".format(click_rate_by_day))
        click_rate_by_day_and_min.append(click_rate_by_day)
        conn.close()
        return click_rate_by_day_and_min

    def get_click_rate_limit_config(self,dsp_app_id, ad_type):
        click_rate_limit_config=[]
        print("第一步：获取dsp应用的配置的全天和分钟的下限值")
        limit_by_day = "select banner_min_ctr from dsp_app where id={};".format(dsp_app_id)
        limit_by_min = "select click_rate_min_ctr_by_minute from dsp_app_ad_config where dsp_app_id={0} and ad_type={1};".format(dsp_app_id, ad_type)

        # click_rate_limit_day = float(configDB.mysqlDB('192.168.0.223', 'zzmanager', 'iadMOB-2013@0622)', 3306, 'ssp',limit_by_day)[0])/100.00
        # click_rate_limit_min = float(configDB.mysqlDB('192.168.0.223', 'zzmanager', 'iadMOB-2013@0622)', 3306, 'ssp',limit_by_min)[0])/100.00
        click_rate_limit_day = float(configDB.mysqlDB('113.31.86.153', 'zzmanager', 'iadMOB-2013@0622)', 3306, 'ssp',limit_by_day)[0])/100.00
        click_rate_limit_min = float(configDB.mysqlDB('113.31.86.153', 'zzmanager', 'iadMOB-2013@0622)', 3306, 'ssp',limit_by_min)[0])/100.00

        click_rate_limit_config.append(click_rate_limit_day)
        click_rate_limit_config.append(click_rate_limit_min)

        return click_rate_limit_config

    def get_current_data_time(self):
        """
        获取当前时间的0点到23：59：59 的时间戳，并转化为毫秒
        :return:
        """
        effective_time = []
        print(time.time())  # 获取当前时间戳
        print(time.localtime(time.time()))  # 获取当前时间的年月日时分秒等
        test_time = time.strftime("%Y-%m-%d", time.localtime(time.time()))  # 获取当前日期
        print(test_time)
        st = '{0} 00:00:00'.format(test_time)  # 需要转换的日期
        et = '{0} 23:59:59'.format(test_time)

        star_timeArray = time.strptime(st, "%Y-%m-%d %H:%M:%S")  # 将日期转换为时间数据组
        end_timeArray = time.strptime(et, "%Y-%m-%d %H:%M:%S")

        start_timeStamp = int(time.mktime(star_timeArray)) * 1000  # 转换成时间戳
        end_timeStamp = int(time.mktime(end_timeArray)) * 1000

        effective_time.append(start_timeStamp)
        effective_time.append(end_timeStamp)

        return effective_time

    def test_click_lower_limit(self):
        """
        测试当前实际天点击率小于设置点击率下限（全天） 或者 当前5分钟内的实际点击率小于设置的点击率下限（分钟），则生情不到二类广告，不执行二类任务
        :return:
        """
        # click_rate_limit=self.get_click_rate_limit_config(156,1)
        click_rate_limit = self.get_click_rate_limit_config(363, 4)
        click_rate_limit_day = click_rate_limit[0]
        click_rate_limit_min = click_rate_limit[1]
        print(f"设置的点击下限（分钟）为:{click_rate_limit_min}")
        print(f"设置的点击下限（全天）为:{click_rate_limit_day}")

        # current_click_rate = self.get_click_rate(156, 1)
        current_click_rate = self.get_click_rate(363, 4)
        # 判断如果当前实际的天点击率 小于 设置的点击率下限（天） 或者 当前分钟的实际点击下限  小于 设置的点击下限（分钟），则请求不到二类广告，否着，继续执行二类
        if current_click_rate[0] <= click_rate_limit_min or current_click_rate[1] <= click_rate_limit_day:
            # pagload = {
            #     "id": "2add876779da45b29a2c6c6e04be9879",
            #     "apiVersion": "10.0",
            #     "app": {
            #         "id": "",
            #         "name": "com.guaguagua.com",
            #         "version": "4.0"
            #     },
            #     "device": {
            #         "did": "86339602226431586339602226431500",
            #         "type": 1,
            #         "os": 1,
            #         "osVersion": "4.2.2",
            #         "vendor": "nubia",
            #         "model": "NX403A",
            #         "ua": "Mozilla/5.0 (Linux; U; Android 4.2.2; zh-cn; NX403A Build/JDQ39) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.32",
            #         "connType": 1,
            #         "androidId": "d1cd48fa22550f89",
            #         "imsi": "460016756228219",
            #         "height": 1280,
            #         "width": 720,
            #         "carrier": 2,
            #         "dpi": 320,
            #         "mac": "98:6c:f5:26:6a:d3",
            #         "ip": "199.168.0.6",
            #         "isForeignIp": 0
            #     },
            #     "geo": {
            #         "latitude": 0.0,
            #         "longitude": 0.0,
            #         "timestamp": 1562860799
            #     },
            #     "adSlot": {
            #         "id": "adxDsp_156_1",
            #         "size": {
            #             "width": 640,
            #             "height": 960
            #         },
            #         "minCpm": 0,
            #         "orientation": 0
            #     },
            #     "adSign": 0,
            #     "extInfo": {
            #         "channelId": "{{channelId}}",
            #         "subChannelId": "{{subChannelId}}",
            #         "mid": "{{mid}}",
            #         "sdkVersion": "V.1.17071700(ZZ)",
            #         "adGroupId": 39,
            #         "preRequestTs": 1563206400000
            #     }
            # }
            # url_2 = "http://192.168.0.77:4400/api/v1/adx/2"
            url_2= "https://bid-stage.iadmob.com/api/v1/adx/2"
            pagload = common.get_request_json("s2s_2_json",appid="x0sgbymi", channelId="CL88", subChannelId="0001", mid="ssiddca98c74423142258b994801ed9f7794", confingid="adxDsp_363_4")
            for i in range(1):
                res_2 = requests.post(url_2, json=pagload).json()
                time.sleep(2)
                ads = len(res_2["ads"])
                self.assertEqual(ads, 0, "不下发二类广告")
        else:
            print("继续执行二类")

    def test_get_ad2_by_time(self,commit_time = int(time.time()*1000)):
        """
        测试预下发二类广告，只有带有当前时间的，才下发预下发二类广告
        :return:
        """
        # commit_time = int(time.time()*1000)
        effective_time = self.get_current_data_time()
        print(f"有效时间范围：{effective_time}")
        url = "https://bid-stage.iadmob.com/api/v1/adx/2"
        pagload = common.get_request_json("s2s_2_y_json", appid="x0sgbymi", channelId="CL88", subChannelId="0001",mid="ssiddca98c74423142258b994801ed9f7794",  confingid="adxDsp_363_4")
        print(pagload)
        res = requests.post(url, json=pagload).json()
        print(res)
        time.sleep(2)
        if commit_time > effective_time[1] or commit_time < effective_time[0]:
            self.assertEqual(len(res["ads"]),0,"没有预下发二类返回")
            pass
        else:
            self.assertIsNot(len(res["ads"]),0,"有预下发二类返回")


