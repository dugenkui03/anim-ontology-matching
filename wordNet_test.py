import nltk

from nltk.corpus import wordnet as wn


# # 查询一个词所在的所有词集
# print(wn.synsets('ape'))
#
# #查询词语某种词性所在的同义词集合：ADJ, ADJ_SAT, ADV, NOUN, VERB = 'a', 's', 'r', 'n', 'v'
# print(wn.synsets('person', pos=wn.NOUN))
#
# # 查询一个同义词集的定义
# print(wn.synset('person.n.01').definition())
#
# # 查询词语一个词义的例子
# print(wn.synset('person.n.01').examples())
#
# # 查询一个同义词集中的所有词
# print(wn.synset('person.n.01').lemma_names())
#
# #输出词集和词的配对——词条
# print(wn.synset('person.n.01').lemmas())
#
# # 利用词条查询反义词
# good = wn.synset('good.a.01')
# print(good.lemmas()[0].antonyms())
#
# # 查询两个词之间的语义相似度 todo 貌似不可用
# color = wn.synset('music.n.01')
# colour = wn.synset('musical.n.01')
# print(color.path_similarity(colour))


def countx():
	res = {}

	dbpedia_term_dict = {}
	with open("data/dbpedia") as dbpedia_file:
		dbpedia_content = dbpedia_file.readlines()
		for line in dbpedia_content:
			dbpedia_term_dict[line.split(";")[1].lower().strip()] = line.split(";")[0].lower().strip()

	with open("data/clz2entityAnim") as animFile:
		animContent = animFile.readlines()
		for animLine in animContent:
			term = animLine.split(";")[1]
			syno_list = wn.synsets(term)
			for ele in syno_list:
				syn_term = ele.name().split(".")[0]
				if (syn_term != term):
					if syn_term in dbpedia_term_dict.keys():
						# list(matchDict.keys())[list(matchDict.values()).index(line.split(";")[0].strip())]
						res[animLine.split(";")[0]] = dbpedia_term_dict[syn_term]
	return res

syno_dic = countx()
print(syno_dic)
