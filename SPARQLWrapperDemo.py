from SPARQLWrapper import SPARQLWrapper, JSON

sparql = SPARQLWrapper("http://dbpedia.org/sparql")
sparql.setQuery(
# """
#     PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
#     SELECT ?label
#     WHERE { <http://dbpedia.org/resource/Asturias> rdfs:label ?label }
# """
"""
select ?label
where{
?label <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://schema.org/City> .
}
"""
)

sparql.setReturnFormat(JSON)
results = sparql.query().convert()

for result in results["results"]["bindings"]:
    print(result["label"]["value"])