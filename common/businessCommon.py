from common import common
from common import configHttp
import readConfig as readConfig
import urllib


localReadConfig = readConfig.ReadConfig()
localConfigHttp = configHttp.ConfigHttp()
localLogin_xls = common.get_xls("adx.xls", "adx")


# login
def login():
    """
    login
    :return: token
    """
    # set url
   # url = {"url": localLogin_xls[0][3]}
    #localConfigHttp.set_url(url)

    # set header
    header = localReadConfig.get_headers("header")
    localConfigHttp.set_headers(header)

    # set param
    #data = {"id": localLogin_xls[0][3]}
    #localConfigHttp.set_data(data)

    # login
    response = localConfigHttp.postWithJson().json()
    #token = common.get_value_from_return_json(response, "member", "token")
    #return token

    # set json
    json = {"json": localLogin_xls[0][4]}
    localConfigHttp.set_json(json)


# logout
def logout(token):
    """
    logout
    :param token: login token
    :return:
    """
    # set url
    url = localConfigHttp.set_url("url")
    localConfigHttp.set_url(url)

    # set header
    #header = {'token': token}
    header = localReadConfig.get_headers("header")
    localConfigHttp.set_headers(header)

    # logout
    localConfigHttp.get()


