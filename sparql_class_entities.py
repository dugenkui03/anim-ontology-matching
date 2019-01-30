from SPARQLWrapper import SPARQLWrapper, JSON



def query_entities(clz):
	# res_list=[]
	num=0
	sparql = SPARQLWrapper("http://dbpedia.org/sparql")
	sparql.setQuery(
	"""
	select COUNT(?label) as ?cou
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
		num=result["cou"]["value"]
	return num


checked_list=[]
sum=0
with open("data/clzEntities","w",encoding='utf-8') as ent_file:
	equal_list=["equal","wordNet_syno","thesuaru_syno"]
	with open("data/finalMatchedAnim_bk0110_自动化数据备份") as final_file:
		file_content=final_file.readlines()
		for line in file_content:
			listX=line.split(";")
			if len(listX)>2 and listX[2] in equal_list:
				if listX[3] in checked_list:

					continue;
				else:
					checked_list.append(listX[3])

				print(listX[3].strip()+":",end="")
				# ent_file.write(listX[3].strip()+"\n")
				count=query_entities(listX[3])
				sum+=int(count)
				print(count)
				# print(len(entities))
				# ent_file.write(str(entities)+"\n")
print(sum)