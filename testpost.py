import requests
import unittest
import urllib,urllib3
import re
from bs4 import BeautifulSoup
import xml.dom.minidom
from xml.etree import ElementTree

def login(loginName,password,validateCode,url,headers):
    """
    login adx or aigo system
    :param
    :return
    """
    session = requests.session()
    body = {"loginName" : loginName,"password":password,"validateCode":validateCode}
    result = session.request('GET',url,headers=headers,params=body)
    cookies = requests.utils.dict_from_cookiejar(session.cookies)
    return cookies

url = 'http://adx74:8080/loginAuthc'
header_dict = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko'}
cookies = login(loginName='admin',password='admin',validateCode='9527',url=url,headers=header_dict)
# session = requests.session()
# body = {"loginName" : "zhangjiaojiao","password":"zhangjiaojiao","validateCode":"9527"}
# re = session.request('GET',url,headers=header_dict,params=body)

print(cookies)

# cookies = requests.utils.dict_from_cookiejar(session.cookies)
# print(cookies)
url = 'http://adx74:8080/report/page?dateType=day&dimension=dsp0_s2s&pageId=0&dspApiType=1&_=1550211013379'
req = requests.request('GET',url,headers=header_dict,cookies=cookies)

print(req.content)

req.text.__contains__('"bidRequests_Content_0">5')


# url = 'http://192.168.0.245:8585/pub/save?navTabId=pagePub&callbackType=closeCurrent'
# keywords = {
#         'id':'258',
#         'devIsShow':'1',
#         'isUpdatePassword':'false',
#         'password':'pbkdf2_sha512_base64$10000$L0LxILSZposjsWvp$b9BDP94OzlXSXmXlvmB9ax5+KGacUnRvNi6HLCIC+aqdBZZzL0qVQfP6YQs86/rwfO/coNXP5UQYdfIAdBlfFA==',
#         'auditStatus':'1',
#         'auditReason':'',
#         'name':'测试_meng',
#         'type':'0',
#         'email':'meng@163.com',
#         'passwordAlt':'********',
#         'province':'010',
#         'city':'50',
#         'address':'fsfewrw',
#         'linkman':'meng',
#         'phone':'13537564862',
#         'web':'',
#         'qq':'912753456',
#         'status':'1',
#         'billDate':'1',
#         'settleDate':'1'
#         }
# r = requests.post(url,data=keywords,headers=header_dict,cookies=cookies)
# print(r.text)