#统计某各类的所有子类
select *
where{
?a <http://www.w3.org/2000/01/rdf-schema#subClassOf> <http://dbpedia.org/ontology/Person> .
optional{
?b <http://www.w3.org/2000/01/rdf-schema#subClassOf> ?a .
optional{
?c <http://www.w3.org/2000/01/rdf-schema#subClassOf> ?b .
optional{
?d <http://www.w3.org/2000/01/rdf-schema#subClassOf> ?c .
}
}
}
}

select COUNT(DISTINCT(?a))+COUNT(DISTINCT(?b))+COUNT(DISTINCT(?c))+COUNT(DISTINCT(?d)) as ?x4
where{
?a <http://www.w3.org/2000/01/rdf-schema#subClassOf> <http://dbpedia.org/ontology/Person> .
optional{
?b <http://www.w3.org/2000/01/rdf-schema#subClassOf> ?a .
optional{
?c <http://www.w3.org/2000/01/rdf-schema#subClassOf> ?b .
optional{
?d <http://www.w3.org/2000/01/rdf-schema#subClassOf> ?c .
}
}
}
}