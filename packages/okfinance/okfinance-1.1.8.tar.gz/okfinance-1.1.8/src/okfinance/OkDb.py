# coding:utf-8
import pymysql


def connect_db(host, user, password, port, dbname):
    '''
    连接数据库
    :return:
    '''
    db = pymysql.connect(host=host, user=user, password=password, port=port, db=dbname)
    return db
