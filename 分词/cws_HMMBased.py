import numpy as np
import pickle
import os


# 基于隐马尔科夫的中文分词
# text：待分词的文本。类型：字符串
# dictionary_path：词典路径。类型：字符串
# params_dir：参数存储目录。类型：字符串
# init：是否要重新初始化。类型：bool
# 返回分词结果列表，列表中每个元素为一个词。类型：列表
def HMMBasedCut(text, dictionary_path="default_dict.txt", params_dir="cwsParams", init=False):
    if init == True:
        cws_HMMBased_init(dictionary_path, params_dir)
    # 初始化参数和字典
    try:
        with open(os.path.join(params_dir, "A.pkl"), "rb") as f:
            A = pickle.load(f)
        with open(os.path.join(params_dir, "B.pkl"), "rb") as f:
            B = pickle.load(f)
        with open(os.path.join(params_dir, "pi.pkl"), "rb") as f:
            pi = pickle.load(f)
        with open(os.path.join(params_dir, "dict_list.pkl"), "rb") as f:
            dict = pickle.load(f)
    except:
        cws_HMMBased_init(dictionary_path, params_dir)
        with open(os.path.join(params_dir, "A.pkl"), "rb") as f:
            A = pickle.load(f)
        with open(os.path.join(params_dir, "B.pkl"), "rb") as f:
            B = pickle.load(f)
        with open(os.path.join(params_dir, "pi.pkl"), "rb") as f:
            pi = pickle.load(f)
        with open(os.path.join(params_dir, "dict_list.pkl"), "rb") as f:
            dict = pickle.load(f)
    # 将 text转化成列表
    list_text = list(text)
    length = len(list_text)
    view_list = []
    temp_list = []
    hidden_list = []
    # 求观测序列，不在字典里的字记下标为-1
    for char in list_text:
        try:
            if char.isdigit():
                view_list += [-1]
            else:
                index = dict.index(char)
                view_list += [index]
        except:
            view_list += [-1]
    # 求隐状态序列
    for index in view_list:
        if index == -1:
            if temp_list != []:
                hidden_list += hiddenList(A, B, pi, temp_list)
                temp_list = []
            # 字典里没有的字作为单字词处理
            hidden_list += [3]
        else:
            temp_list += [index]
    if temp_list != []:
        hidden_list += hiddenList(A, B, pi, temp_list)
    result_list = []
    temp_str = ""
    # 根据隐状态序列求分词结果
    for i in range(length):
        state = hidden_list[i]
        str = list_text[i]
        if state == 0:
            # 将缓存写入结果列表，清空缓存
            if temp_str != "":
                result_list += [temp_str]
                temp_str = ""
            temp_str = temp_str + str
        elif state == 1:
            temp_str = temp_str + str
        elif state == 2:
            temp_str = temp_str + str
            # 将缓存写入结果列表，清空缓存
            result_list += [temp_str]
            temp_str = ""
        elif state == 3:
            # 将缓存写入结果列表，清空缓存
            if temp_str != "":
                result_list += [temp_str]
                temp_str = ""
            if str.isdigit() and result_list != [] and result_list[-1].isdigit():
                result_list[-1] = result_list[-1] + str
            else:
                result_list += [str]
    return result_list


# 初始化
def cws_HMMBased_init(dictionary_path, params_dir):
    BM, BE, MM, ME, S, NS = 0, 0, 0, 0, 0, 0
    # 字典
    dict = []
    with open(dictionary_path, "r", encoding="utf-8") as f:
        print("正在初始化，首次分词可能较慢")
        for line in f.readlines():
            line = line.strip('\n')
            line = line.strip()
            line_list = line.split(' ')
            word = line_list[0]
            frequence = int(line_list[1])
            length = len(word)
            list_word = list(word)
            dict += list_word
            if length == 1:
                S += frequence
            elif length == 2:
                NS += frequence
                BE += frequence
            else:
                NS += frequence
                BM += frequence
                ME += frequence
                MM += frequence * (length - 3)
    pNS = NS / (NS + S)
    pS = S / (NS + S)
    # A
    A = np.zeros((4, 4))
    A[0][1] = BM / (BM + BE)
    A[0][2] = BE / (BM + BE)
    A[1][1] = MM / (MM + ME)
    A[1][2] = ME / (MM + ME)
    A[2][0] = pNS
    A[2][3] = pS
    A[3][0] = pNS
    A[3][3] = pS
    A = A + 1e-8
    for i in range(4):
        A[i] = A[i] / np.sum(A[i])
    # pi
    pi = np.array([pNS, 0, 0, pS])
    pi = pi + 1e-8
    sum_pi = np.sum(pi)
    pi = pi / sum_pi
    # 字典
    dict = sorted(list(set(dict)))
    # B
    B = np.zeros((4, len(dict)))
    with open(dictionary_path, "r", encoding="utf-8") as f:
        for line in f.readlines():
            line = line.strip('\n')
            line = line.strip()
            line_list = line.split(' ')
            word = line_list[0]
            frequence = int(line_list[1])
            length = len(word)
            list_word = list(word)
            if length == 1:
                B[3][dict.index(list_word[0])] += frequence
            if length > 1:
                B[0][dict.index(list_word[0])] += frequence
                B[2][dict.index(list_word[-1])] += frequence
            if length > 2:
                M_list = list_word[1:-1]
                for char in M_list:
                    B[1][dict.index(char)] += frequence
    for i in range(4):
        B[i] = B[i] / np.sum(B[i])
    B = B + 1e-12
    for i in range(4):
        B[i] = B[i] / np.sum(B[i])
    # 保存参数
    if os.path.exists(params_dir) == False:
        os.mkdir(params_dir)
    with open(os.path.join(params_dir, "A.pkl"), "wb") as f:
        pickle.dump(A, f)
    with open(os.path.join(params_dir, "B.pkl"), "wb") as f:
        pickle.dump(B, f)
    with open(os.path.join(params_dir, "pi.pkl"), "wb") as f:
        pickle.dump(pi, f)
    with open(os.path.join(params_dir, "dict_list.pkl"), "wb") as f:
        pickle.dump(dict, f)
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

# print(HMMBasedCut("文本"))
# print(HMMBasedCut("文本", init=True))
