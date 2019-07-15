# -*- coding:UTF-8 -*-
import pymysql
import readConfig as readConfig
from common.Log import MyLog as Log


localReadConfig = readConfig.ReadConfig()


class MyDB:
    # global host, username, password, port, database, config
    # host = localReadConfig.get_db("host")
    # username = localReadConfig.get_db("username")
    # password = localReadConfig.get_db("password")
    # port = localReadConfig.get_db("port")
    # database = localReadConfig.get_db("database")
    # config = {
    #     'host': str(host),
    #     'user': username,
    #     'passwd': password,
    #     'port': int(port),
    #     'db': database
    # }

    def __init__(self):
        self.log = Log.get_log()
        self.logger = self.log.get_logger()
        self.db = None
        self.cursor = None

    def mysqlDB(self, host, username, passwd, ports, dbase, sql):
        """
        connect to database
        :return:
        """
        try:
            # connect to DB
            self.db = pymysql.connect(host=host,user=username,password=passwd,port=ports,db=dbase)
            # create cursor
            # self.cursor = self.db.cursor()
            print("Connect DB successfully!")
            cursor = self.db.cursor()
            cursor.execute(sql)
            self.db.commit()
            return cursor.fetchone()
        except ConnectionError as ex:
            self.logger.error(str(ex))
        self.db.close()


    def executeSQL(self, sql ):
        """
        execute sql
        :param sql:
        :return:
        """
        # self.connectDB( self.host, self.username, self.passwd, self.ports, self.dbase)
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
        value = self.cursor.fetchone()
        return value

    def closeDB(self):
        """
        close database
        :return:
        """
        self.db.close()
        print("Database closed!")

