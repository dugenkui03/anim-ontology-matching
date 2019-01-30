from SPARQLWrapper import SPARQLWrapper,JSON # SPARQL查询



sparql_endpoint=SPARQLWrapper('https://dbpedia.org/sparql')

count=0
with open("data/prop_data/propDataPrepro") as prop_file:
	prop_content=prop_file.readlines()
	prop_content.sort(key= lambda line:len(line.split(';')[1].strip().lower().replace('_'," ")))
	for line in prop_content:
		prop_name=line.split(';')[1].strip().lower().replace('_'," ")
		print(prop_name+":\t")

		sparql_endpoint.setQuery('SELECT ?pro WHERE{  ?pro rdf:type rdf:Property . ?pro rdfs:label ?label . FILTER REGEX(STR(?label),\'^'+prop_name+'$\') . } ')
		sparql_endpoint.setReturnFormat(JSON)
		results=sparql_endpoint.query().convert()
		for result in results['results']['bindings']:
			print(result['pro']['value'])
			count+=1
print(count)
