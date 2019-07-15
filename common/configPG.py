# -*- coding:UTF-8 -*-
import psycopg2
import readConfig as readConfig
from common.Log import MyLog as Log

localReadConfig = readConfig.ReadConfig()

class PGDB:
    global Host, user, passwd, Port, dbase, Config
    Host = localReadConfig.get_db("host")
    user = localReadConfig.get_db("username")
    passwd = localReadConfig.get_db("password")
    Port = localReadConfig.get_db("port")
    dbase = localReadConfig.get_db("database")
    Config = {
        'host': str(Host),
        'user': user,
        'password': passwd,
        'port': int(Port),
        'database': dbase
    }


    def __init__(self):
        self.log = Log.get_log()
        self.logger = self.log.get_logger()
        self.db = None
        self.cursor = None

    def connectPG(self,puser,passwd,port,hosts,dbbase):
        """
        connect to database
        :return:
        """
        try:
            # connect to DB
            # self.db = psycopg2.connect(user="root",password="aszx",port="5432",host="192.168.0.66",database=dbbase)
            # self.db = psycopg2.connect(user="adxroot", password="adxroot321", port="65432", host="113.31.86.153", database=dbbase)
            self.db = psycopg2.connect(user=puser,password=passwd,port=port,host=hosts,database=dbbase)
            # create cursor
            self.cursor = self.db.cursor()
            print("Connect PG DB successfully!")
        except ConnectionError as ex:
            self.logger.error(str(ex))

    def executeSQL(self,sql):
        """
        execute sql
        :param sql:
        :return:
        """
        # self.connectPG("adx_report")
        # executing sql
        self.cursor.execute(sql)
        # executing by committing to DB
        self.db.commit()
        return self.cursor

    def get_all(self, cursor):
        """
        get all result after execute sql
        :param cursor:
        :return:
        """
        value = cursor.fetchall()
        return value

    def get_one(self, cursor):
        """
        get one result after execute sql
        :param cursor:
        :return:
        """
        value = cursor.fetchone()
        return value

    def closeDB(self):
        """
        close database
        :return:
        """
        self.db.close()
        print("PG Database closed!")


