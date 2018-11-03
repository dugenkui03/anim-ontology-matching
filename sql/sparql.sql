# 统计某各类的所有子类
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

# 查询Entity类的所有子类，配合utils和EntityClass、EntityClassURI数据集
select *
where{
?a <http://www.w3.org/2000/01/rdf-schema#subClassOf> <http://www.ontologyportal.org/translations/SUMO.owl.txt#Entity> .
optional{
?b <http://www.w3.org/2000/01/rdf-schema#subClassOf> ?a .
optional{
?c <http://www.w3.org/2000/01/rdf-schema#subClassOf> ?b .
optional{
?d <http://www.w3.org/2000/01/rdf-schema#subClassOf> ?c .
optional{
?e <http://www.w3.org/2000/01/rdf-schema#subClassOf> ?d .
optional{
?f <http://www.w3.org/2000/01/rdf-schema#subClassOf> ?e .
optional{
?g <http://www.w3.org/2000/01/rdf-schema#subClassOf> ?f .
}
}
}
}
}
}
}

某个类下边的实例：一层层剥减
select ?x
where{
   ?x rdf:type ?t1 .
   ?t1 rdfs:subClassOf ?t2 .
   ?t2 rdfs:subClassOf ?t3 .
   ?t3 rdfs:subClassOf ?t4 .
   ?t4 rdfs:subClassOf ?t5 .
   ?t5 rdfs:subClassOf ?t6 .
   ?t6   rdfs:subClassOf <http://www.ontologyportal.org/translations/SUMO.owl.txt#Entity> .
}