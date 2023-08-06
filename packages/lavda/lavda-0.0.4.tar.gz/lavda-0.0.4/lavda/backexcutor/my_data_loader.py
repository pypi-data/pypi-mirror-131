import pandas as pd

from lavda.util.panda_tool import PandaTool
from lavda.util.file_tool import FileTool

from lavda.util.mysql_util import LavwikiDfReader, local_server_engine

from impala.dbapi import connect


class HiveSource(object):
    def __init__(self, table_name):
        self._table_name = table_name
        self.conn = connect(host='192.168.10.10', port=10000, user=None, password=None, database='default',
                            auth_mechanism="PLAIN")

    @property
    def table_name(self):
        return self._table_name

    def select_data(self, sql):
        cur = self.conn.cursor()

        cur.execute("desc {}".format(self.table_name))
        d = cur.fetchall()
        cols = []
        for i in d:
            cols.append(i[0])

        cur.execute(sql)
        data = cur.fetchall()
        df = pd.DataFrame(data, columns=cols)
        return df


class DaDataLoader(object):
    @staticmethod
    def load_from_db(input_path, merge_task_object=None):
        """
        从mysql数据库加载数据
        :param input_path: 表名
        :param merge_task_object: 数据合并类
        :return:
        """
        # 1.验证表是否存在
        select_sql = "show tables;"
        table_list = local_server_engine.execute(select_sql).cursor._rows
        if ('{}'.format(input_path)) not in table_list:
            return None
        # 2.加载数据
        # TODO 先这么写，等之后改，这么写数据量大了肯定不合适

        read_sql = "select * form '{}' where datetime = '{}';".format(input_path, data_datetime)
        # 数据主体
        df_data = local_server_engine.execute(read_sql).fetchall()
        # 字段名
        df_columns = local_server_engine.execute(
            "select column_name from information_schema.columns where table_name = '{}'".format(input_path)).fetchall()
        df_columns = [column[0] for column in df_columns]
        df_input = [{m[0]: n for m, n in zip(df_columns, _data)} for _data in df_data]
        return df_input

    @staticmethod
    def load_from_file(input_path, merge_task_object=None, suffix=".xlsx"):
        """
        加载数据
        :param input_path:string, 目录/文件
        :param merge_task_object:object, 数据合并类
        :return:
        """

        # 1.获取所有数据文件路径
        if isinstance(input_path, (list, tuple, set)):
            file_params_list = input_path
        else:
            file_params_list = FileTool.get_file_path(input_path, suffix=".xlsx")
            if not file_params_list:
                return None
        if len(file_params_list) <= 0:
            raise Exception("no data input")

        # 2.加载数据
        if merge_task_object is not None:
            df_data = merge_task_object.processor.process(file_params_list)
        else:
            df_list = list()
            for file_path in file_params_list:
                df_one = PandaTool.read_more(file_path)
                df_list.append(df_one)

            df_data = pd.concat(df_list, sort=False)

        return df_data


class DaDataSave(object):
    @staticmethod
    def save_to_db(output_path, df_result):

        pass

    @staticmethod
    def save_to_file(output_path, df_result, task_meta):
        if task_meta['taskCount'] != task_meta['dfStatisTaskCount']:
            if df_result is not None:
                PandaTool.save(output_path, df_result)
