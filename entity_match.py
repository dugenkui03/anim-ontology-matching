import nltk

from nltk.tokenize import sent_tokenize # 分词


def pre_hand():
    with open("data/entity_data/animEntityPrepro","w") as empty_file:
        with open("data/entity_data/animEntity") as entity_file:
            entity_file_content=entity_file.readlines()
            for line in entity_file_content:
                try:
                    lindex=line.index("#")
                    rindex=line.index(" of")
                    empty_file.write(line.strip()+";"+line[lindex+1:rindex].strip()+"\n")
                except:
                    pass




"""
1. 分隔符使用空格替换——》分词——》去停用词，包括M、SP等动画本体库标识词——>提取词根——>rdfs:label进行匹配
"""
with open('data/entity_data/animEntityPrepro') as handed_entity_file:
    entity_content=handed_entity_file.readlines()
    for line in entity_content:
        rid_sep=line.split(';')[1].strip().replace("_"," ")
        sep_text=sent_tokenize(rid_sep)
        print(sep_text)
