#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author : dada
# @time   : 2020/7/13 14:18
import pandas as pd
from lavda.analysis.da_tag.Filed_Services import filed_services
from lavda.analysis.da_tag.tag import related_word_mapping,get_Text2Formal,TextMatch2,index_list
from lavda.analysis.da_tag.tag_config import tag_choice_dic



def max_split_tag(df,mappings,Intermediate,add_head_text):
    return last_max_split_tag(df=df,mappings=mappings,Intermediate=Intermediate,add_head_text=add_head_text)

def max_relation_split_tag(df,mappings,intermediate,add_head_text):
    return last_max_relation_split_tag(df=df,mappings=mappings,intermediate=intermediate,add_head_text=add_head_text)



@filed_services
def last_max_split_tag(df, mappings, Intermediate, add_head_text):
    for _map in mappings:
        df['{}_other'.format(_map.sheetname)] = df[Intermediate].apply(lambda line: eval(line)['{}'.format(_map.sheetname)] if line and str(line) != "nan" else "")
    for mapping in mappings:
        df['{}_index'.format(mapping.sheetname)] = range(df.shape[0])
        keyword = mapping.mapping_list
        Sen = mapping.sentment
        tag_other_list = df[['{}_index'.format(mapping.sheetname),'{}_other'.format(mapping.sheetname)]].values.tolist()
        tag_list = []
        for tag in tag_other_list:
            index = tag[0]
            G_tag = str(tag[1]).split("噜")
            tag_list += [[index, G_id] for G_id in G_tag]

        df_tag = pd.DataFrame(tag_list, columns=["{}_index".format(mapping.sheetname), "{}_other".format(mapping.sheetname)])
        df = df.drop(['{}_other'.format(mapping.sheetname)], axis=1,)
        df = pd.merge(df, df_tag, on="{}_index".format(mapping.sheetname), how="left")
        for word in enumerate(keyword):
            df[word[1]] = df['{}_other'.format(mapping.sheetname)].apply(lambda line: str(line).split("*")[word[0]] if len(line) > 0 else "" )
        if Sen:
            df["{}_aspect".format(mapping.sheetname)] = df['{}_other'.format(mapping.sheetname)].apply(lambda line: str(line).split("*")[-1] if len(line) > 0 else "")
        df = df.drop(['{}_other'.format(mapping.sheetname), '{}_index'.format(mapping.sheetname)], axis=1)
    df = df.drop([Intermediate], axis=1)
    df.drop_duplicates(keep="first", inplace=True)
    return df


@filed_services
def last_max_relation_split_tag(df,mappings,intermediate,add_head_text):
    df['merge_index'] = range(df.shape[0])
    keyword_list = []  # 存放keyword列的字段名，下面提取打到的词会用到

    map_collect_list = mappings.get_map_name_collect()
    if  len(map_collect_list) == 1:
        collet_name = map_collect_list[0]
        df['tag_example'] = df[intermediate].apply(lambda line:signle_mapping_deal(line,collet_name))
        tag_other_list = df[
            ['merge_index', 'tag_example']].values.tolist()
        tag_list = []
        for tag in tag_other_list:
            index = tag[0]
            G_tag = tag[1]
            tag_list += [[index, G_id] for G_id in G_tag]

        df_tag = pd.DataFrame(tag_list,
                              columns=["merge_index", "{}-id".format(collet_name)])

        df1 = pd.merge(df, df_tag, on="merge_index", how="left")
        df2 = pd.merge(df1,mappings[0].mapping_df , on="{}-id".format(collet_name), how="left")
        df2 = df2.drop(['{}-id'.format(collet_name),'merge_index','tag_example','tag_keyword', intermediate], axis=1, )
        for i in df2:
            if '(keyword)' in i and add_head_text not in i:
                keyword_list.append(i)
        for i in keyword_list:
            df2[i.split('(')[0] + '_aspect'] = df2.apply(lambda line: add_aspect(line, i), axis=1)
        df2 = df2.drop(['tag_aspect'], axis=1)
        return df2
    else:
        split_merge_index = df.groupby('merge_index')
        df_list = [related_word_mapping(intermediate,the_data, mappings) for name, the_data in split_merge_index]
        df_data = pd.concat(df_list,sort=False)
        df_data.drop(['merge_index', 'tag_keyword', intermediate], axis=1, inplace=True)
        for i in df_data:
            if '(keyword)' in i and add_head_text not in i:
                keyword_list.append(i)
        for i in keyword_list:
            df_data[i.split('(')[0] + '_aspect'] = df_data.apply(lambda line: add_aspect(line, i), axis=1)
        df_data = df_data.drop(['tag_aspect'], axis=1)
        return df_data


def add_aspect(line, i):
    #TODO 提取aspect词
    '''
    先这么用，之后会改，写的太草了
    为分句打标增加实际打上的字段（情感使用）
    :param line:传进来的一列数据
    :param i: 传进来的keyword列字段名，比如：时间(keyword)
    :return:
    '''
    result_list = []  # 存放结果
    keywords_list = []  # 存放结果
    keywords_list2 = []  # 存放结果
    keywords_list3 = []  # 存放结果
    if '|' in str(line[i]):
        for split_1 in str(line[i]).split('|'):
            if '-' in split_1:
                keywords_list.append(split_1.split('-')[0])
            else:
                keywords_list.append(split_1)
    else:
        if '-' in str(line[i]):
            keywords_list.append(str(line[i]).split('-')[0])
        else:
            keywords_list.append(str(line[i]))
    for i in keywords_list:
        if '(' in i or '（' in i:
            keywords_list2.append(i[1:-1])
        else:
            keywords_list2.append(i)
    for i in keywords_list2:
        if '+' in i:
            keywords_list3.extend(i.split('+'))
        else:
            keywords_list3.append(i)

    if line['tag_aspect']:
        for i in eval(line['tag_aspect']):
            if '#' in i and i in keywords_list3:
                result_list.append(i[1:])
            elif '@' in i and i in keywords_list3:
                text = str(line['content'])+str(line['title'])
                text_list = [text[tag_index-5 if tag_index-5>=0 else 0:tag_index+len(i[1:])+5] for tag_index in index_list(text,i[1:])]
                for _ in text_list:
                    for foudingci in TextMatch2.negative_word_list:
                        if foudingci in _:
                            result_list.extend([foudingci,i[1:]])
                            break
                    break
            elif i in keywords_list3:
            # if i in keywords_list3:
                result_list.append(i)
    return ','.join(set(result_list))


def signle_mapping_deal(line,collectname):
    if str(line) in ["nan", "", "NaN", "null", "Null", "None"]:
        result = [-1]
    else:
        line = eval(line)
        if len(line) == 1:
            if str(line[0]) ==  '({})'.format(collectname):
                result = [-1]
            else:
                result = [int(str(line[0]).replace('({})'.format(collectname),''))]
        else:
            result = [int(str(tag_).replace('({})'.format(collectname),'')) for tag_ in line]
    return result