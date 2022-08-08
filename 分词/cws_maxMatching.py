#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Wang Zifan

"""基于最大匹配的中文分词"""
import os
import pickle


def forwardMaxMatching(text: str, dictionary_path: str = "default_dict.txt", params_dir: str = "cwsParams",
                       max_length: int = 5, init: bool = False):
    """ 前向最大匹配法中文分词

        Args:
            text (str): 待分词的文本
            dictionary_path (str): 词典路径
            params_dir (str): 参数存储目录
            max_length (int): 最大匹配长度
            init (bool): 是否要重新初始化

        Returns:
            List: 分词结果列表，列表中每个元素为一个词
    """
    if init == True:
        cws_maxMatching_init(dictionary_path, params_dir)
    # 读取参数
    try:
        with open(os.path.join(params_dir, "dictionary_list.pkl"), "rb") as f:
            dictionary = pickle.load(f)
    except:
        cws_maxMatching_init(dictionary_path, params_dir)
        with open(os.path.join(params_dir, "dictionary_list.pkl"), "rb") as f:
            dictionary = pickle.load(f)
    # 将词典变为集合的形式
    dictionary = set(dictionary)
    list_text = list(text)
    len_text = len(list_text)
    result_list = []
    i = 0
    while i < len_text:
        # 判断当前的 i有没有分得词
        i_word = False
        for j in reversed(range(1, max_length + 1)):
            word = ''.join(list_text[i: i + j])
            if word in dictionary:
                # 如果当前词为数字(0~9)且上一个词也为数字(0~9)，则将这两个词合并
                if word.isdigit() and result_list != [] and result_list[-1].isdigit():
                    result_list[-1] = result_list[-1] + word
                else:
                    result_list += [word]
                # 分得词，i=i+j-1+1
                i = i + j - 1
                i_word = True
                break
        # 如果当前的 i没有分得词，则将当前字(list_text[i])放入分词结果中
        if i_word == False:
            str = list_text[i]
            # 如果当前词为数字(0~9)且上一个词也为数字(0~9)，则将这两个词合并
            if str.isdigit() and result_list != [] and result_list[-1].isdigit():
                result_list[-1] = result_list[-1] + str
            else:
                result_list += [str]
        # 未分得词，i=i+1
        i += 1
    return result_list


def backwardMaxMatching(text: str, dictionary_path: str = "default_dict.txt", params_dir: str = "cwsParams",
                        max_length: int = 5, init: bool = False):
    """ 后向最大匹配法中文分词

        Args:
            text (str): 待分词的文本
            dictionary_path (str): 词典路径
            params_dir (str): 参数存储目录
            max_length (int): 最大匹配长度
            init (bool): 是否要重新初始化

        Returns:
            List: 分词结果列表，列表中每个元素为一个词
    """
    if init == True:
        cws_maxMatching_init(dictionary_path, params_dir)
    # 读取参数
    try:
        with open(os.path.join(params_dir, "dictionary_list.pkl"), "rb") as f:
            dictionary = pickle.load(f)
    except:
        cws_maxMatching_init(dictionary_path, params_dir)
        with open(os.path.join(params_dir, "dictionary_list.pkl"), "rb") as f:
            dictionary = pickle.load(f)
    # 将词典变为集合的形式
    dictionary = set(dictionary)
    list_text = list(text)
    len_text = len(list_text)
    result_list = []
    j = len_text
    while j > 0:
        # 判断当前的 j有没有分得词
        j_word = False
        for i in reversed(range(1, max_length + 1)):
            word = ''.join(list_text[j - i:j])
            if word in dictionary:
                # 如果当前词为数字(0~9)且上一个词也为数字(0~9)，则将这两个词合并(反过来加)
                if word.isdigit() and result_list != [] and result_list[-1].isdigit():
                    result_list[-1] = word + result_list[-1]
                else:
                    result_list += [word]
                # 分得词，j=j-i+1-1
                j = j - i + 1
                j_word = True
                break
        # 如果当前的 j没有分得词，则将当前字(list_text[j-1])放入分词结果中
        if j_word == False:
            str = list_text[j - 1]
            # 如果当前词为数字(0~9)且上一个词也为数字(0~9)，则将这两个词合并(反过来加)
            if str.isdigit() and result_list != [] and result_list[-1].isdigit():
                result_list[-1] = str + result_list[-1]
            else:
                result_list += [str]
        # 未分得词，j=j-1
        j -= 1
    return list(reversed(result_list))


def cws_maxMatching_init(dictionary_path: str, params_dir: str):
    """ 初始化

        Args:
            dictionary_path (str): 词典路径
            params_dir (str): 参数存储目录

        Returns:
            None
    """
    print("正在初始化")
    # 词典列表
    dictionary = set()
    with open(dictionary_path, "r", encoding="utf-8") as f:
        for line in f.readlines():
            line = line.strip('\n')
            line = line.strip()
            line_list = line.split(' ')
            word = line_list[0]
            if word != '':
                dictionary.add(word)
    dictionary = sorted(list(dictionary))
    # 保存词典列表
    if os.path.exists(params_dir) == False:
        os.makedirs(params_dir)
    with open(os.path.join(params_dir, "dictionary_list.pkl"), "wb") as f:
        pickle.dump(dictionary, f)
    print("初始化完成")

# print(forwardMaxMatching("文本"))
# print(backwardMaxMatching("文本"))
# print(forwardMaxMatching("文本", init=True))
# print(backwardMaxMatching("文本", init=True))
