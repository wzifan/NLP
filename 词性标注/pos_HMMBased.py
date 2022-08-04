from typing import List
import numpy as np
import pickle
import os


# 基于隐马尔科夫的中文词性标注
# cutted_text：被分好词的文本。类型：字符串列表
# params_dir：参数存储目录。类型：字符串
# 参数目录中应包含：
# A.pkl 词性状态转移矩阵pickle对象(词性种数行,词性种数列)
# B.pkl 发射概率矩阵pickle对象(词性种数行,词数列)
# pi.pkl 初始概率向量pickle对象(词性种数元)
# postag_list.pkl 排好序的词性列表
# vocab_of_pos.pkl 排好序的词典列表
# 返回词性标注结果。类型：列表
def HMMBasedPos(cutted_text: List[str], params_dir="posParams"):
    # 读取参数
    with open(os.path.join(params_dir, "vocab_of_pos.pkl"), "rb") as f:
        dictionary = pickle.load(f)
    with open(os.path.join(params_dir, "postag_list.pkl"), "rb") as f:
        postag = pickle.load(f)
    with open(os.path.join(params_dir, "A.pkl"), "rb") as f:
        A = pickle.load(f)
    with open(os.path.join(params_dir, "B.pkl"), "rb") as f:
        B = pickle.load(f)
    with open(os.path.join(params_dir, "pi.pkl"), "rb") as f:
        pi = pickle.load(f)
    # 初始化
    set_dictionary = set(dictionary)
    view_list = []
    temp_list = []
    tag_list = []
    # 将被分好词的文本转化为观测序列
    for word in cutted_text:
        if word.isdigit():
            view_list += [-3]
        elif word in set_dictionary:
            view_list += [dictionary.index(word)]
        else:
            view_list += [-1]
    # 求词性列表
    for index in view_list:
        if index == -3:
            if temp_list != []:
                hidden_list = hiddenList(A, B, pi, temp_list)
                for i in hidden_list:
                    tag_list += [postag[i]]
                temp_list = []
            # 如果是数字则标记为m
            tag_list += ['m']
        elif index == -1:
            if temp_list != []:
                hidden_list = hiddenList(A, B, pi, temp_list)
                for i in hidden_list:
                    tag_list += [postag[i]]
                temp_list = []
            # 词典里没有的词标记为x
            tag_list += ['x']
        else:
            temp_list += [index]
    if temp_list != []:
        hidden_list = hiddenList(A, B, pi, temp_list)
        for i in hidden_list:
            tag_list += [postag[i]]
    return tag_list


