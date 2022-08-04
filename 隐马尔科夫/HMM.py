import numpy as np


# 求给定模型和观测序列时，观测序列的概率
# A：概率转移矩阵，A[i][j]表示状态 i到 j的概率。类型：二维列表或numpy矩阵
# B：发射概率矩阵，B[i][j]表示状态 i产生观测状态 j的概率。类型：二维列表或numpy矩阵
# pi：初始概率向量。类型：一维列表或一维numpy数组
# view_list：观测状态序列。类型：一维列表或一维numpy数组
# 返回观测序列的概率。类型：数字
def viewListP(A, B, pi, view_list):
    A = A.T
    B = B.T
    length = len(view_list)
    s = pi * B[view_list[0]]
    if length > 1:
        for t in range(1, length):
            s = np.dot(A, s)
            s = s * B[view_list[t]]
    return sum(s)


# 求给定模型和观测序列时，最有可能的隐状态序列
# A：概率转移矩阵，A[i][j]表示状态 i到 j的概率。类型：二维列表或numpy矩阵
# B：发射概率矩阵，B[i][j]表示状态 i产生观测状态 j的概率。类型：二维列表或numpy矩阵
# pi：初始概率向量。类型：一维列表或一维numpy数组
# view_list：观测状态序列。类型：一维列表或一维numpy数组
# return_maxp：要不要返回最有可能的隐状态序列对应的概率。类型：bool
# 返回最有可能的隐状态序列（及其概率）。类型：列表（、数字）
def hiddenList(A, B, pi, view_list, return_maxp=False):
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
    if return_maxp == False:
        # 求隐状态序列
        index = np.argmin(s)
        h_list = [index]
        for temp_list in reversed(pre):
            index = temp_list[index]
            h_list += [index]
        h_list = list(reversed(h_list))
        return h_list
    else:
        # 求隐状态序列及其概率
        index = np.argmin(s)
        max_p = np.e ** (-s[index])
        h_list = [index]
        for temp_list in reversed(pre):
            index = temp_list[index]
            h_list += [index]
        h_list = list(reversed(h_list))
        return h_list, max_p


# 求给定模型和观测序列时，最有可能的隐状态序列
# A：概率转移矩阵，A[i][j]表示状态 i到 j的概率。类型：二维列表或numpy矩阵
# B：发射概率矩阵，B[i][j]表示状态 i产生观测状态 j的概率。类型：二维列表或numpy矩阵
# pi：初始概率向量。类型：一维列表或一维numpy数组
# view_list：观测状态序列。类型：一维列表或一维numpy数组
# return_maxp：要不要返回最有可能的隐状态序列对应的概率。类型：bool
# 返回最有可能的隐状态序列（及其概率）。类型：列表（、数字）
def hiddenListWithoutLog(A, B, pi, view_list, return_maxp=False):
    A = A.T
    B = B.T
    # 隐状态种类数
    num_hstate = len(A)
    # 时间长度或观测状态数目
    length = len(view_list)
    s = pi * B[view_list[0]]
    # 直接前驱列表
    pre = []
    if length > 1:
        for t in range(1, length):
            # 当前时刻状态概率
            current_s = []
            # 当前时刻直接前驱列表
            current_pre = []
            for i in range(num_hstate):
                temp_list = []
                for j in range(num_hstate):
                    temp_list += [s[j] * A[i][j]]
                # 最大概率下标
                index = np.argmax(temp_list)
                current_s += [temp_list[index]]
                current_pre += [index]
            s = current_s * B[view_list[t]]
            pre += [current_pre]
    if return_maxp == False:
        # 求隐状态序列
        index = np.argmax(s)
        h_list = [index]
        for temp_list in reversed(pre):
            index = temp_list[index]
            h_list += [index]
        h_list = list(reversed(h_list))
        return h_list
    else:
        # 求隐状态序列及其概率
        index = np.argmax(s)
        max_p = s[index]
        h_list = [index]
        for temp_list in reversed(pre):
            index = temp_list[index]
            h_list += [index]
        h_list = list(reversed(h_list))
        return h_list, max_p
