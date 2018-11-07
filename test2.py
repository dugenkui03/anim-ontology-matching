import re

str1="http://lookup.dbpedia.org/xxxxxxxxx"
str2="<URI>http://dbpedia.org/resource/Patriot_Act</URI>"


matchObj=re.match("<URI>http://dbpedia.org/resource/.*</URI>",str1,re.I)
matchObjx=re.match("<URI>http://dbpedia.org/resource/.*</URI>",str2,re.I)

if matchObj:
	print(matchObj.group())

if matchObjx:
	print(matchObjx.group()[5:matchObjx.group().rindex("</URI>")])



