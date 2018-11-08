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



def countx(type):
	cout=0
	with open("data/clz2entityAnim") as animFile:
		animContent=animFile.readlines()
		for line in animContent:
			term=line.split(";")[1]
			syno=str(wn.synsets(term, pos=type))
			if len(syno)>4:
				cout += 1
			print("term:"+term.strip()+"\tsyno"+syno)
	print(type+"："+str(cout))

type=[wn.NOUN,wn.VERB,wn.ADJ,wn.ADJ_SAT,wn.ADV]

for ele in type:
	countx(ele)