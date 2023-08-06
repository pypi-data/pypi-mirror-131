# -*- coding: utf-8 -*-
# ----------------------------------------------
# purpose: 提取用户类型 PGC/UGC/BGC
# author : 
# create_time : 2020/6/30 10:23
# update_time : 2020/6/30 10:23
# copyright : Lavector
# ----------------------------------------------
from lavda.backexcutor.analysis_interface import *
from lavda.util.mysql_util import LavwikiReader
import pandas as pd


class UserTag(RowInterface):
    def __init__(self, classify, default_value=None):
        super(UserTag, self).__init__(default_value)
        classify = classify.split('&')
        tag_df = LavwikiReader.get_as_df("lav2bgc_star")[
            ['classify', 'channel', 'userid', 'user_tag', 'brand']]

        tag_bgc_format = tag_df[(tag_df['classify'] == 'currency')]
        tag_pgc_format = tag_df[(tag_df['classify'] != 'personal')].loc[:, ('classify', 'channel', 'userid', 'user_tag')]
        if len(classify) > 0:
            tag_bgc_format = '''tag_df[(tag_df['classify'] == 'currency') '''
            tag_pgc_format = '''tag_df[(tag_df['classify'] != 'personal') '''
            for e_classify in classify:
                tag_bgc_format = tag_bgc_format + '''| (tag_df['classify'] == "{}") '''.format(e_classify)
                tag_pgc_format = tag_pgc_format + '''& (tag_df['classify'] != "{}") '''.format(e_classify)
            tag_bgc_format = tag_bgc_format + "]"
            tag_pgc_format = tag_pgc_format + "].loc[:,('classify', 'channel', 'userid', 'user_tag')]"
        tag_bgc_df = eval(tag_bgc_format)
        tag_pgc_df = eval(tag_pgc_format)

        # tag_bgc_df = tag_df[(tag_df['classify'] == classify) | (tag_df['classify'] == 'currency')]
        tag_star_df = tag_df[tag_df['classify'] == 'personal']
        # tag_pgc_df = tag_df[(tag_df['classify'] != 'personal') & (tag_df['classify'] != classify)].loc[:,
        #              ('classify', 'channel', 'userid', 'user_tag')]
        tag_pgc_df.loc[:, 'user_tag'] = 'pgc'
        # 下面这四行是为了去除重复的userID
        bgc_list = list(tag_bgc_df['userid'])
        tag_pgc_df['kk'] = tag_pgc_df.apply(lambda x: x['userid'] in bgc_list, axis=1)
        tag_pgc_df = tag_pgc_df[tag_pgc_df['kk'] == False]
        self.tag_dict = {}
        this_tag_df = pd.concat([tag_bgc_df, tag_star_df, tag_pgc_df], sort=False)
        for a, b in this_tag_df.groupby('channel'):
            b.index = b['userid']
            self.tag_dict[a] = b['user_tag'].to_dict()

        self.redbook_brand_list = []
        for e_classify in classify:
            redbook_brand_list = [i.lower() for i in list(
            tag_df[tag_df['channel'] == 'redbook'][tag_df[tag_df['channel'] == 'redbook']['classify'] == e_classify][
                'brand'])]
            self.redbook_brand_list.extend(redbook_brand_list)
        self.redbook_brand_list = list(set(self.redbook_brand_list))
        self.redbook_pgc_list = ['qq.com', '163.com', '126.com', 'icloud.com', 'htomail.com', 'xzwh.com',
                                 'yahoo.com', 'gmail.com', '邮箱', '美妆博主', '原创博主', '时尚博主', '店铺', '连锁店',
                                 '店主', 'b站', 'wb', '微博', 'ins', '同名', '干货', '分享', '直播', '搬运', '金冠薯']
        self.weibo_pgc_list = ['自媒体', '官方网站', '官方微博', '学者', '作家', '专家', '教授', '导师', '医师', '创始人', '主理人', '达人', '博主',
                               '主编', '编辑', '编剧', '漫画家', '撰稿人', '电竞选手', '游戏选手', '评论人', '影评人', '剧评人', '股评师', '股评人',
                               '优秀回答者', '顾问', '测评', '评测', '安利', '投资', 'vlog', '欢迎投稿', '答主', '问答', '原创', '头条文章作者',
                               '游戏视频自媒体', '医生', '美妆博主', '美食博主', '时尚博主', '摄影博主', '中国区总代理', '经销商']
        self.weibo_star_list = ['反黑站']
        self.tiktok_pgc_list = ['商业合作', '合作', '商务', '联系', '全网同名', '说明来意', '注明来意', '邮箱',
                                '导演', '制作人', '造型师', '专家', '导师', '医生', '博主', '创作者', '成员', '官方',
                                'qq.com', '163.com', '126.com', 'icloud.com', 'htomail.com', 'xzwh.com',
                                'yahoo.com', 'gmail.com', 'vx', 'wx', '微信', '酷狗', 'b站', 'q音', '网易云',
                                'vb', '微博', '微吧', '围脖', 'wb', 'weibo', ]

    def func_redbook(self, data, judge_text, user_tag='ugc'):
        # 认证
        authentication = data['authentication']
        if authentication == '蓝标':
            user_tag = 'pgc'
            if list(filter(lambda x: x in data['nickname'], self.redbook_brand_list)):
                user_tag = 'bgc'
                return user_tag
            return user_tag
        if authentication == '红标':
            user_tag = 'pgc'
            return user_tag
        # 粉丝
        if str(data['fans']).isnumeric():
            ss = int(data['fans'])
            if ss <= 1000 and user_tag != 'pgc':
                user_tag = 'ugc'
            else:
                user_tag = 'pgc'
                return user_tag
        # 简介、昵称、用户标签
        if list(filter(lambda x: x in judge_text, self.redbook_pgc_list)):
            user_tag = 'pgc'
        return user_tag

    def func_tiktok(self, data, judge_text, user_tag='ugc'):
        # 粉丝
        if str(data['fans']).isnumeric():
            ss = int(data['fans'])
            if ss <= 5000 and user_tag != 'pgc':
                user_tag = 'ugc'
            else:
                user_tag = 'pgc'
                return user_tag
        # 认证
        if data['authentication'] == '红标' or data['authentication'] == '蓝标':
            user_tag = 'pgc'
            return user_tag
        # 简介、昵称、用户标签
        if list(filter(lambda x: x in judge_text, self.tiktok_pgc_list)):
            user_tag = 'pgc'

        return user_tag

    def func_weibo(self, data, judge_text, user_tag='ugc'):
        # 粉丝
        if str(data['fans']).isnumeric():
            ss = int(data['fans'])
            if ss <= 3000 and user_tag != 'pgc':
                user_tag = 'ugc'
            else:
                user_tag = 'pgc'
                return user_tag
        # 认证
        if data['authentication'] == '黄标' or data['authentication'] == '蓝标':
            user_tag = 'pgc'
            return user_tag
        # 简介、昵称、用户标签
        if list(filter(lambda x: x in judge_text, self.weibo_star_list)):
            user_tag = 'star'
            return user_tag
        if list(filter(lambda x: x in judge_text, self.weibo_pgc_list)):
            user_tag = 'pgc'

        return user_tag

    def distribute(self, data, **params):
        '''
        分布处理三个平台的数据
        :param data: 字典类型一行数据
        :param params:
        :return:
        '''
        judge_column_name_list = ['fans', 'authentication', 'introduce', 'user_label', 'nickname']
        for column_name in judge_column_name_list:
            if column_name not in data:
                data[column_name] = ''
        judge_text = '.'.join([str(data[i]) for i in judge_column_name_list[1:] if data[i]]).lower()
        channel_dict = {'redbook': self.func_redbook, 'weibo': self.func_weibo, 'tiktok': self.func_tiktok}
        return channel_dict[data['channel']](data, judge_text)

    def process(self, data, **params):
        """
        判断用户类别
        """
        user_tag = 'ugc'  # 默认为ugc
        if data['channel'] in self.tag_dict and data['userid'] in self.tag_dict[data['channel']]:
            user_tag = self.tag_dict[data['channel']][str(data['userid'])]
        if data['channel'] in ['redbook', 'weibo', 'tiktok'] and user_tag not in ['bgc', 'star']:
            user_tag = self.distribute(data)
        # TODO 默认给定ugc
        return user_tag


if __name__ == '__main__':


    # classify = ['美妆', '个护']
    classify = ['皮肤美容大健康', '保健品']
    user_tag = UserTag(classify)
    # data = {'channel': 'weibo', 'userid': '1016215307'} # 皮肤美容大健康 保健品 bgc

    df = pd.read_excel('data.xlsx')


    def func(line):
        dic = line.to_dict()
        return user_tag.process(dic)
    df['user_tag'] = df.apply(func, axis=1)
    split_count = df.shape[0] // 1000000 + 1
    for i in range(split_count):
        writer = pd.ExcelWriter('data_结果文件_{}.xlsx'.format(i), options={'strings_to_urls': False}, engine='xlsxwriter')
        df[i * 1000000:(i + 1) * 1000000].to_excel(writer, sheet_name=str(i), header=True, index=False,
                                                   encoding="utf_8_sig")
        print(i)
        writer.save()
