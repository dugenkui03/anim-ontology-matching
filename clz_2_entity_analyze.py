from SPARQLWrapper import SPARQLWrapper, JSON


"""
查看DBpedia数据的label属性是否包含在动画的 命名uri，构造的query如下，TV是动态参数：
	select COUNT(?obj) as ?cou
	where{
		?obj rdfs:label ?label .
		FILTER REGEX(STR(?label),"^Tv") . #可以使用正则通配符
		FILTER(STRLEN(?label)<5+STRLEN("Tv")) .
	}
	
"""

def query_entities(label_str):
	sparql = SPARQLWrapper("http://dbpedia.org/sparql")
	query_str="""
	select COUNT(?obj) as ?cou
	where{
		?obj rdfs:label ?label .
		FILTER REGEX(STR(?label),\"^"""+label_str+"""\") . #可以使用正则通配符
		FILTER(STRLEN(?label)<5+STRLEN(\""""+label_str+"""\")) .
	}
	"""
	# print(query_str)
	sparql.setQuery(query_str)
	sparql.setReturnFormat(JSON)
	results = sparql.query().convert()
	num=0
	for result in results["results"]["bindings"]:
		num=result["cou"]["value"]
	return num

with open("data/finalMatchedAnim")as matched_file:
	file_content=matched_file.readlines()
	for file_line in file_content:
		key_word=file_line.split(";")[1].strip().title()
		print(key_word)
		print(query_entities(key_word))


