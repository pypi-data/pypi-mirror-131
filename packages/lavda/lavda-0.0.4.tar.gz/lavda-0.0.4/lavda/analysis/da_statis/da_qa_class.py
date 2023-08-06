# -*- coding: utf-8 -*-
# ----------------------------------------------
# purpose : 数据质量检测
# author :
# create_time : 2020/7/15 16:28
# update_time : 2020/7/15 16:28
# copyright : Lavector
# ----------------------------------------------
import pandas as pd
import numpy as np
import datetime
from lavda.backexcutor.analysis_interface import *
from lavda.analysis.common import parse_multi_column


class QaCommonWays(object):
    @staticmethod
    def save(all_df_result_dict, result_file_path):
        writer = pd.ExcelWriter(result_file_path)
        for label_name in all_df_result_dict:
            df_one_label = all_df_result_dict[label_name]
            df_one_label.to_excel(writer, sheet_name=label_name, index=True)
        writer.save()

    @staticmethod
    def count_percent(df_result, df_data_count, cul_name, name_count, name_percent):
        df_count = df_result.groupby([cul_name]).agg({cul_name: 'count'})
        df_count.rename(columns={cul_name: name_count}, inplace=True)
        df_count.sort_values(by=[name_count], axis=0, ascending=False, inplace=True)
        # 比例
        df_count[name_percent] = df_count[name_count].astype(float)/df_data_count.astype(float)
        df_count[name_percent] = df_count[name_percent].apply(lambda x: '%.2f%%' % (x*100))
        return df_count

    @staticmethod
    def get_count_column(df_result, prefix):
        column_name = df_result.columns.tolist()
        # print(column_name)
        count_column_list = []
        for i in column_name:
            # print(i)
            if i.startswith(prefix):
                count_column_list.append(i)
        return count_column_list

    @staticmethod
    def clean_count(df_result, prefix):
        # 获取要统计的列名
        get_count_column_list = QaCommonWays.get_count_column(df_result, prefix)
        list_front = ["清洗前数据总量"]
        list_after = ["清洗后数据总量"]
        list_front.extend(get_count_column_list)
        list_front.extend(list_after)
        # print(list_front)
        dict_count = {'channel': list_front}

        # 分组统计各个渠道的数据
        df_grouped = df_result.groupby(df_result['channel'])
        for name, df_group in df_grouped:
            count_0 = [df_group.shape[0]]
            tag_list = df_group[get_count_column_list].values.astype(int).tolist()
            # 各个渠道1的求和
            list_1_sum = np.sum(tag_list, axis=0).tolist()
            count_0.extend(list_1_sum)

            # 将数据清洗前后的数据量加进去
            list_0_sum = np.sum(tag_list, axis=1).tolist()
            count = 0
            for i in list_0_sum:
                if i == 0:
                    count += 1
            count_1 = [count]
            count_0.extend(count_1)
            dict_count[name] = count_0
        df_count = pd.DataFrame(dict_count)
        return df_count


class PreQuality(DfStatisInterface):
    """
    离散型数据质量统计
    即统计各个值的数量，
    """
    def __init__(self, index_column, input_column_str):
        """

        :param index_column: string， 数据索引列名
        :param input_column_str: string， 待统计的数据列名
                                eg: content, title
        """
        self.index_column = index_column
        self.count_cul_name_list = parse_multi_column(input_column_str)

    def process(self, data, **params):
        """
        :param data: 输入数据 df
        :param params:
        :return:
        """
        qa_common_friend = QaCommonWays()
        df_data_count = data[self.index_column].count()

        column_set = set(data.columns.tolist())

        all_df_result_dict = dict()
        for name_i in self.count_cul_name_list:
            if name_i not in column_set:
                continue
            cul_name_count = qa_common_friend.count_percent(data, df_data_count, name_i, "%s_count" % (name_i), "%s_percent" % (name_i))
            all_df_result_dict["%s_count" % name_i] = cul_name_count

        return all_df_result_dict


class CleanQuality(DfStatisInterface):
    """
    清洗后数据的质量
    """
    def __init__(self, prefix="tag_clean"):
        """
        清洗结果字段的前缀
        :param prefix:
        """
        self.prefix = prefix

    def process(self, df_result, params=None):
        """
        params:输出路径
         """
        qa_common_friend = QaCommonWays()

        df_count = qa_common_friend.clean_count(df_result, self.prefix)

        return df_count


class TagQuality(DfStatisInterface):
    """
    统计标签的质量
    """
    def __init__(self, index_column, input_column_prefix):
        """
        :param input_column_prefix: 需要统计字段前缀
        """
        self.index_column = index_column
        self.input_column_prefix = input_column_prefix.lower()

    def process(self, data, params=None):
        column_name = data.columns.tolist()
        column_name = [name.lower() for name in column_name]
        input_column_list = [name for name in column_name if name.startswith(self.input_column_prefix)]
        data['datetime_year_month'] = data['datetime'].astype(str).apply(lambda line: line[0:7])

        all_df_result_dict = dict()
        # 提取各个sheet需要统计的字段。
        for input_name in input_column_list:
            last_count_col_name_list = ['datetime_year_month']

            if input_name not in column_name:
                continue
            last_count_col_name_list.append(input_name)

            dup_list = [self.index_column]
            dup_list.append(input_name)
            data_dup = data.drop_duplicates(subset=dup_list, keep='first')

            # 开始对各个sheet的标签统计
            df_tag_count = data_dup.groupby(last_count_col_name_list).agg({input_name: 'count'})
            # df_tag_count = data.groupby(last_count_col_name_list).agg(['count'])
            # df_tag_count.rename(columns={(input_name: '%s_keywords_count' % (input_name)}, inplace=True))
            df_tag_count.rename(columns={input_name: '%s_count' % (input_name)},
                                inplace=True)

            df_tag_count = df_tag_count.reset_index()
            all_df_result_dict[input_name] = df_tag_count

        # 数据多sheet保存
        return all_df_result_dict


def main():
    infile1 = "C:/Users/zhang/Desktop/data_teest.xlsx"
    outfile = "C:/Users/zhang/Desktop/test666.xlsx"
    df_tag = pd.read_excel(infile1, header=0, error_bad_lines=False, encoding="utf_8_sig")

    # 预处理代码测试
    # count_cul_name_list = ['age', 'gender', 'city', 'city_rank', 'age_level']
    # qa = PreQuality(count_cul_name_list)
    # qa.process(df_tag, outfile)

    # 打标质量检测代码测试
    wayfriend = QaCommonWays()
    qa = TagQuality('da_index','tag_format')
    dict_test = qa.process(df_tag)
    wayfriend.save(dict_test,outfile)


    # 清洗质量检测代码测试
    # qa = CleanQuality()
    # qa.process(df_tag, outfile)


if __name__ == "__main__":
    # 开始时间
    sta_time = datetime.datetime.now()

    main()

    # 结束时间
    end_time = datetime.datetime.now()
    times = (end_time - sta_time).seconds
    print("\n运行时间: %ss == %sm == %sh\n\n" % (times, times/60, times/60/60))
    print('文件存储成功！')