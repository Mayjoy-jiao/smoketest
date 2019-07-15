# -*- coding:UTF-8 -*-
import requests
import readConfig as readConfig
import json
from common.Log import MyLog as Log

localReadConfig = readConfig.ReadConfig()


class ConfigHttp:

    def __init__(self):
        global scheme, host, port, timeout
        scheme = localReadConfig.get_http("scheme")
        host = localReadConfig.get_http("baseurl")
        port = localReadConfig.get_http("port")
        timeout = localReadConfig.get_http("timeout")
        self.log = Log.get_log()
        self.logger = self.log.get_logger()
        self.headers = {}
        self.params = {}
        self.data = {}
        self.url = None
        self.files = {}
        self.json = {}
        self.state = 0

    def set_url(self, url):
        """
        set url
        :param: interface url
        :return:
        """
        self.url = scheme+'://'+host+url

    def set_headers(self, header):
        """
        set headers
        :param header:
        :return:
        """
        self.headers = header

    def set_params(self, param):
        """
        set params
        :param param:
        :return:
        """
        self.params = param

    def set_data(self, data):
        """
        set data
        :param data:
        :return:
        """
        self.data = data

    def set_files(self, filename):
        """
        set upload files
        :param filename:
        :return:
        """
        if filename != '':
            file_path = '/home/jiaojiao/download/apiTest/interfaceTest/testFile/img/' + filename
            self.files = {'file': open(file_path, 'rb')}

        if filename == '' or filename is None:
            self.state = 1

    def set_json(self,json_path):
        if json_path != '':
            #json_path = '' + jsonname
            #self.json = {'json': open("/home/jiaojiao/download/apiTest/interfaceTest/testFile/json/zmm.json",encoding= 'utf-8')}
            self.fb = {'json': open(json_path, encoding='utf-8')}
            #json = json.load(self.fb)
            #self.fb.close()
            #return dicts
            print(json)

        if json_path == '' or json_path is None:
            self.state = 1


    def load_json(self,path):
        import json
        lines = []     #  第一步：定义一个列表， 打开文件
        with open(path,encoding='utf8') as f:
            for row in f.readlines(): # 第二步：读取文件内容
                if row.strip().startswith("//"):   # 第三步：对每一行进行过滤
                    continue
                lines.append(row)                   # 第四步：将过滤后的行添加到列表中.
        return json.loads("\n".join(lines))

    # defined http get method

    def get(self):
        """
        defined get method
        :return:
        """
        try:
            response = requests.get(self.url, headers=self.headers, params=self.params, timeout=float(timeout))
            # response.raise_for_status()
            return response
        except TimeoutError:
            self.logger.error("Time out!")
            return None

    # defined http post method
    # include get params and post data
    # uninclude upload file

    # defined http post method
    # include upload file
    def postWithFile(self):
        """
        defined post method
        :return:
        """
        try:
            response = requests.post(self.url, headers=self.headers, data=None, json=self.json, timeout=float(timeout))

            return response
        except TimeoutError:
            self.logger.error("Time out!")
            return None


if __name__ == "__main__":
    print("ConfigHTTP")
