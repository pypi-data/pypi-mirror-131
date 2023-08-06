# -*- coding: utf-8 -*-
# ----------------------------------------------
# purpose : 
# author : LGD
# create_time : 2021/2/26 10:51
# update_time : 2021/2/26 10:51
# copyright : Lavector
# ----------------------------------------------
import re
import pandas as pd
import string

from lavda.util.text_util import DBC2SBC

gl_letter_sets = set(string.ascii_letters)

class LabelUtil(object):
    RE_USER_TAT = re.compile('@[\S]+') #re.compile('@.*? ')
    RE_TOPIC = re.compile('#.*?#')
    RE_EMOTION = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               "]+", flags=re.UNICODE)

    @staticmethod
    def clean_text(content):
        if pd.isna(content):
            return ""
        text = str(content)
        text = LabelUtil.remove_topic(text)

        text = LabelUtil.RE_EMOTION.sub(r'', text)
        line = re.sub(r"[\n]+", "。", text.strip())
        # line = re.sub(r"[!！?？#,，@… ~～。.`、'‘]+", " ", line)
        # line = re.sub(r"[#]+", " ", line)
        line = re.sub(r"( ){2,}", "", line)
        line = LabelUtil.format_eng_text(line)

        line = line.lower().strip()
        line = DBC2SBC(line)

        return line

    @staticmethod
    def clean_dict_cell(content):
        """
        标签词典单元格清理方法
        :param content:
        :return:
        """
        if pd.isna(content):
            return ""
        line = str(content).strip()
        line = LabelUtil.format_eng_text(line)

        line = line.replace(" ", "")
        line = line.lower()

        line = DBC2SBC(line)

        return line

    @staticmethod
    def format_eng_text(content):
        """
        标准化英文数据，英文名字可能通过空格、引号等进行分隔处理，这个很不方便，因此要格式化
        :param content:
        :return:
        """
        line = content
        while 1:
            result = re.sub(r"(.*[A-Za-z])( |')+([A-Za-z].*)", r'\1_\3', line)
            if result == line:
                break
            line = result

        return line

    @staticmethod
    def remove_topic(content, user_max_len=16):
        """
        去除文本中的话题、用户名等
        :param content: string, 输入文本
        :param user_max_len: int,由于'@用户名'使用不规范，后面可能没有空格分隔，因此可以设置一个最大长度，超过此长度的不删除
        :return:
        """
        if '@' in content:
            # 正常的@用户
            li = LabelUtil.RE_USER_TAT.findall(content)
            for i in li:
                if user_max_len is not None:
                    if len(i) > user_max_len:
                        i = i[:user_max_len]

                content = content.replace(i, '')
        if '#' in content:
            content = LabelUtil.RE_TOPIC.sub("", content)

        return content


def run_one():
    data = "我肋中国#123#lsdfld,@lkl苈轸ewewrwer w "
    result = LabelUtil.clean_text(data)
    print(result)


def run_format_en():
    line = "Nature Way'lei佳思敏"
    while 1:
        result = re.sub(r"(.*[A-Za-z])( |')+([A-Za-z].*)", r'\1_\3', line)
        if result == line:
            break
        line = result

    print(line)


if __name__ == '__main__':
    run_format_en()