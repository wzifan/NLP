import re

pfr_articles = []
with open("PFRdemoData.txt", "r", encoding="utf-8") as f:
    for line in f.readlines():
        line = line.strip('\n')
        line = line.strip()
        line = re.sub("[ ]+", " ", line)
        line_list = line.split(' ')
        word_tag_list = []
        nt = False
        temp_word = ""
        if line_list[0] != '':
            for temp_str in line_list:
                temp_list = temp_str.split('/')
                if '[' in temp_list[0]:
                    nt = True
                    temp_list[0] = temp_list[0].replace('[', '')
                if ']' in temp_list[1]:
                    nt = False
                    temp_list[1] = temp_list[1].split(']')[0]
                    temp_word += temp_list[0]
                    word_tag_list += [[temp_word, 'nt']]
                    temp_word = ""
                if nt == True:
                    temp_word += temp_list[0]
                word_tag_list += [temp_list]
            pfr_articles += [word_tag_list]
print(pfr_articles)
for line in pfr_articles:
    print(line)
