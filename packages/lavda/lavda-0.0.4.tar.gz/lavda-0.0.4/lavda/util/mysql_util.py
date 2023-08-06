# -*- coding: utf-8 -*-
# ----------------------------------------------
# author : 
# create_time : 2020/6/29 15:36
# update_time : 2020/6/29 15:36
# copyright : Lavector
# ----------------------------------------------
from pymysql import *
import pandas as pd
import copy

from lavda.util.py_config_parser import PyConfigParser
from lavda.config.maxda_config import *
from sqlalchemy import create_engine


class LavwikiReader(object):
    """
    加载 lavwiki 数据库的数据
    """

    @staticmethod
    def get_connection_config(dict_format=False):
        # TODO 注意要复制一份而不是直接使用，因此下一面还要修改值的
        db_config = copy.deepcopy(CONF_DB_LAVWIKI)

        if dict_format:
            db_config['cursorclass'] = cursors.DictCursor

        return db_config

    @staticmethod
    def get_as_df(db_table_name, dict_format=True):
        # 注意没有列名的
        # 创建连接
        config = LavwikiReader.get_connection_config(dict_format)
        con = connect(**config)
        # 执行sql语句
        try:
            with con.cursor() as cursor:
                sql = "select * from %s" % db_table_name
                cursor.execute(sql)
                result = cursor.fetchall()
        finally:
            con.close()
        df = pd.DataFrame(result)
        return df

    @staticmethod
    def execute(sql, dict_format=False):
        db = None
        cur = None
        try:
            config = LavwikiReader.get_connection_config(dict_format)
            db = connect(**config)
            # 游标对象
            cur = db.cursor()
            cur.execute("%s;" % sql)
            db.commit()
            msg = "success"
        except Exception as e:
            # 错误回滚
            db.rollback()
            msg = "fail"
        finally:
            cur.close()
            db.close()
        # 返回统一状态
        return msg

    # 数据库查询所有操作方法:
    @staticmethod
    def execute_all(sql, dict_format=False):
        db = None
        cur = None
        import traceback
        try:
            config = LavwikiReader.get_connection_config(dict_format)
            db = connect(**config)
            cur = db.cursor()
            cur.execute("%s;" % sql)
            result = cur.fetchall()
            msg = "success"
        except Exception as e:
            # 错误回滚
            db.rollback()
            msg = "fail"
            result = []
        finally:
            cur.close()
            db.close()
        # 返回统一状态
        return result, msg


class LavwikiDfReader(object):
    @staticmethod
    def read_table(table_name, database="lavwiki"):
        """

        :param table_name: string,表名
        :param database: string，数据库名
        :return:
        """
        db_config = CONF_DB_LAVWIKI
        db_config['database'] = database
        conn = connect(**db_config)
        sql = """select * from {0}{1}""".format("", table_name)
        df = pd.read_sql(sql, conn)
        conn.close()
        return df


class CommonLavDbReader(object):
    """
    加载 lav 数据库的数据
    """

    @staticmethod
    def get_connection_config(dict_format=False, database='lav_ai', default_db_config=None):
        # TODO 注意要复制一份而不是直接使用，因此下一面还要修改值的
        if default_db_config is None:
            parser = PyConfigParser()
            config = parser.parse_xml("configs")
            db_config = config['lav_db']
        else:
            db_config = default_db_config.copy()
        db_config['port'] = int(db_config['port'])
        db_config['database'] = database

        if dict_format:
            db_config['cursorclass'] = cursors.DictCursor

        return db_config

    @staticmethod
    def get_as_df(db_table_name, dict_format=True, database='lav_ai', db_config=None):
        """

        :param db_table_name: string, 表名
        :param dict_format: bool, 是否返回dict格式的数据
        :param database: string，数据库名
        :param db_config: dict, 数据库连接配置
        :return:
        """
        # 注意没有列名的
        # 创建连接
        config = CommonLavDbReader.get_connection_config(dict_format, database=database, default_db_config=db_config)
        con = connect(**config)
        # 执行sql语句
        try:
            with con.cursor() as cursor:
                sql = "select * from %s" % db_table_name
                cursor.execute(sql)
                result = cursor.fetchall()
        finally:
            con.close()
        df = pd.DataFrame(result)
        return df

    @staticmethod
    def execute(sql, dict_format=False, database='lav_ai', db_config=None):
        db = None
        cur = None
        try:
            config = CommonLavDbReader.get_connection_config(dict_format, database, default_db_config=db_config)
            db = connect(**config)
            # 游标对象
            cur = db.cursor()
            cur.execute("%s;" % sql)
            db.commit()
            msg = "success"
        except Exception as e:
            # 错误回滚
            db.rollback()
            msg = "fail"
        finally:
            cur.close()
            db.close()
        # 返回统一状态
        return msg

    # 数据库查询所有操作方法:
    @staticmethod
    def execute_all(sql, dict_format=False, database='lav_ai', db_config=None):
        db = None
        cur = None
        try:
            config = CommonLavDbReader.get_connection_config(dict_format, database, default_db_config=db_config)
            db = connect(**config)
            cur = db.cursor()
            cur.execute("%s;" % sql)
            result = cur.fetchall()
            msg = "success"
        except Exception as e:
            # 错误回滚
            db.rollback()
            msg = "fail"
            result = []
        finally:
            cur.close()
            db.close()
        # 返回统一状态
        return result, msg


# 增加个线上数据库的engine
cloud_server_engine = create_engine(
    'mysql+pymysql://data_analysis:data_analysis_root_0715@111.207.114.228:13306/lavtest')
local_server_engine = create_engine(
    'mysql+pymysql://data_analysis:data_analysis_root_0715@111.207.114.228:13306/lavtest')

if __name__ == '__main__':
    config = LavwikiReader.get_connection_config()
    LavwikiReader.execute_all("select keyword from ec_des_word")
