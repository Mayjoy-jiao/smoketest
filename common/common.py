# -*- coding:UTF-8 -*-
import requests
import readConfig as readConfig
import os
from xlrd import open_workbook
from xml.etree import ElementTree as ElementTree
from common import configHttp as configHttp
from common.Log import MyLog as Log
from xlwt import easyxf
import json
import time
import urllib
import hashlib
from xlutils.copy import copy
import jpype
from jpype import *


localReadConfig = readConfig.ReadConfig()
proDir = readConfig.proDir
localConfigHttp = configHttp.ConfigHttp()
log = Log.get_log()
logger = log.get_logger()

caseNo = 0

def runJVM():
    # jvmPath = r'E:\port\javanew\jre\bin\client\jvm.dll'
    jvmPath = jpype.getDefaultJVMPath()
    # jarPath=r'E:\port\protocol-1.0.0.jar'
    jarPath = os.path.join(proDir,'venv','protocol-1.0.0.jar')
    return startJVM(jvmPath, "-ea", "-Djava.class.path=%s"%jarPath )

def stopJVM():
    return shutdownJVM()

def checkSum(jsdata):
    Test=JClass('com.zzcm.protocol.ParserUtil')
    return Test.getCRC(jsdata)

def decrypt(re):
    Test=JClass('com.zzcm.protocol.CodeUtil')
    return Test.getInstance().decrypt(re)

def runaigaoapi(rdata,data_url):

    data = json.dumps(rdata)
    checksum = checkSum(data)
    datas = {'data': data, 'checkSum': checksum}
    Res = requests.post(url=data_url, data=datas).text
    response = decrypt(Res)
    return json.loads(response)

def get_visitor_token():
    """
    create a token for visitor
    :return:
    """
    host = localReadConfig.get_http("BASEURL")
    response = requests.get(host+"/v2/User/Token/generate")
    info = response.json()
    token = info.get("info")
    logger.debug("Create token:%s" % (token))
    return token

def set_visitor_token_to_config():
    """
    set token that created for visitor to config
    :return:
    """
    token_v = get_visitor_token()
    localReadConfig.set_headers("TOKEN_V", token_v)


def get_value_from_return_json(json, name1, name2):
    """
    get value by key
    :param json:
    :param name1:
    :param name2:
    :return:
    """

    info = json[ 'statusCode' ]
    group = info[name1]
    value = group[name2]
    return value

def show_return_msg(response):
    """
    show msg detail
    :param response:
    :return:
    """
    url = response.url
    msg = response.text
    print("\n请求地址："+url)
    # 可以显示中文
    print("\n请求返回值："+'\n'+json.dumps(json.loads(msg), ensure_ascii=False, sort_keys=True, indent=4))
# ****************************** read testCase excel ********************************


def get_xls(xls_name, sheet_name):
    """
    get interface data from xls file
    :return:
    """
    cls = []
    # get xls file's path
    xlsPath = os.path.join(proDir, "testFile", 'case', xls_name)
    # open xls file
    file = open_workbook(xlsPath)
    # get sheet by name
    sheet = file.sheet_by_name(sheet_name)
    # get one sheet's rows
    nrows = sheet.nrows
    for i in range(nrows):
        if sheet.row_values(i)[0] != u'case_name':
            cls.append(sheet.row_values(i))
    return cls

# ****************************** read SQL xml ********************************
database = {}


def set_xml():
    """
    set sql xml
    :return:
    """
    if len(database) == 0:
        sql_path = os.path.join(proDir, "testFile", "SQL.xml")
        tree = ElementTree.parse(sql_path)
        for db in tree.findall("database"):
            db_name = db.get("name")
            # print(db_name)
            table = {}
            for tb in db.getchildren():
                table_name = tb.get("name")
                # print(table_name)
                sql = {}
                for data in tb.getchildren():
                    sql_id = data.get("id")
                    # print(sql_id)
                    sql[sql_id] = data.text
                table[table_name] = sql
            database[db_name] = table


def get_xml_dict(database_name, table_name):
    """
    get db dict by given name
    :param database_name:
    :param table_name:
    :return:
    """
    set_xml()
    database_dict = database.get(database_name).get(table_name)
    return database_dict


