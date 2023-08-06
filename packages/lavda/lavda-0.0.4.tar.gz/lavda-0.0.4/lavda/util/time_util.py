# -*- coding: utf-8 -*-
# ----------------------------------------------
# purpose : 
# author : 
# create_time : 2020/8/21 15:11
# update_time : 2020/8/21 15:11
# copyright : Lavector
# ----------------------------------------------
import time
import datetime


class TimeTool(object):
    @staticmethod
    def get_current_day():
        current_day = time.strftime('%Y%m%d', time.localtime(time.time()))
        return current_day

    @staticmethod
    def get_current_time():
        current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        return current_time

    @staticmethod
    def get_current_dgraph_time():
        current_time = time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime(time.time()))
        return current_time

    @staticmethod
    def epoch_seconds(start_datetime, end_datetime):
        """

        :param start_datetime: datetime
        :param end_datetime: datetime
        :return: 返回时间间隔，单位为秒
        """
        td = end_datetime - start_datetime  # datetime.timedelta
        return td.days * 86400 + td.seconds + (float(td.microseconds) / 1000000)

    @staticmethod
    def epoch_hours(start_datetime, end_datetime):
        """

        :param start_datetime: datetime
        :param end_datetime: datetime
        :return: 返回时间间隔，单位为小时
        """
        total_seconds = TimeTool.epoch_seconds(start_datetime, end_datetime)
        hours = int(round(total_seconds / 3600))
        return hours

    @staticmethod
    def epoch_seconds(start_datetime, end_datetime):
        """

        :param start_datetime: datetime
        :param end_datetime: datetime
        :return: 返回时间间隔，单位为秒
        """
        td = end_datetime - start_datetime  # datetime.timedelta
        return td.days * 86400 + td.seconds + (float(td.microseconds) / 1000000)

    @staticmethod
    def string_to_datetime(datetime_string):
        return datetime.datetime.strptime(datetime_string, u"%Y-%m-%d %H:%M:%S")

    @staticmethod
    def datetime_to_string(datetime_data):
        return datetime_data.strftime("%Y-%m-%d %H:%M:%S")