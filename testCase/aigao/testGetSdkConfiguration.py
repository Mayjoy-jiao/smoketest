"""
	5.1.3.208-3
	2018-8-20
	预发布环境中：
	渠道：CL88-0001 ，mid:ssiddca98c74423142258b994801ed9f7794 ,将渠道分别投放到以下SDK应用的广告位中：
		测试穿山甲-自动化（横幅_模板）： 协议版本2
		测试穿山甲－自动化1.0（信息流(自渲染)）：协议版本1
		测试百度-自动化（插屏_模板）：协议版本1.0.7
		测试百度－自动化1.0（开屏_模板）：协议版本1.0.6
	将以上广告位的支持触发方式选择为： 【SDK应用管理-广告位设置】
		穿山甲：应用内媒体SDK
		百度：桌面SDK
	渠道设置中，确定以上4个应用在支持触发方式内被勾选上，【渠道-SDK-SDK投设置】
	渠道设置中，确认渠道的应用总开关，开启了“应用内媒体SDK”和“桌面SDK”
	5.1.3.208-3 SDK配置新增下发配置默认值：
	countdownTime:5
	countdownRate:0
	disableBackKey1:true
	disableBackKey2:true
	bgTemplateClickRate:100

	5.1.3.208-6 返回字段新增"bgTemplateClickMultiple"  --背景可点击大小倍数
	360SDK_自动化208-6 （信息流(自渲染)） configid：721
"""
import unittest
import paramunittest
from common import common
from common.Log import MyLog
from common.configDB import MyDB

aigao_xls = common.get_xls("aigao.xlsx", "aigao")
# common.runJVM()

# @paramunittest.parametrized(aigao_xls[1])
class TestGetSdkConfiguration(unittest.TestCase):
	def setParameters(self, case_name, url, method, token, goods_id, result, code, msg):
		"""

		:param case_name:
		:param url:
		:param method:
		:param token:
		:param goods_id:
		:param result:
		:param code:
		:param msg:
		:return:
		"""
		self.case_name = str(case_name)
		self.url = str(url)
		self.method = str(method)
		self.token = str(token)
		self.goodsId = str(goods_id)
		self.result = str(result)
		self.code = str(code)
		self.msg = str(msg)
		self.response = None
		self.info = None

	def description(self):
		self.case_name

	def setUp(self):
		self.log = MyLog.get_log()
		self.logger = self.log.get_logger()


	def tearDown(self):
		pass

	def get_data(self,version,mediaSdkVersion):
		data = {
		"channelId": "CL88",
		"mid": "ssiddca98c74423142258b994801ed9f7794",
		"imei": "865625020257042",
		"version": version,
		"subChannelId": "0001",
		"appid": "LK1006",
		"imsi": "460011207707575",
		"showType": "1,2",
		"mediaSdkVersion":mediaSdkVersion,
		"mediaPkgName":"",
		"sdkConfs": []
	}
		return data

	def testGetSdkConfig(self):
		config_id1 = []
		config_id2 = []
		# self.url2 = 'http://test.iad.zzay.net/ps/getSdkConfig.do'
		self.url2 = aigao_xls[1][3]
		print(self.url2)
		config_data = common.runaigaoapi(self.get_data("1.0.7", 2), self.url2)["configs"]
		for i in config_data:
			config_id1.append(i["configid"])
			if i["configid"] == '534':
				print("断言接口新增返回字段的默认值：")
				self.assertEqual(i["countdownTime"], 5)
				self.assertEqual(i["countdownRate"], 0)
				self.assertEqual(i["disableBackKey1"], False)
				self.assertEqual(i["disableBackKey2"], False)
				self.assertEqual(i["bgTemplateClickRate"], 100)
		print(f"断言高协议版本可以拉取低版本的配置，拉取广告位配置为：{config_id1}")
		self.assertListEqual(['485', '503', '516', '534'],config_id1)
		config_data = common.runaigaoapi(self.get_data("1.0.6", 1), self.url2)["configs"]
		for i in config_data:
			config_id2.append(i["configid"])
		print(f"断言低协议版本不能拉取低版本的配置，拉取广告位配置为：{config_id2}")
		self.assertListEqual(['516', '534'], config_id2)

	def test_assert_bgTemplateClickMultiple(self):
		"""
		测试背景点击倍数下发准确
		:return:
		"""
		config_id = []
		self.url2 = aigao_xls[1][3]
		print(self.url2)
		data = common.runaigaoapi(self.get_data("1.0.7", 3), self.url2)
		config_data = data["configs"]
		for i in config_data:
			config_id.append(i["configid"])
			if i["configid"] == '721':
				print(f"断言5.1.3.208-6 新增bgTemplateClickMultiple字段值下发正确")
				sql = 'SELECT bg_template_click_multiple from ad_channel_sdk_app_setting where config_id=645 and sdk_ad_setting_id=721;'
				bg_data = float(MyDB().mysqlDB("113.31.86.153", "zzmanager", "iadMOB-2013@0622)", 3306, "iadsupport", sql)[0])
				self.assertEqual(i["bgTemplateClickMultiple"], bg_data)

	def test_assert_downloadWakeSwitch(self):
		"""
				测试背景点击倍数下发准确
				:return:
				"""
		self.url2 = aigao_xls[1][3]
		print(self.url2)
		data = common.runaigaoapi(self.get_data("1.0.7", 3), self.url2)
		print(f"断言5.1.3.208-6 下载保活开关downloadWakeSwitch字段默认值为False")
		sql1 = "select download_wake_switch from ad_channel_sdk_user_group_config where config_id='645';"
		# 查询数据库中CL88-0001 的保活设置的值
		downloadWakeSwitch = MyDB().mysqlDB("113.31.86.153", "zzmanager", "iadMOB-2013@0622)", 3306, "iadsupport", sql1)[0]
		print(downloadWakeSwitch)
		print(data["downloadWakeSwitch"])
		self.assertEqual(data["downloadWakeSwitch"], downloadWakeSwitch)

