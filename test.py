import requests

from SPARQLWrapper import SPARQLWrapper, JSON


def test_sparql_api():
	sparql = SPARQLWrapper("http://dbpedia.org/sparql")
	sparql.setQuery("""
	    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
	    SELECT ?label
	    WHERE { <http://dbpedia.org/resource/Asturias> rdfs:label ?label }
	""")
	sparql.setReturnFormat(JSON)
	results = sparql.query().convert()

	for result in results["results"]["bindings"]:
	    print(result["label"]["value"])


def test_lookup():
	api_lookup="http://lookup.dbpedia.org/api/search.asmx/KeywordSearch?QueryClass=&QueryString="
	res=requests.get(api_lookup+"gymnast").content

