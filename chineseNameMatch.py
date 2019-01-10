import re

from SPARQLWrapper import SPARQLWrapper,JSON


"""
todo :label与ChineseName匹配
"""

sparql=SPARQLWrapper("http://dbpedia.org/sparql")

with open("data/chineseName_data/chineseNameResource",encoding="utf8") as chineseName_file:
	pat=re.compile("[\u4e00-\u9fa5]{1,}")
	chineseName_file_content=chineseName_file.readlines()
	for line in chineseName_file_content:
		chiese_name=pat.findall(line)[0]
		print(chiese_name)
		sparql.setQuery(
			"""
				select ?obj,?label,strlen(?label) as ?cou where{
					?obj rdfs:label ?label .
					FILTER REGEX(STR(?label),\""""+chiese_name+"""\") .
				}order by strlen(?label)
			"""
		)
		sparql.setReturnFormat(JSON)
		results=sparql.query().convert()
		print(sparql.queryString)
		for result in results["results"]["bindings"]:
			print(result["obj"]["value"]+result["label"]["value"]+result["cou"]["value"])
