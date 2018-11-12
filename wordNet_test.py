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


def get_syno_dic():
	"""
		1.获取anim term对应的近义词列表；
		2.如果anim_term的近义词可以再dbpedia中找到，则将(anim_term_uri,dbpedia_term_uri)加入到字典。可以多对多；
		3. todo: 可以多对多，但是不在去匹配已经精确匹配的数据
	"""
	res = {}

	dbpedia_term_dict = {}
	with open("data/equalDBpedia") as dbpedia_file:
		"""
		获取dbpedia数据键值对，key是term，value是uri，例如：
		'q5','<http://wikidata.dbpedia.org/resource/q5>'
		"""
		dbpedia_content = dbpedia_file.readlines()
		for line in dbpedia_content:
			# fixme 不去匹配已经精确匹配的数据
			if len(line.split(";"))>2:
				continue
			dbpedia_term_dict[line.split(";")[1].lower().strip()] = line.split(";")[0].lower().strip()

	with open("data/equalAnim") as anim_file:
		animContent = anim_file.readlines()
		for anim_line in animContent:
			# fixme 不去匹配已经精确匹配的数据
			if ";equal;" in anim_line:
				continue
			# 获取近义词列表
			anim_term = anim_line.split(";")[1].strip()
			syno_list = wn.synsets(anim_term)
			for anim_term_syno_info in syno_list:
				# 如果anim_term的近义词可以再dbpedia中找到，则将(anim_term_uri,dbpedia_term_uri)加入到字典。可以多对多
				syn_term_syno = anim_term_syno_info.name().split(".")[0]
				if syn_term_syno != anim_term and syn_term_syno in dbpedia_term_dict.keys():
						res[anim_line.split(";")[0]] = dbpedia_term_dict[syn_term_syno]
	return res

syno_dic = get_syno_dic()
print(syno_dic)