def get_sql(database_name, table_name, sql_id):
    """
    get sql by given name and sql_id
    :param database_name:
    :param table_name:
    :param sql_id:
    :return:
    """
    db = get_xml_dict(database_name, table_name)
    sql = db.get(sql_id)
    return sql

def writeExcel( xls_name):
    """
    write reqid to excel
    :param path:
    :return:
    """
    cls = []
    xlsPath = os.path.join(proDir, "testFile", 'case', xls_name)
    rb = open_workbook(xlsPath,formatting_info=True)
    wb = copy(rb)
    sheet = wb.get_sheet(1)
    sheet.write(2,0,'some')
    wb.save(xlsPath)
    return cls

def login(loginName,password,validateCode,url):
    """
    login adx or aigo system
    :param
    :return
    """
    session = requests.session()
    body = {"loginName" : loginName,"password":password,"validateCode":validateCode}
    header_dict = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko'}
    result = session.request('GET',url,headers=header_dict,params=body)
    cookies = requests.utils.dict_from_cookiejar(session.cookies)
    return cookies

def download_js(jsurl):
    req = urllib.request.urlopen(jsurl)
    jsname = "360"
    filename = '/tmp/' + jsname
    if (req.getcode() == 200):
        with open(filename,"wb") as code:
            code.write(req.read())
            return filename

def gethash(filepath):
    f = open(filepath)
    thehash = hashlib.sha1()
    theline = f.readline()
    while (theline):
        thehash.update(theline.encode("utf-8"))
        theline = f.readline()
    hash = thehash.hexdigest()
    print(filepath,"hash is ", hash)
    return hash

def get_dsp_application_config(url, configid):
    """
    获取dsp应用配置信息 /ad/v1/getAdSimConfig
    :param url: 接口地址
    :param configid: dsp应用的广告位id  例如：adxDsp_1_1
    :return: <list>该应用的广告位配置信息
    """

    r = requests.post(url).json()
    res = r["adxDspConfigBean"]
    print(res)
    for i in res:
        if i["configid"] == configid:
            re_config = i
    return re_config

