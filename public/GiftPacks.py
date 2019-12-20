#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    GiftPacks
    ~~~~~
    A python tools collections which contains DB,Transaction,allow_cross,ApiResponse,Presto,File, et al.
    @Author: ziyezhang
    @date: 2019-08-28
"""
import pymysql
import configparser
import time
import os
import re
import json
import codecs
import csv
from flask import make_response
from public.logger import Logger
from werkzeug.utils import find_modules, import_string
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.schedulers.background import BackgroundScheduler

logger = Logger(__name__)


def load_module(app):
    for dir in os.listdir("."):
        if os.path.isdir(dir) and re.match(r"(.*)_api", dir) is not None:
            for name in find_modules(dir):
                module = import_string(name)
                print("Loading API Module: %s" % name)
                app.register_blueprint(module.blue_print, url_prefix="/giftPacks/api")


def get_config(section, key):
    cp = configparser.ConfigParser()
    cp.read("public/GiftPacks.config")
    if not cp.has_section(section):
        raise ValueError('DB section does not exit')
    return cp.get(section, key)


def today():
    return time.strftime('%Y%m%d', time.localtime(time.time()))


def ApiResponse(code, data, message=None):
    """

    :rtype: object
    """
    if message is None:
        return json.dumps(dict(code=code, data=data), ensure_ascii=False)
    return json.dumps(dict(code=code, msg=message), ensure_ascii=False)


class FlaskConfig:
    swaggerConf = {
        'uiversion': 3,
        'openapi': '3.0.2',
        'title': 'API GiftPacks',
        'description': '元气满满',
        'version': '2.0',
        'specs_route': '/giftPacks/apidocs',
    }
    basePath = "/giftPacks"


class CODE:
    success = 0
    failure = -1


class STATE:
    running = 1
    finished = 2
    error = -1


class TIME:
    @staticmethod
    def now():
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))


class DB:
    def __init__(self, conf, section):
        cp = configparser.ConfigParser()
        cp.read("conf/%s.conf" % conf)
        if not cp.has_section(section):
            raise ValueError('config section does not exit')
        self.host = cp.get(section, "host")
        self.port = cp.get(section, "port")
        self.user = cp.get(section, "user")
        self.passwd = cp.get(section, "passwd")
        self.schema = cp.get(section, "schema")
        self.connect = pymysql.connect(host=self.host, port=int(self.port), user=self.user, passwd=self.passwd,
                                       db=self.schema, charset="utf8")

    def select(self, sql, index=None, limit=None) -> object:
        cursor = self.connect.cursor()
        try:
            if index is not None and limit is not None and sql.find("SQL_CALC_FOUND_ROWS") == -1 and sql.find("limit") == -1:
                sql = sql.replace("select", "select SQL_CALC_FOUND_ROWS")
                sql += " limit %d,%d" % (int(index), int(limit))
                cursor.execute(sql)
                data = cursor.fetchall()
                cursor.execute("select FOUND_ROWS()")
                total_count = cursor.fetchone()[0]
                return dict(data=data, total_count=total_count)
            else:
                cursor.execute(sql)
                return cursor.fetchall()
        except Exception as e:
            logger.error("Error: select error -- %s -- error info:%s" % (sql, str(e)))
            return None

    def select_page(self, sql: str, index: int, limit: int) -> dict:
        cursor = self.connect.cursor()
        try:
            if sql.find("SQL_CALC_FOUND_ROWS") == -1 and sql.find("limit") == -1:
                sql = sql.replace("select", "select SQL_CALC_FOUND_ROWS")
                sql += " limit %d,%d" % (int(index), int(limit))
            cursor.execute(sql)
            data = cursor.fetchall()
            cursor.execute("select FOUND_ROWS()")
            total_count = cursor.fetchone()[0]
            return dict(data=data, total_count=total_count)
        except Exception as e:
            logger.error("Error: select error -- %s -- error info:%s" % (sql, str(e)))
            return data(data=list(), total_count=0)

    def insert(self, sql):
        cursor = self.connect.cursor()
        try:
            cursor.execute(sql)
            self.connect.commit()
            return True
        except Exception as e:
            self.connect.rollback()
            logger.error("Error: insert error -- %s -- error info:%s" % (sql, str(e)))
            return False

    '''
    insert a record while return a auto incremented id
    '''

    def insert_rowid(self, sql):
        cursor = self.connect.cursor()
        try:
            cursor.execute(sql)
            self.connect.commit()
            return cursor.lastrowid
        except Exception as e:
            self.connect.rollback()
            logger.error("Error: insert error -- %s -- error info:%s" % (sql, str(e)))
            return None

    def update(self, sql):
        cursor = self.connect.cursor()
        try:
            cursor.execute(sql)
            self.connect.commit()
            return True
        except Exception as e:
            self.connect.rollback()
            logger.error("Error: update error -- %s -- error info:%s" % (sql, str(e)))
            return False

    def delete(self, sql):
        cursor = self.connect.cursor()
        try:
            cursor.execute(sql)
            self.connect.commit()
            return True
        except Exception as e:
            self.connect.rollback()
            logger.error("Error: delete error -- %s -- error info:%s" % (sql, str(e)))
            return False

    def transaction(self):
        return Transaction(pymysql.connect(host=self.host, port=int(self.port), user=self.user, passwd=self.passwd,
                                           db=self.schema, charset="utf8"))

    def close(self):
        self.connect.close()

    def ping(self):
        try:
            return self.connect.ping()
        except Exception as e:
            logger.error("Error: DataBase Connect Error, %s" % str(e))
            return 1


class Transaction:
    def __init__(self, connect):
        self.connect = connect

    def execute(self, sql):
        cursor = self.connect.cursor()
        try:
            cursor.execute(sql)
            return True
        except Exception as e:
            self.connect.rollback()
            logger.error("Error: %s - error info:%s" % (sql, str(e)))
            return False

    def rollback(self):
        self.connect.rollback()

    def commit(self):
        self.connect.commit()
        self.connect.close()


job_scheduler = BackgroundScheduler(jobstores={
    'default': MemoryJobStore()
}, executors={
    'default': ThreadPoolExecutor(20),
    'processpool': ProcessPoolExecutor(10)
}, job_defaults={
    'coalesce': False,
    'max_instances': 5
})


def allow_cross(func):
    """
    跨域注解
    :param func:
    :return:
    """
    def wrapper(*args, **kwargs):
        response = make_response(func(*args, **kwargs))
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE,OPTIONS'
        allow_headers = "Referer,Accept,Origin,User-Agent,x-requested-with,content-type"
        response.headers['Access-Control-Allow-Headers'] = allow_headers
        response.mimetype = 'application/json'
        return response

    wrapper.func_name = func.func_name
    wrapper.func_doc = func.func_doc
    return wrapper


class CSVFile:
    def __init__(self, section, autoCreateDir=None):
        self.base_dir = get_config(section, 'path')
        self.auto_create_dir = autoCreateDir

    def mkdir(self, path):
        if not os.path.exists(path):
            os.makedirs(path, True)

    def write(self, name, headers, rows):
        if self.auto_create_dir == 'day':
            file_path = self.base_dir + "/" + today() + "/"
        if self.auto_create_dir is None:
            file_path = self.base_dir + "/"
        self.mkdir(file_path)
        with codecs.open(file_path + name, 'a', encoding='utf-8-sig') as _file:
            f_csv = csv.DictWriter(_file, headers)
            f_csv.writeheader()
            f_csv.writerows(rows)

    def write_rows(self, name, headers, rows):
        if self.auto_create_dir == 'day':
            file_path = self.base_dir + "/" + today() + "/"
        if self.auto_create_dir is None:
            file_path = self.base_dir + "/"
        self.mkdir(file_path)
        with codecs.open(file_path + name, 'a', encoding='utf-8') as _file:
            f_csv = csv.writer(_file)
            if headers is not None:
                f_csv.writerows(headers)
            if rows is not None:
                f_csv.writerows(rows)