from ltp import LTP


# 使用哈工大分词方法，输入为字符串(str)，输出为列表(List[str])的分词
def myltpcut(text):
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
