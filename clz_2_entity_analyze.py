from SPARQLWrapper import SPARQLWrapper, JSON


category_prex="http://dbpedia.org/page/Category:"

def query_entities(clz):
	# res_list=[]
	num=0
	sparql = SPARQLWrapper("http://dbpedia.org/sparql")
	query_str="""
	select COUNT(?label) as ?cou
	where{
	?label ?b
	"""+clz+"""
	.
	}
	"""
	sparql.setQuery(query_str)
	sparql.setReturnFormat(JSON)
	results = sparql.query().convert()
	for result in results["results"]["bindings"]:
		num=result["cou"]["value"]
	return num

with open("data/finalMatchedAnim")as matched_file:
	file_content=matched_file.readlines()
	for file_line in file_content:
		print("<"+category_prex+file_line.split(";")[1].strip().title()+">",end=":\t")
		print(query_entities("<"+category_prex+file_line.split(";")[1].strip().title()+">"))


