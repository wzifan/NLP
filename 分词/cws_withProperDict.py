#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Wang Zifan

"""带专有词的中文分词(专有词不会被分开)"""
import os
import pickle
import re
import jieba


def cutWithProDict(text: str, prodict_path: str = "proper_dict.txt", method=jieba.lcut,
                   params_dir: str = "cwsParams", init: bool = False):
    """ 针对带有专有词的中文分词

        Args:
            text (str): 待分词的文本
            prodict_path (str): 词典路径
            method (输入字符串返回列表的函数): 分词方法
            params_dir (str): 参数存储目录
            init (bool): 是否要重新初始化

        Returns:
            List: 分词结果列表，列表中每个元素为一个词
    """
    if init == True:
        cws_withProperDict_init(prodict_path, params_dir)
    # 读取参数
    try:
        with open(os.path.join(params_dir, "prodict_list.pkl"), "rb") as f:
            prodict = pickle.load(f)
    except:
        cws_withProperDict_init(prodict_path, params_dir)
        with open(os.path.join(params_dir, "prodict_list.pkl"), "rb") as f:
            prodict = pickle.load(f)
    list_text = list(text)
    len_text = len(list_text)
    position_list = []
    cuttedtext = []
    result_list = []
    # 根据prodict对原文本切分
    # 求prodict中每个词在文本中的位置
    for word in prodict:
        position_list += substrPosition(word, text)
    # 去重
    position_list = sorted(position_list, key=lambda x: (x[0], -x[1]))
    temp_list = []
    i = 0
    for x in position_list:
        if x[0] < x[1] and x[0] >= i:
            i = x[1]
            temp_list += [x]
    position_list = temp_list
    # 根据专有词的位置切分文本
    i = 0
    for x in position_list:
        cuttedtext += [list_text[i:x[0]]]
        cuttedtext += [''.join(list_text[x[0]:x[1]])]
        i = x[1]
    cuttedtext += [list_text[i:len_text]]
    # 删除空列表
    for e in cuttedtext:
        if e == []:
            cuttedtext.remove(e)
    # 对切分后的文本分词
    for x in cuttedtext:
        if type(x) is list:
            result_list += method(''.join(x))
        elif type(x) is str:
            result_list += [x]
    return result_list


def cws_withProperDict_init(prodict_path: str, params_dir: str):
    """ 初始化

        Args:
            dictionary_path (str): 词典路径
            params_dir (str): 参数存储目录

        Returns:
            None
    """
    print("正在初始化")
    # 专有词典列表
    prodict = set()
    with open(prodict_path, "r", encoding="utf-8") as f:
        for line in f.readlines():
            line = line.strip('\n')
            line = line.strip()
            line_list = line.split(' ')
            word = line_list[0]
            if word != '':
                prodict.add(word)
    prodict = sorted(list(prodict))
    # 保存参数
    if os.path.exists(params_dir) == False:
        os.makedirs(params_dir)
    with open(os.path.join(params_dir, "prodict_list.pkl"), "wb") as f:
        pickle.dump(prodict, f)
    print("初始化完成")


def substrPosition(substr, s):
    """ 求子串在字符串s中的所有位置

        Args:
            substr (str): 子串
            s (str): 指定的字符串

        Returns:
            List[tuple]: 位置元组列表
    """
    result_list = []
    if substr in s:
        result_list = [a.span() for a in re.finditer(substr, s)]
    return result_list

# print(cutWithProDict("文本"))
# print(cutWithProDict("文本", init=True))
