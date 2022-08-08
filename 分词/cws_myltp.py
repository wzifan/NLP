#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Wang Zifan

"""基于哈工大LTP的中文分词"""
from ltp import LTP


def myltpcut(text):
    """ 使用哈工大LTP的分词

        Args:
            text (str): 待分词的文本

        Returns:
            List: 分词结果列表，列表中每个元素为一个词
    """
    # 加载模型
    ltp = LTP(path="base1")
    # 分句
    sentences = LTP.sent_split([text])
    num_sentence = len(sentences)
    result = []
    # 为防止显存溢出，每10句分一次词
    for n in range(0, num_sentence, 10):
        # 分词
        seg, hidden = ltp.seg(sentences[n:n + 10])
        for sentence in seg:
            result += sentence
    return result
