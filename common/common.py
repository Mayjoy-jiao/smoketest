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
import urllib
import hashlib
from xlutils.copy import copy


localReadConfig = readConfig.ReadConfig()
proDir = readConfig.proDir
localConfigHttp = configHttp.ConfigHttp()
log = Log.get_log()
logger = log.get_logger()

caseNo = 0


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




if __name__ == "__main__":
    print(get_xls("adx.xls", "adx"))
    #set_visitor_token_to_config()
