import requests
import time
import re
from ontology_matching import OntologyMatching
from SPARQLWrapper import SPARQLWrapper, JSON


# def test_sparql_api():
# 	sparql = SPARQLWrapper("http://dbpedia.org/sparql")
# 	sparql.setQuery("""
# 	    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
# 	    SELECT ?label
# 	    WHERE { <http://dbpedia.org/resource/Asturias> rdfs:label ?label }
# 	""")
# 	sparql.setReturnFormat(JSON)
# 	results = sparql.query().convert()
#
# 	for result in results["results"]["bindings"]:
# 	    print(result["label"]["value"])

api_lookup = "http://lookup.dbpedia.org/api/search.asmx/KeywordSearch?QueryClass=&QueryString="
remainderItem = OntologyMatching.get_item("data/clz2entityAnim")
reStr="<URI>http://dbpedia.org/resource/.*</URI>"


def test_lookup(item):
	api_lookup="http://lookup.dbpedia.org/api/search.asmx/KeywordSearch?QueryClass=&QueryString="+item
	res=requests.get(api_lookup).content
	matchObjx=re.match(reStr,str(res,"utf-8"),re.I)
	if matchObjx:
		print(matchObjx.group()[5:matchObjx.group().rindex("</URI>")])

for line in remainderItem:
	item=line.split(";")[1].title().strip()
	test_lookup(item)
	time.sleep(1)

