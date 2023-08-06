# -*- coding: utf-8 -*-
# ----------------------------------------------
# purpose : 
# author : 
# create_time : 2020/7/1 16:46
# update_time : 2020/7/1 16:46
# copyright : Lavector
# ----------------------------------------------
import re


def indexMany(The_Str,The_Find):   #str是要查询的字符
    length = len(The_Str)     #获取该字符串的长度
    str1 = The_Str            #拷贝字符串
    The_List = []
    count = 0             #用来计算每次截取完字符串的总长度
    try:
        while str1.index(The_Find)!=-1:      #当字符串中没有该字符则跳出
            n = str1.index(The_Find)         #查询查找字符的索引
            str2 = str1[0:n + 1]        #截取的前半部分
            str1 = str1[n + 1:length]   #截取的后半部分
            count = count + len(str2)       #计算每次截取完字符串的总长度
            The_List.append(count - 1)        #把所有索引添加到列表中
            length=length-len(str2)     #截取后半部分的长度
    except ValueError:
        return The_List
    return The_List


def add_self_length(content,tag):
    result_list = indexMany(content, tag)


    return_list = [result+len(tag) for result in result_list]
    return return_list



def continuous_addition(content,tag,preset_length):
    assert type(preset_length) == int , "长度不符合规范"
    tag_list = tag.split("+")
    assert len(tag_list) == 2, "关键词长度不符合规范"
    if not re.search("(?=.*{})(?=.*{})^.*$".format(tag_list[0], tag_list[1]), content):
        return False
    first_word = tag_list[0]
    end_word = tag_list[1]
    first_length = len(first_word)
    second_length = len(end_word)
    first_index = indexMany(content,first_word)
    second_index = indexMany(content,end_word)
    for first in first_index:
        for second in second_index:
            if first < second:
                length = second-(first+first_length)
            else:
                length = first-(second+second_length)
            if length < preset_length:
                return True

    return False
