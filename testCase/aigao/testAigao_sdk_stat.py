"""
测试＂媒体包触发SDK＂的数据上报
SDK应用：测试穿山甲-自动化　横幅－模板：485
包名：com.android.test
包的版本：19090300


测试数据:

360SDK(sdkId:):
投放广告组:    对应广告组ID:
媒体包名：
媒体包版本：
SDK应用名称:       对应sdkAppId:
开屏_自渲染(configid:    renderType:)
信息流_自渲染:(configid:    renderType:)


百度SDK(sdkId:):
投放广告组:    对应广告组ID:
媒体包名：
媒体包版本：
SDK应用名称:       对应sdkAppId:
开屏_自渲染(configid:    renderType:)
信息流_自渲染:(configid:    renderType:)


广点通SDK(sdkId:):
投放广告组:    对应广告组ID:
媒体包名：
媒体包版本：
SDK应用名称:       对应sdkAppId:
开屏_自渲染(configid:    renderType:)
信息流_自渲染:(configid:    renderType:)


穿山甲SDK(sdkId:):
投放广告组:    对应广告组ID:
媒体包名：
媒体包版本：
SDK应用名称:       对应sdkAppId:
开屏_自渲染(configid:    renderType:)
信息流_自渲染:(configid:    renderType:)

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
# common.runJVM()


@paramunittest.parametrized(aigao_xls[0])
class AigaoSdkmediaData(unittest.TestCase):
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

    def postdata_mediasdk(self, type):
        """
        媒体触发SDK数据上报post json data
        :return:
        """
        data = {
            "mid": "ssiddca98c74423142258b994801ed9f7794",
            "appid": "LK1006",
            "network": 1,
            "channelId": "CL88",
            "subChannelId": "0001",
            "version": "1.0.7",
            "cardType": "other",
            "simOp": "",
            "model": "GIONEE S10CL",
            "adCounts": [
                {
                    "adGroupId": "45",
                    "adType": 5,
                    "configid": 715,
                    "mediaPkgName": "com.android.test",
                    "mediaPkgVersion": 19090300,
                    "sdkAppId": 146,
                    "sdkId": "SDK_0002",
                    "renderType": 2,
                    "statNodes": [
                        {
                            "type": type,
                            "count": 3
                        }
                    ]
                }
            ],
            "adCountSeq": round(time.time()) * 1000
        }
        #测试百度－自动化208-6（开屏_模板）数据上报
        # data1 = {
        #     "mid": "ssiddca98c74423142258b994801ed9f775f",
        #     "appid": "LK1006",
        #     "network": 1,
        #     "channelId": "CL88",
        #     "subChannelId": "0001",
        #     "version": "1.0.7",
        #     "cardType": "other",
        #     "simOp": "",
        #     "model": "GIONEE S10CL",
        #     "adCounts": [
        #         {
        #             "adGroupId": "45",
        #             "adType": 3,
        #             "configid": 717,
        #             "mediaPkgName": "com.android.test",
        #             "mediaPkgVersion": 19090300,
        #             "sdkAppId": 146,
        #             "sdkId": "SDK_0002",
        #             "renderType": 1,
        #             "statNodes": [
        #                 {
        #                     "type": type,
        #                     "count": 1
        #                 }
        #             ]
        #         }
        #     ],
        #     "adCountSeq": round(time.time()) * 1000
        # }
        return data

    def postdata_mediaPkg(self, mediaPkgVersion, type):
        """
        媒体升级包数据上报post json data
        上行说明:
        1.请求~下载成功的节点上报上行,媒体包版本号置0
        2.下载成功以后的节点上报上行,要带具体的媒体包版本号

        :return:
        """
        data = {
            "mid": "ssiddca98c74423142258b994801ed9f7794",
            "appid": "LK1006",
            "network": 1,
            "channelId": "CL88",
            "subChannelId": "0001",
            "version": "1.0.7",
            "cardType": "other",
            "simOp": "",
            "model": "GIONEE S10CL",
            "adCounts": [
                {
                    "adGroupId": None,
                    "adType": 0,
                    "configid": None,
                    "mediaPkgName": "com.android.test",
                    "mediaPkgVersion": mediaPkgVersion,
                    "sdkAppId": 0,
                    "sdkId": 0,
                    "renderType": None,
                    "statNodes": [
                        {
                            "type": type,
                            "count": 1
                        }
                    ]
                }
            ],
            "adCountSeq": round(time.time()) * 1000
        }
        return data

    # @unittest.skip("该用例暂不执行")
    def testAigaomediasdkdata(self):
        """
        test body
        :return:
        """
        # set url
        self.url = aigao_xls[0][3]
        print("第一步：设置url  " + self.url)
        # set post data
        print("第二步：设置请求上行　")
        self.type = ['MCPKG', 'MCSUS', 'REQT', 'PULLS', 'PULLF', 'SHOW', 'EXPO', 'SHOWF', 'CLICK', 'CLOSED', 'LANDP',
                     'LEAVP', 'DOWNS', 'INSTS',
                     'OPEN', 'SREQT', 'SPULL', 'SPULF', 'SIMS', 'SEXPO', 'SSHWF', 'SCLSD', 'SBACK', 'ICLSD', 'IBACK',
                     'IACLD', 'DOWN', 'RENDF', 'RENDS',
                     'OPISP', 'OPTAP', 'OPLD', 'SRENDF', 'SRENDS', 'SMCPKG', 'SMCSUS', 'SMCFAT']
        for type in self.type:
            data = self.postdata_mediasdk(type)
            print("第三步：sdk媒体包－穿山甲数据上报请求上行：", data)
            # 请求接口
            res = common.runaigaoapi(data, self.url)
            print("第四步：sdk媒体包－穿山甲数据上报请求下行", res)
            # check result
            print("第五步：验证数据库结果")
            self.checkDBResult(type, 1)
            time.sleep(2)

    # @unittest.skip("该用例暂不执行")
    def testAigao_mediaPkg_stat(self):
        """
        test body
        :return:
        """
        # set url
        self.url = aigao_xls[0][3]
        print("第一步：设置url  " + self.url)
        # set post data
        print("第二步：设置请求上行　")
        """
        上行说明:
        1.请求~下载成功的节点上报上行,媒体包版本号置0
        2.下载成功以后的节点上报上行,要带具体的媒体包版本号
        """
        print("媒体包升级接口请求~下载成功的节点上报")
        self.type_1 = ['MREQT', 'MQUEY', 'MPULL', 'MDOWN', 'MDOWS']
        self.type_2 = ['MBIST', 'MISTS', 'MINSF', 'MUINS', 'MUINF']
        for type in self.type_1:
            data = self.postdata_mediaPkg(0, type)
            print("第三步：媒体包数据上报请求上行：", data)
            # 请求接口
            res = common.runaigaoapi(data, self.url)
            print("第四步：媒体包数据上报请求下行", res)
            # check result
            print("第五步：验证数据库结果")
            self.checkDBResult(type, 0)
            time.sleep(2)

        print("媒体包升级接口下载成功以后的节点上报")
        for type in self.type_2:
            data = self.postdata_mediaPkg(19090300, type)
            print("第三步：媒体包数据上报请求上行：", data)
            # 请求接口
            res = common.runaigaoapi(data, self.url)
            print("第四步：媒体包数据上报请求下行", res)
            # check result
            print("第五步：验证数据库结果")
            self.checkDBResult(type, 0)
            time.sleep(2)

    def tearDown(self):
        """

        :return:
        """

    def checkDBResult(self, type, configid_flag):
        """
        :param type: 上报的节点的名称
        :param configid_flag: 上行configid是否为None 1:不为None 0:为None
        :return:
        """
        date = time.strftime("%Y%m%d", time.localtime())
        sql_table_name = "sdk_stats_day_" + date
        time.sleep(5)
        self.sql1 = "select configid from %s where  channelId='CL88' and operator='%s' and sdkId='SDK_0002' order by create_date desc limit 1" % (
            sql_table_name, type)
        self.sql2 = "select configid from %s where  channelId='CL88' and operator='%s' and sdkId='0' order by create_date desc limit 1" % (
            sql_table_name, type)
        if configid_flag == 1:
            dbresult = ConfigDB.mysqlDB("113.31.86.153", "zzmanager", "iadMOB-2013@0622)", 3306, "iadstat", self.sql1)
            time.sleep(2)
            self.assertEqual(dbresult[0], '715')
        else:
            dbresult = ConfigDB.mysqlDB("113.31.86.153", "zzmanager", "iadMOB-2013@0622)", 3306, "iadstat", self.sql2)
            time.sleep(2)
            self.assertEqual(dbresult[0], None)