# 基于隐马尔科夫的中文词性标注(带自定义专有词词典)
# cutted_text：被分好词的文本。类型：列表
# prodict_path：自定义专有词典路径，每一行的第一个空格前为一个词，utf8编码。类型：字符串
# params_dir：参数存储目录。类型：字符串
# 参数目录中应包含：
# A.pkl 词性状态转移矩阵pickle对象(词性种数行,词性种数列)
# B.pkl 发射概率矩阵pickle对象(词性种数行,词数列)
# pi.pkl 初始概率向量pickle对象(词性种数元)
# postag_list.pkl 排好序的词性列表
# vocab_of_pos.pkl 排好序的词典列表
# 初始化后还包含：
# prodict_list.pkl 排序好的实体词列表
# 返回词性标注结果。类型：元组列表
def HMMBasedPosWithProdict(cutted_text: List[str], prodict_path="proper_dict.txt", params_dir="posParams", init=False):
    if init == True:
        pos_HMMBased_init(prodict_path, params_dir)
    # 读取参数
    try:
        with open(os.path.join(params_dir, "prodict_list.pkl"), "rb") as f:
            prodict = pickle.load(f)
    except:
        pos_HMMBased_init(prodict_path, params_dir)
        with open(os.path.join(params_dir, "prodict_list.pkl"), "rb") as f:
            prodict = pickle.load(f)
    with open(os.path.join(params_dir, "vocab_of_pos.pkl"), "rb") as f:
        dictionary = pickle.load(f)
    with open(os.path.join(params_dir, "postag_list.pkl"), "rb") as f:
        postag = pickle.load(f)
    with open(os.path.join(params_dir, "A.pkl"), "rb") as f:
        A = pickle.load(f)
    with open(os.path.join(params_dir, "B.pkl"), "rb") as f:
        B = pickle.load(f)
    with open(os.path.join(params_dir, "pi.pkl"), "rb") as f:
        pi = pickle.load(f)
    # 初始化
    set_dictionary = set(dictionary)
    set_prodict = set(prodict)
    view_list = []
    temp_list = []
    tag_list = []
    # 将被分好词的文本转化为观测序列
    for word in cutted_text:
        if word.isdigit():
            view_list += [-3]
        elif word in set_prodict:
            view_list += [-2]
        elif word in set_dictionary:
            view_list += [dictionary.index(word)]
        else:
            view_list += [-1]
    # 求词性列表
    for index in view_list:
        if index == -3:
            if temp_list != []:
                hidden_list = hiddenList(A, B, pi, temp_list)
                for i in hidden_list:
                    tag_list += [postag[i]]
                temp_list = []
            # 如果是数字则标记为m
            tag_list += ['m']
        elif index == -2:
            if temp_list != []:
                hidden_list = hiddenList(A, B, pi, temp_list)
                for i in hidden_list:
                    tag_list += [postag[i]]
                temp_list = []
            # 将专有名词标记为nz
            tag_list += ['nz']
        elif index == -1:
            if temp_list != []:
                hidden_list = hiddenList(A, B, pi, temp_list)
                for i in hidden_list:
                    tag_list += [postag[i]]
                temp_list = []
            # 词典里没有的词标记为x
            tag_list += ['x']
        else:
            temp_list += [index]
    if temp_list != []:
        hidden_list = hiddenList(A, B, pi, temp_list)
        for i in hidden_list:
            tag_list += [postag[i]]
    return tag_list


# 初始化
def pos_HMMBased_init(prodict_path, params_dir):
    print("正在初始化")
    # 专有词典
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


# 求给定模型和观测序列时，最有可能的隐状态序列
# A：概率转移矩阵，A[i][j]表示状态 i到 j的概率。类型：二维列表或numpy矩阵
# B：发射概率矩阵，B[i][j]表示状态 i产生观测状态 j的概率。类型：二维列表或numpy矩阵
# pi：初始概率向量。类型：一维列表或一维numpy数组
# view_list：观测状态序列。类型：一维列表或一维numpy数组
# return_maxp：要不要返回最有可能的隐状态序列对应的概率。类型：bool
# 返回最有可能的隐状态序列。类型：列表
def hiddenList(A, B, pi, view_list):
    with np.errstate(divide='ignore'):
        A = -np.log(A.T)
        B = -np.log(B.T)
        pi = -np.log(pi)
    # 隐状态种类数
    num_hstate = len(A)
    # 时间长度或观测状态数目
    length = len(view_list)
    s = pi + B[view_list[0]]
    # 直接前驱列表
    pre = []
    if length > 1:
        for t in range(1, length):
            # 当前时刻状态负对数概率
            current_s = []
            # 当前时刻直接前驱列表
            current_pre = []
            for i in range(num_hstate):
                temp_list = []
                for j in range(num_hstate):
                    temp_list += [s[j] + A[i][j]]
                # 最小负对数概率下标
                index = np.argmin(temp_list)
                current_s += [temp_list[index]]
                current_pre += [index]
            s = current_s + B[view_list[t]]
            pre += [current_pre]
    # 求隐状态序列
    index = np.argmin(s)
    h_list = [index]
    for temp_list in reversed(pre):
        index = temp_list[index]
        h_list += [index]
    h_list = list(reversed(h_list))
    return h_list

# print(HMMBasedPos(["word1", "word2"]))
# print(HMMBasedPosWithProdict(["word1", "word2"]))
# print(HMMBasedPosWithProdict(["word1", "word2"], init=True))
