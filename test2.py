import re

# str1="http://lookup.dbpedia.org/xxxxxxxxx"
# str2="<URI>http://dbpedia.org/resource/Patriot_Act</URI>"
#

# matchObj=re.match("<URI>http://dbpedia.org/resource/.*</URI>",str1,re.I)
# matchObjx=re.match("<URI>http://dbpedia.org/resource/.*</URI>",str2,re.I)
#
# if matchObj:
# 	print(matchObj.group())
#
# if matchObjx:
# 	print(matchObjx.group()[5:matchObjx.group().rindex("</URI>")])
#

#
# strxx="DefaultOWLNamedClass(http://www.owl-ontologies.com/Ontology1290308675.owl#PlacePlot);place;equal;<http://dbpedia.org/ontology/Place>"
#
# if ";equal;" in strxx:
# 	print(1111111111111)
# else:
# 	print(3333)
#
# re1 = re.compile(u'<http://.*?#(.*?)> <http://.*?#(.*?)> <http://.*?#(.*?)> .')
# re2 = re.compile(u'<http://.*?#(.*?)> <http://.*?#(.*?)> "(.*?)".*?<http://.*?> .')

def get_matched_info(file_path="data/animsynoClz2EntityAnim"):
	"""
	获取已经匹配的数据放进字典中，格式是<anim,dbpedia_term_uri>
	file_path
	"""
	with open(file_path) as anim_file:
		matched_anim_dict = {}
		regex = re.compile(".*;.*;.*")
		anim_content = anim_file.readlines()
		for anim_line in anim_content:
			m = regex.match(anim_line)
			if m:
				arr = str(m.group()).split(";")
				ele={}
				ele[arr[2]]=arr[3]
				matched_anim_dict[arr[1]] = ele

	return matched_anim_dict

# 字典格式<anim_term,dbpedia_term_uri> TODO：匹配方式也应该记录，因为有的是类2类，有的是类2实例——可以通过DBpedia的uri分析得到，但是不精确
dict_res=get_matched_info()

def complete_repeated_matched_data(matched_data_dict,matched_file_path="data/matchedAnim",data_file_path="data/animsynoClz2EntityAnim"):
	"""
	对于动画知识库中term相同但是只匹配上一个的情况，另一个term名称相同的anim_term也以相同的方式匹配到同一个DBpedia_term上。方式如下：
		遍历data_file_path中的数据行，如果此数据行是没有匹配上的数据(if not regex.match(anim_line)，并且anim_term可以在matched_data_dict中找到
		，则使用此数据行的term_uri构造新数据(term_uri,matched_way,matched_dbpedia_term_uri)
	:param matched_data_dict: 记录已经匹配上的数据，格式是<anim_term,<matched_way,matched_dbpedia_term_uri>>
	:param matched_file_path: 要写入的文件路径
	:param data_file_path:  数据来源文件
	:return:
	"""
	with open(matched_file_path,"w") as new_file:
		with open(data_file_path) as anim_file:
			regex=re.compile(".*;.*;.*")
			anim_content=anim_file.readlines()
			for anim_line in anim_content:
				"""
				如果是没有匹配上的数据"""
				if not regex.match(anim_line):
					"""
					如果是没有匹配上的，则需要处理:
					1. 查看是否有同名term已经匹配上DBpedia数据：
						1)如果有的话，则
					"""
					arr=anim_line.split(";")
					if arr[1].strip() in matched_data_dict.keys():
						print(arr[0],end="\t dugenkui")
						print(list(matched_data_dict[arr[1].strip()].keys())[0],end="\t dugenkui")
						print(matched_data_dict[arr[1].strip()][list(matched_data_dict[arr[1].strip()].keys())[0]])
						new_file.write(arr[0]+";"+list(matched_data_dict[arr[1].strip()].keys())[0]+";"+matched_data_dict[arr[1].strip()][list(matched_data_dict[arr[1].strip()].keys())[0]]+"\n")
					else:
						if anim_line.strip()=="":
							print("空格")
						print(anim_line)
						new_file.write(anim_line)
				else:
					if anim_line.strip() == "":
						print("空格")
					print(anim_line)
					new_file.write(anim_line)


