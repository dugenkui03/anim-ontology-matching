from SPARQLWrapper import SPARQLWrapper, JSON



def query_entities(clz):
	res_list=[]
	sparql = SPARQLWrapper("http://dbpedia.org/sparql")
	sparql.setQuery(
	"""
	select ?label
	where{
	?label <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> 
	"""+clz+
	"""
	.
	}
	"""
	)
	sparql.setReturnFormat(JSON)
	results = sparql.query().convert()
	for result in results["results"]["bindings"]:
		res_list.append(result["label"]["value"])
	return res_list


with open("data/clzEntities","w",encoding='utf-8') as ent_file:
	equal_list=["equal","wordNet_syno","thesuaru_syno"]
	with open("data/finalMatchedAnim") as final_file:
		file_content=final_file.readlines()
		for line in file_content:
			listX=line.split(";")
			if len(listX)>2 and listX[2] in equal_list:
				ent_file.write(listX[3])
				entities=query_entities(listX[3])
				ent_file.write(str(entities)+"\n")