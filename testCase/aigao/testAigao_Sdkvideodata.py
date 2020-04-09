"""
测试＂媒体包触发SDK＂的数据上报
SDK应用：
测试广点通激励视频－自动化　激励视频：618
爱告SDK协议版本：1.0.7
"""
import time
import unittest
import paramunittest
from common import common
from common.Log import MyLog
import readConfig as readConfig
from common import configHttp as configHttp
from common import configDB as configDB

aigao_xls = common.get_xls("aigao.xlsx", "aigao")
localReadConfig = readConfig.ReadConfig()
localConfigHttp = configHttp.ConfigHttp()
ConfigDB = configDB.MyDB()


@paramunittest.parametrized(aigao_xls[0])
class AigaoSdkVideoData(unittest.TestCase):
    def setParameters(self, case_name, url,method, sql, type, result, code, msg):
        """
        set params
        :param case_name:
        :param url:
        :param method:
        :param sql:
        :param goods_id:
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

    def postdata(self,type):
        """
        post json data
        :return:
        """
        data = {
    "mid": "ssid10abf0504bba4ea7ad5f29e0e8845851",
    "appid": "LK1006",
    "network": 1,
    "channelId": "AU8888",
    "subChannelId": "1",
    "version": "1.0.7",
    "cardType": "unicom",
    "simOp": "46001",
    "model": "GN5003",
    "adCounts": [
        {
            "adGroupId": "48",
            "adType": 6,
            "configid": "618",
            "mediaPkgName": "com.android.test",
            "mediaPkgVersion": 48,
            "sdkAppId": 131,
            "sdkId": "SDK_0001",
            "renderType": 3,
            "statNodes": [
                {
                    "type": type,
                    "count": 1
                }
            ]
        }
    ],
            "adCountSeq": round(time.time())*1000
        }
        return data


    def testAigaovideosdkdata(self):
        """
        test body
        :return:
        """
        # set url
        self.url = aigao_xls[0][3]
        print("第一步：设置url  " + self.url)
        # set post data
        print("第二步：设置请求上行　")
        type = ['MCPKG','MCSUS','CSHOW','CCLICK','EREQT','EREQTN','EPULL','ELOADS','ESHOWF','SHOW','EEXPO','EPLAYE','EREWARD','ECLI1','ECLI2','DOWN','DOWNS','INSTS','OPEN','OPLD','OPTAP','ESTAY',
                    'EBREAK','EPAT','ENADC','ENADCS','ECLO1','ECLO2','ECLO3','ECLO4','EACLO1','EACLO2','EACLO3','EACLO4','EACLO5']
        for self.type in type:
            data = self.postdata(self.type)
            print("第三步：sdk媒体包－广点通激励视频数据上报请求上行：　",data)
            #请求接口
            # common.runJVM()
            res = common.runaigaoapi(data,self.url)
            print("第四步：sdk媒体包－广点通激励视频数据上报请求下行",res)
            # check result
            print("第五步：验证数据库结果")
            self.checkDBResult(self.type)



    def tearDown(self):
        """

        :return:
        """


    def checkDBResult(self,type):
        type = "J_" + type
        date = time.strftime("%Y%m%d", time.localtime())
        sql_table_name = "sdk_stats_day_" + date
        time.sleep(5)
        self.sql = "select configid from %s where  channelId='AU8888' and  operator = '%s' and  sdkId='SDK_0001' order by create_date desc limit 1" % (sql_table_name,type)
        dbresult = ConfigDB.mysqlDB("113.31.86.153", "zzmanager", "iadMOB-2013@0622)", 3306, "iadstat", self.sql)
        print("test data is",type)
        time.sleep(1)
        self.assertEqual(dbresult[0], '618')
