#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author : dada
# @time   : 2020/8/17 14:45
"""
* 表示支持所有的sheetname
如需要增加打标字段直接增加即可
例如："tmall": {
        "品牌": ['content', 'title'，'keyword'],
    },
    天猫在打品牌标签时就会合并content，title，keyword字段进行打标
"""
tag_choice_dic = {
    "redbook": {
        "*": ['content', 'title'],
    },
    "zhihu": {
        "*": ['content', 'title'],
    },
    "xinyang": {
        "*": ['content', 'title'],
    },
    "tmall": {
        "品牌": ['content', 'title'],
    },
    "jd": {
        "品牌": ['content', 'title'],
    },
    "nosetime": {
        "品牌": ['content', 'title'],
    },
}