def get_request_json(api,appid=None, channelId=None, subChannelId=None, mid=None, type=0, confingid=None, adid=None,commit_time = int(time.time()*1000)):
    """
    :param api: 接口形式
    :param appid: 开发者应用id
    :param channelId: 渠道id
    :param subChannelId: 子渠道id
    :param mid: mad
    :param type:二类广告的类型 :c2s:1(一类)；2（普通2类）；3（预下发二类）；4（dsp sdk补充）
    :param confingid: dsp应用广告位id ，C2S中，可能是个列表，如["adxDsp_212_1"]
    :param adid: 开发者广告位id
    :param commit_time: 预下发二类广告请求的有效时间
    :return:
    """
    s2s_1_json = {
    "id":"554af654-99f1-4de2-9663-65d4f487f29a",
    "apiVersion":"10",
    "app":{
        "id":appid,
        "name":"com.zzcm.wtwd",
        "version":"1.0.0"
    },
    "device":{
        "did":"864230036377784",
        "type":1,
        "os":1,
        "osVersion":"6.0",
        "vendor":"HONOR",
        "model":"NEM-AL10",
        "ua":"Mozilla/5.0 (Linux; Android 5.1.1; vivo X7 Build/LMY47V) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/39.0.0.0 Mobile Safari/537.36",
        "connType":1,
        "androidId":"2b1822e7afaab2e4",
        "imsi":"",
        "height":1812,
        "width":1080,
        "carrier":1,
        "dpi":480,
        "mac":"44:c3:46:f4:6b:05",
        "ip":"112.95.161.57",
        "isForeignIp": 0
    },
    "geo":{
        "latitude":22.544177,
        "longitude":113.944334,
        "timestamp":1515034624700
    },
    "adSlot":{
        "id":adid,
        "size":{
            "width":640,
            "height":100
        },
        "minCpm":0,
        "orientation":1
    },
   "adSources": [
     {
      "dspCode": "",
      "dspAppId": -1,
      "adSlotId":""
     }
   ],
    "extInfo":{
      "channelId": channelId,
      "subChannelId": subChannelId,
      "mid": mid,
      "sdkVersion":"V.1.17071700(ZZ)",
      "adGroupId":39
  }
}
    s2s_2_json = {
  "id" : "2add876779da45b29a2c6c6e04be9879",
  "apiVersion" : "10.0",
  "app" : {
    "id": appid,
    "name" : "com.guaguagua.com",
    "version" : "4.0"
  },
  "device" : {
    "did" : "86339602226431586339602226431500",
    "type" : 1,
    "os" : 1,
    "osVersion" : "4.2.2",
    "vendor" : "nubia",
    "model" : "NX403A",
    "ua" : "Mozilla/5.0 (Linux; U; Android 4.2.2; zh-cn; NX403A Build/JDQ39) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.32",
    "connType" : 1,
    "androidId" : "d1cd48fa22550f89",
    "imsi" : "460016756228219",
    "height" : 1280,
    "width" : 720,
    "carrier" : 2,
    "dpi" : 320,
    "mac" : "98:6c:f5:26:6a:d3",
    "ip" : "199.168.0.6",
    "isForeignIp": 0
  },
  "geo" : {
    "latitude" : 0.0,
    "longitude" : 0.0,
    "timestamp" : 1562860799
  },
  "adSlot" : {
    "id" : confingid,
    "size" : {
      "width" : 640,
      "height" : 960
    },
    "minCpm" : 0,
    "orientation" : 0
  },
  "adSign": type,
  "extInfo":{
      "channelId": channelId,
      "subChannelId": subChannelId,
      "mid": mid,
      "sdkVersion":"V.1.17071700(ZZ)",
      "adGroupId":39,
      "preRequestTs":1563206400000
  }
}
    s2s_2_y_json = {
        "id": "2add876779da45b29a2c6c6e04be9879",
        "apiVersion": "10.0",
        "app": {
            "id": appid,
            "name": "com.guaguagua.com",
            "version": "4.0"
        },
        "device": {
            "did": "86339602226431586339602226431500",
            "type": 1,
            "os": 1,
            "osVersion": "4.2.2",
            "vendor": "nubia",
            "model": "NX403A",
            "ua": "Mozilla/5.0 (Linux; U; Android 4.2.2; zh-cn; NX403A Build/JDQ39) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.32",
            "connType": 1,
            "androidId": "d1cd48fa22550f89",
            "imsi": "460016756228219",
            "height": 1280,
            "width": 720,
            "carrier": 2,
            "dpi": 320,
            "mac": "98:6c:f5:26:6a:d3",
            "ip": "199.168.0.6",
            "isForeignIp": 0
        },
        "geo": {
            "latitude": 0.0,
            "longitude": 0.0,
            "timestamp": 1562860799
        },
        "adSlot": {
            "id": confingid,
            "size": {
                "width": 640,
                "height": 960
            },
            "minCpm": 0,
            "orientation": 0
        },
        "adSign": 1,
        "extInfo": {
            "channelId": channelId,
            "subChannelId": subChannelId,
            "mid": mid,
            "sdkVersion": "V.1.17071700(ZZ)",
            "adGroupId": 39,
            "preRequestTs": commit_time
        }
    }
    c2s_json = {
  "id": "id-123-123",
  "device": {
    "ua": "Mozilla/5.0 (Linux; Android 5.1.1; vivo X7 Build/LMY47V) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/39.0.0.0 Mobile Safari/537.36",
    "make": "Huawei",
    "model": "NEM-AL10",
    "os": "Android",
    "osv": "9.0",
    "mcc": "123456",
    "imsi": "",
    "androidid": "2b1822e7afaab2e4",
    "mac": "44:c3:46:f4:6b:05",
    "imei": "863244036388855",
    "ext": {
      "channelcode": "{{channelId}}",
      "subchannelcode": "{{subChannelId}}",
      "mid": "{{mid}}",
      "sdkversion": "3.2.1",
      "adgroupid": 62,
      "adgrouptype": 2
    }
  },
  "version": "10",
  "imptype": type,
  "ext": {
    "configids": confingid,
      "placements": adid
  }
}
    if api=="s2s_1_json":
        return s2s_1_json
    elif api=="s2s_2_json":
        return s2s_2_json
    elif api == "c2s_json":
        return c2s_json
    elif api == "s2s_2_y_json":
        return s2s_2_y_json
    else:
        return None



if __name__ == "__main__":
    print(get_xls("adx.xls", "adx"))
    #set_visitor_token_to_config()
