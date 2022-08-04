import numpy as np
import re
import os
import pickle


# 最短路径法中文分词
# text：待分词的文本。类型：字符串
# dictionary_path：词典路径。类型：字符串
# params_dir：参数存储目录。类型：字符串
# big_number；相邻字之间如果没有路，则给一个大的值，big_number为该值的大小。类型：能被转化成浮点型的正数
# init：是否要重新初始化。类型：bool
# 返回分词结果列表，列表中每个元素为一个词。类型：列表
def shortestPathCut(text, dictionary_path="default_dict.txt", params_dir="cwsParams", big_number=20.0, init=False):
    if init == True:
        cws_shortestPath_init(dictionary_path, params_dir)
    # 读取参数
    try:
        with open(os.path.join(params_dir, "dictionary_p.pkl"), "rb") as f:
            dictionary_p = pickle.load(f)
    except:
        cws_shortestPath_init(dictionary_path, params_dir)
        with open(os.path.join(params_dir, "dictionary_p.pkl"), "rb") as f:
            dictionary_p = pickle.load(f)
    dictionary = set(dictionary_p)
    big_number = float(big_number)
    list_text = list(text)
    len_text = len(list_text)
    result_list = []
    DAG = {}
    # 构建有向无环图
    for word in dictionary:
        # 求词在文本中的位置
        subsp = substrPosition(word, text)
        # 有向无环图 DAG的 key为词位置元组，value词串概率的负对数
        if subsp != []:
            v = dictionary_p[word]
            for tu in subsp:
                DAG[tu] = v
    # 相邻字之间如果没有路，则给一个大的值
    for i in range(len_text):
        if (i, i + 1) not in DAG:
            DAG[(i, i + 1)] = big_number
    # 获得排序好的 DAG的 keys，如 [(0, 1), (0, 2), (1, 2), (2, 3), (3, 4), (2, 5), (3, 5)]
    DAG_keylist = list(DAG.keys())
    DAG_keylist.sort(key=lambda x: (x[1], x[0]))
    len_keylist = len(DAG_keylist)
    # 计算到某个结点为止的最短距离及到该节点最短路径的直接前驱的下标
    # minDistanceList中每个元素为一个元组，第一个值为到该下标结点的距离，第二个值为到该节点最短路径的直接前驱
    minDistanceList = [(0, 0)]
    i = 0
    while i < len_keylist:
        j = i + 1
        while j < len_keylist:
            if DAG_keylist[i][1] != DAG_keylist[j][1]:
                break
            j += 1
        # DAG_keylist[i:j]为到 DAG_keylist[i][1]的所有路径
        dList = []
        for t in range(i, j):
            # 到 DAG_keylist[t][0]的最短距离加上 DAG_keylist[t]的距离
            dList += [minDistanceList[DAG_keylist[t][0]][0] + DAG[DAG_keylist[t]]]
        # 到 DAG_keylist[i][1]的最短距离
        mind = min(dList)
        # 到 DAG_keylist[i][1]的最短距离的下标
        index = np.argmin(dList)
        # 到 DAG_keylist[i][1]的最短路径的直接前驱
        pre = DAG_keylist[i + index][0]
        # 将结果放入 minDistanceList中
        minDistanceList += [(mind, pre)]
        i = j
    # 求最短路径
    i = len_text
    SPath = [i]
    while i > 0:
        i = minDistanceList[i][1]
        SPath += [i]
    SPath = list(reversed(SPath))
    # 根据最短路径分词
    for i in range(len(SPath) - 1):
        str = ''.join(list_text[SPath[i]:SPath[i + 1]])
        # 如果当前词为数字(0~9)且上一个词也为数字(0~9)，则将这两个词合并
        if str.isdigit() and result_list != [] and result_list[-1].isdigit():
            result_list[-1] = result_list[-1] + str
        else:
            result_list += [str]
    return result_list


# 初始化
def cws_shortestPath_init(dictionary_path, params_dir):
    print("正在初始化")
    # 词典列表
    dictionary = []
    p = []
    with open(dictionary_path, "r", encoding="utf-8") as f:
        for line in f.readlines():
            line = line.strip('\n')
            line = line.strip()
            line_list = line.split(' ')
            word = line_list[0]
            if word != '':
                dictionary += [word]
                p += [float(line_list[1])]
    p = np.array(p)
    sum = np.sum(p)
    p = p / sum
    p = -np.log(p)
    dictionary_p = {k: v for k, v in zip(dictionary, p)}
    if os.path.exists(params_dir) == False:
        os.makedirs(params_dir)
    with open(os.path.join(params_dir, "dictionary_p.pkl"), "wb") as f:
        pickle.dump(dictionary_p, f)
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

# print(shortestPathCut("文本"))
# print(shortestPathCut("文本", init=True))
