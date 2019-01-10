from SPARQLWrapper import SPARQLWrapper, JSON

"""

"""


def count_entities(dbpedia_Clz):
	sparql = SPARQLWrapper("http://dbpedia.org/sparql")
	query_str = """
	select COUNT(?obj) as ?cou
	where{
		?obj rdf:type """+dbpedia_Clz+""" .
	}
	"""
	# print(query_str)
	sparql.setQuery(query_str)
	sparql.setReturnFormat(JSON)
	results = sparql.query().convert()
	num = 0
	for result in results["results"]["bindings"]:
		num = result["cou"]["value"]
	return num


matched_list=["equal","wordNet_syno","thesuaru_syno"]

with open("E:/github/ontology-matching/data/finalMatchedAnim")as matched_file:
	file_content = matched_file.readlines()
	total_num=0
	for file_line in file_content:
		content_list=file_line.split(";")
		if len(content_list)>2 and content_list[2] in matched_list:
			print(content_list[1],end=":\t")
			num=count_entities(content_list[3])
			total_num+=int(num)
			print(num,end=":")
			print(total_num)



