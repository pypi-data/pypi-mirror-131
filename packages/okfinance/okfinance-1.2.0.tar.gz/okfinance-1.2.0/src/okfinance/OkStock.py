# coding:utf-8

import datetime
import time

import requests


def get_day_type(query_date):
    url = 'http://tool.bitefu.net/jiari/?d=' + query_date
    content = requests.get(url).text
    if content:
        try:
            day_type = int(content)
        except ValueError:
            return -1
        else:
            return day_type
    else:
        return -1


def is_tradeday(query_date):
    '''
        判断传入日期是否交易日，返回1是0否,参数格式(%Y%m%d)
    '''
    weekday = datetime.datetime.strptime(query_date, '%Y%m%d').isoweekday()
    if weekday <= 5 and get_day_type(query_date) == 0:
        return 1
    else:
        return 0


def today_is_tradeday():
    '''
        判断今天是否交易日，返回1是0否
    '''
    query_date = datetime.datetime.strftime(datetime.datetime.today(), '%Y%m%d')
    return is_tradeday(query_date)


def get_ymd():
    '''
        获取当前年月日,格式(%Y-%m-%d)
    '''
    return time.strftime("%Y-%m-%d", time.localtime())


def get_ymd2():
    '''
    获取当前年月日,格式(%Y%m%d)
    '''
    return time.strftime("%Y%m%d", time.localtime())
