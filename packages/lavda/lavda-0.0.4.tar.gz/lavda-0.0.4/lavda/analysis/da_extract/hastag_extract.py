# -*- coding: utf-8 -*-
# ----------------------------------------------
# purpose : HashTag提取
# author : 
# create_time : 2020/7/9 15:11
# update_time : 2020/7/9 15:11
# copyright : Lavector
# ----------------------------------------------
import re
import numpy as np

from lavda.backexcutor.analysis_interface import *


class HastTagExtract(RowInterface):
    def __init__(self, default_value=None, tag_type='en', separator=","):
        """
        :param default_value: , 无数据或非法数据时返回此默认值
        :param tag_type: string, hasttag类型
                        en: 英文
                        ch: 中文
        :param separator: string, 结果分隔符
        """
        super(HastTagExtract, self).__init__(default_value)
        self.default_value = default_value
        self.separator = separator

        if tag_type == "en":
            self.tag_pattern = re.compile('#[^\s]+')
        else:
            self.tag_pattern = re.compile('#.*?#', re.S)

    def process(self, data, params=None):
        if data is None:
            return self.default_value

        data = str(data)
        result = self.tag_pattern.findall(data)
        t_list = [self.separator] * len(result)
        result = "{}".join(result).format(*t_list)

        return result


class HasTagExtractAndFormat(DfProcessInterface):
    """
    hastag tag 数据提取并格式化
    """
    def __init__(self, input_column=None, output_column=None, separator=","):
        self.input_column = input_column
        self.output_column = output_column
        self.separator = separator

    def cross_analysis(self, data, columns):
        """
         做交叉分析。将一个cell中的值，拆分为多行。
        :param data: 数据,dataframe
        :param columns: 要处理的列名,string
        :return:
            拆分好的数据框。因为是将同一个cell中的数据进行拆分，所以要保证一个cell
            拆分后对应的索引不变，这会让我们找到拆分后的数据在原数据中的位置，也方
            便通过统计不同的索引次数，来统计单个值的讨论量
        """

        token = self.separator

        a = data[columns].str.split(token, expand=True)
        b = a.stack()  # 压缩成一列：此时的数据结果变为多层列
        # 重新指定index:drop=true，将变更前的列去掉，默认保留
        c = b.reset_index(level=1, drop=True)
        c1 = c.replace(' ', np.nan).dropna()
        e = c1.rename(columns)  # 为series设置名称，方便join
        f = data.drop(columns, axis=1)  # 删除原始数据中的被分出的列，使用join合并：join默认使用index合并
        g = f.join(e)
        return g

    def process(self, data, **params):
        extractor = HastTagExtract()
        # 找出hashtag后面的值
        data[self.output_column] = data[self.input_column].astype(str).apply(lambda x: extractor.process(x))
        # 替换不必要符号
        data[self.output_column] = data[self.output_column].astype(str).apply(lambda x: re.sub('\[|\]|\'|\ˇ|\#', '', x))
        # 将逗号拆分合并,相同条数复制
        data = self.cross_analysis(data, self.output_column)
        data[self.output_column] = data[self.output_column].apply(lambda x: re.sub(' ', '', x))  # 缩减空格

        return data



if __name__ == "__main__":
    # data = "#SHOTSANDSWATCHES @fentybeauty Cheeks Out. #Cream Blush. 10 shades"
    # extractor = HastTagExtract()
    # result = extractor.process(data)
    # print(result)

    import os
    root_path = "/Users/yuantian/Downloads"
    input_path = os.path.join(root_path, "博主帖子.xlsx")
    output_path = os.path.join(root_path, "博主帖子-result.xlsx")
    from maxda.util.panda_tool import PandaTool
    df_input = PandaTool.read(input_path)

    extractor = HasTagExtractAndFormat("content", "hasttag_result")
    df_result = extractor.process(df_input)

    PandaTool.save(output_path, df_result)

    # data = ['#Georgefloyd', '#restinpower', '#justiceforgeorgefloyd', '#blacklivesmatter']
    # d_lst = [','] * len(data)
    # data = "{}".join(data).format(*d_lst)
    # print(data)