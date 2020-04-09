import time
import unittest
import paramunittest
from common import common
from common.Log import MyLog
import readConfig as readConfig
from common import configHttp as configHttp
from common import configDB as configDB
from common.configDB import MyDB

aigao_xls = common.get_xls("aigao.xlsx", "aigao")
localReadConfig = readConfig.ReadConfig()
localConfigHttp = configHttp.ConfigHttp()
ConfigDB = configDB.MyDB()
# common.runJVM()


@paramunittest.parametrized(aigao_xls[0])
class TestGetChannelConfig(unittest.TestCase):
    def setParameters(self, case_name, url, method, sql, type, result, code, msg):
        """
        set params
        :param case_name:
        :param url:
        :param method:
        :param sql:
        :param type:
        :param result:
        :param code:
        :param msg:
        :return:
        """
        self.case_name = str(case_name)
        self.url = str(url)
        self.method = str(method)
        self.sql = str(sql)
        self.type = str(type)
        self.result = str(result)
        self.code = str(code)
        self.msg = str(msg)
        self.response = None
        self.info = None

    def description(self):
        """

        :return:
        """
        self.case_name

    def setUp(self):
        """

        :return:
        """
        self.log = MyLog.get_log()
        self.logger = self.log.get_logger()

    def tearDown(self):
        pass

    def get_postdata(self,mid,channelId,subChannelId):
        data = {
    "network": "WIFI",
    "sysVersion": "SV.P123.160809(HD)",
    "channelId": channelId,
    "mid": mid,
    "imei": "865625020257042",
    "geoStr": {
        "cellId": "0",
        "mnc": "-1",
        "lbs": {
            "latitude": 0,
            "longitude": 0
        },
        "lac": "0"
    },
    "cardType": "unknown",
    "version": "2.4.8",
    "subChannelId": subChannelId,
    "appid": "LK1006",
    "phoneNumber": "null",
    "imsi": "460011207707575",
    "simOp": "46006"
}
        return data

    def get_channel_config(self):
        data = self.get_postdata("ssiddca98c74423142258b994801ed9f7794","CL88","0001")
        res_data = common.runaigaoapi(data, "http://test.iad.zzay.net/ps/getConfig.do")
        print(res_data)
        return res_data

    def test_channel_config_blackAppANDtriggerApp_01default(self):
        """
        渠道_修改_广告设置_垃圾清理广告组]设置“终极黑名单”、“触发app黑名单”默认值下发
        :return:
        """
        print('第一步：拉取渠道配置')
        res_config = self.get_channel_config()
        print("第二步：查找广告类型（adtype=46）垃圾清理广告组的终极黑名单和触发app黑名单的配置项")
        # 查询数据库中，终极黑名单blackApp->(create_interval)和 触发app黑名单triggerApp->(apk_second_rate)配置项的值
        sql = "select create_interval,apk_second_rate from ad_channel_day_month where config_id='645' and ad_type=46;"
        db_data = MyDB().mysqlDB("113.31.86.153", "zzmanager", "iadMOB-2013@0622)", 3306, "iadsupport", sql)
        print(db_data)
        for i in res_config["adLimit"]:
            if i["adType"] == 46:
                blackApp= i["extData"]["blackApp"]
                triggerApp = i["extData"]["triggerApp"]
                print("验证终极黑名单（blackApp）默认值是否为‘是’")
                self.assertEqual(blackApp, True)
                print("验证触发app黑名单（triggerApp）默认值是否为‘是’")
                self.assertEqual(triggerApp, True)

    def test_channel_config_blackAppANDtriggerApp_02modify(self):
        """
        渠道_修改_广告设置_垃圾清理广告组]设置“终极黑名单”、“触发app黑名单”修改后的值下发
        :return:
        """
        print("第一步:修改广告类型（adtype=46）垃圾清理广告组的终极黑名单和触发app黑名单的配置项")
        # 查询数据库中，终极黑名单blackApp->(create_interval)和 触发app黑名单triggerApp->(apk_second_rate)配置项的值
        sql = "update ad_channel_day_month set create_interval=0,apk_second_rate=0 where config_id='645' and ad_type=46;"
        db_data = MyDB().mysqlDB("113.31.86.153", "zzmanager", "iadMOB-2013@0622)", 3306, "iadsupport", sql)
        print(db_data)
        time.sleep(600)
        print('第二步：拉取渠道配置')
        res_config = self.get_channel_config()

        for i in res_config["adLimit"]:
            if i["adType"] == 46:
                blackApp= i["extData"]["blackApp"]
                triggerApp = i["extData"]["triggerApp"]
                print("验证终极黑名单（blackApp）修改后的值为‘否’")
                self.assertEqual(blackApp, False)
                print("验证触发app黑名单（triggerApp）修改后的值为‘否’")
                self.assertEqual(triggerApp, False)
                print("恢复修改前的默认值")
                MyDB().mysqlDB("113.31.86.153", "zzmanager", "iadMOB-2013@0622)", 3306, "iadsupport", "update ad_channel_day_month set create_interval=1,apk_second_rate=1 where config_id='645' and ad_type=46;")
