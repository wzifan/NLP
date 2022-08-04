import re
import xml.dom.minidom

# 根据xml文件构建DOM树
DOMTree = xml.dom.minidom.parse("example.xml")
# 获得DOM树的根结点
collection = DOMTree.documentElement
# 获得根结点的所有的doc子结点
docs = collection.getElementsByTagName("doc")
# 获得第一个doc元素
doc0 = docs[0]
doc1 = docs[1]
print("*" * 30)
print("# 获得第一个doc元素")
print(doc0)
# 获取元素的属性值
value = doc0.getAttribute("name")
print("*" * 30)
print("# 获取元素的属性值")
print("value=" + value)
# 每个元素和元素之间都有字符时(包括回车)，一共有2n+1个childNode，n为子元素个数
print("*" * 30)
print("# 每个元素和元素之间都有字符时(包括回车)，一共有2n+1个childNode，n为子元素个数")
print(doc0.childNodes)
# 元素和元素之间没有字符时，则相应的childNode也不存在
print("*" * 30)
print("# 元素和元素之间没有字符时，则相应的childNode也不存在")
print(doc1.childNodes)
# 可以通过.data获得元素和元素之间的字符串(包括回车)
print("*" * 30)
print("# 可以通过.data获得元素和元素之间的字符串(包括回车)")
print(doc0.childNodes[0].data)
# 获得doc0中的第一个content元素
content = doc0.getElementsByTagName("content")[0]
print("*" * 30)
print("# 获得doc0中的第一个content元素")
print(content)
# 如果content的内容不为空，则获取content的内容
print("*" * 30)
print("# 如果content的内容不为空，则获取content的内容")
text = ""
if content.hasChildNodes():
    text = text + content.firstChild.data
print(text)
# 将text中的回车和空格(包括全角空格)去掉
print("*" * 30)
print("# 将text中的回车和空格(包括全角空格)去掉")
text = re.sub("[\n\040\u3000]+", "", text)
print(text)
