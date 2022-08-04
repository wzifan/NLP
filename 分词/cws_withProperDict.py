import os
import pickle
import re
import jieba


# 针对带有专有词的中文分词
# text：待分词的文本。类型：字符串
# prodict_path：专有词词典路径。类型：字符串
# method：分词方法。类型：输入字符串(str)返回列表(list)的函数
# params_dir：参数存储目录。类型：字符串
# init：是否要重新初始化。类型：bool
# 返回分词结果列表，列表中每个元素为一个词。类型：列表
def cutWithProDict(text, prodict_path="proper_dict.txt", method=jieba.lcut, params_dir="cwsParams", init=False):
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


# 初始化
def cws_withProperDict_init(prodict_path, params_dir):
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


# 求子串在字符串s中的所有位置
# substr：子串。类型：字符串
# s：指定的字符串。类型：字符串
# 返回位置元组列表。类型：元组列表
def substrPosition(substr, s):
    result_list = []
    if substr in s:
        result_list = [a.span() for a in re.finditer(substr, s)]
    return result_list

# print(cutWithProDict("文本"))
# print(cutWithProDict("文本", init=True))
