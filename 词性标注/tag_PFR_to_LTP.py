tag = "词性"
list_tag = list(tag)
# 词性转换
if list_tag[0] == "a":
    tag = "a"
if list_tag[-1] == "g":
    tag = "g"
if tag == "l":
    tag = "i"
if tag == "f":
    tag = "nd"
if tag == "nr":
    tag = "nh"
if tag == "nx":
    tag = "ws"
if list_tag[0] == "n" and tag != "n" and tag != "nd" and tag != "nh":
    tag = "xxx"
if list_tag[0] == "u":
    tag = "u"
if tag == "vn":
    tag = "n"
if list_tag[0] == "v":
    tag = "v"
if tag == "w":
    tag = "wp"
if tag == "y":
    tag = "u"
