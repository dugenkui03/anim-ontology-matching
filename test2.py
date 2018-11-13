import re

str1="http://lookup.dbpedia.org/xxxxxxxxx"
str2="<URI>http://dbpedia.org/resource/Patriot_Act</URI>"


# matchObj=re.match("<URI>http://dbpedia.org/resource/.*</URI>",str1,re.I)
# matchObjx=re.match("<URI>http://dbpedia.org/resource/.*</URI>",str2,re.I)
#
# if matchObj:
# 	print(matchObj.group())
#
# if matchObjx:
# 	print(matchObjx.group()[5:matchObjx.group().rindex("</URI>")])
#


strxx="DefaultOWLNamedClass(http://www.owl-ontologies.com/Ontology1290308675.owl#PlacePlot);place;equal;<http://dbpedia.org/ontology/Place>"

if ";equal;" in strxx:
	print(1111111111111)
else:
	print(3333)

re1 = re.compile(u'<http://.*?#(.*?)> <http://.*?#(.*?)> <http://.*?#(.*?)> .')
re2 = re.compile(u'<http://.*?#(.*?)> <http://.*?#(.*?)> "(.*?)".*?<http://.*?> .')