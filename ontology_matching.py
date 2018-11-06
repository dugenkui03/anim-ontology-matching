import Levenshtein


class OntologyMatching():
	"""
	 fixme 以下函数分析用，实际匹配需要修改文件
	"""
	def get_item(filePath):
		with open(filePath) as file:
			fileContent = file.readlines()
			res = []
			for line in fileContent:
				try:
					listx=line.split(";")
					if(len(listx)>2):#如果已经匹配过
						continue
					res.append(line.split(";")[1].strip())
				except:
					pass
					# print(line.strip() + " has no term")
		return res

	def match_two_list_equal(listx, listy):
		"""
		返回两个列表的交集
		"""
		res=[val for val in listx if val in listy]
		return res

	def match_two_list_levDis(listx,listy):
		"""
		编辑距离为1，而且字符串长度大于等于5
		"""
		res={}
		for x in listx:
			for y in listy:
				if Levenshtein.distance(x,y)<2 and len(x)>4 and len(y)>4:
					res[x]=y
		return res

	def match_two_list_ratio(listx,listy):
		"""
		编辑距离为1，而且字符串长度大于等于5
		"""
		res={}
		for x in listx:
			for y in listy:
				if Levenshtein.ratio(x,y)>0.75 and len(x)>4 and len(y)>4:
					res[x]=y
		return res

	def match_two_list_jaro(listx,listy):
		res={}
		for x in listx:
			for y in listy:
				if Levenshtein.jaro(x,y)>0.83 and len(x)>4 and len(y)>4:
					res[x]=y
		return res

	def match_two_list_jaroWinkler(listx,listy):
		res={}
		for x in listx:
			for y in listy:
				if Levenshtein.jaro_winkler(x,y)>0.95 and len(x)>4 and len(y)>4:
					res[x]=y
		return res

	"""
	 fixme 以下函数匹配并修改文件
	"""
	def someway_match(animPath, dbpediaPath, matchList, matWay):
		"""
		创建新文件保存匹配上的term及匹配方式，例如 Book以equal的方式匹配上了，则两个文件相应列修改为： .../book,book->.../book,book,equal
		:param dbpediaPath: 需要被修改的文件路径
		:param matchList:  匹配列表
		:param matWay:  匹配方式
		"""
		with open("data/"+matWay+"Anim","w") as matchedAnim:
			with open(animPath) as animfile:
				animContent=animfile.readlines()
				for line in animContent:
					ele=line.split(";")[1].strip()
					if  ele in matchList:
						matchedAnim.write(line.strip()+";"+matWay+"\n")
					else:
						matchedAnim.write(line.strip()+"\n")
		with open("data/"+matWay+"DBpedia","w") as matchedDBpedia:
			with open(dbpediaPath) as dbpediaFile:
				dbpediaContent=dbpediaFile.readlines()
				for line in dbpediaContent:
					if line.split(";")[1].strip() in matchList:
						matchedDBpedia.write(line.strip()+";"+matWay+"\n")
					else:
						matchedDBpedia.write(line.strip()+"\n")

	def dict_match(animPath, dbpediaPath, matchDict, matWay):
		"""
		创建新文件保存匹配上的term及匹配方式，例如 Book以equal的方式匹配上了，则两个文件相应列修改为： .../book,book->.../book,book,equal
		:param dbpediaPath: 需要被修改的文件路径
		:param matchList:  匹配列表
		:param matWay:  匹配方式
		"""
		with open("data/"+matWay+"Anim","w") as matchedAnim:
			with open(animPath) as animfile:
				animContent=animfile.readlines()
				for line in animContent:
					ele=line.split(";")[1].strip()
					if  ele in matchDict.keys():
						matchedAnim.write(line.strip()+";"+matWay+"\n")
					else:
						matchedAnim.write(line.strip()+"\n")
		with open("data/"+matWay+"DBpedia","w") as matchedDBpedia:
			with open(dbpediaPath) as dbpediaFile:
				dbpediaContent=dbpediaFile.readlines()
				for line in dbpediaContent:
					if line.split(";")[1].strip() in matchDict.values():
						matchedDBpedia.write(line.strip()+";"+matWay+"\n")
					else:
						matchedDBpedia.write(line.strip()+"\n")



# 相等匹配
animList=OntologyMatching.get_item("data/anim")
dbpediaList=OntologyMatching.get_item("data/dbpedia")
equalList = OntologyMatching.match_two_list_equal(animList, dbpediaList)
OntologyMatching.someway_match("data/anim", "data/dbpedia", equalList, "equal")

# 编辑距离为1匹配且字符串长度大于4的匹配
animList=OntologyMatching.get_item("data/equalAnim")
dbpediaList=OntologyMatching.get_item("data/equalDBpedia")
disDict=OntologyMatching.match_two_list_levDis(animList, dbpediaList)
OntologyMatching.dict_match("data/equalAnim", "data/equalDBpedia", disDict, "levdis")

# ratio = (sum-dis)/sum > 0.75 而且字串长度大于4
animList=OntologyMatching.get_item("data/levdisAnim")
dbpediaList=OntologyMatching.get_item("data/levdisDBpedia")
disDict=OntologyMatching.match_two_list_ratio(animList,dbpediaList)
OntologyMatching.dict_match("data/levdisAnim", "data/levdisDBpedia", disDict, "ratio")

# jaro  > 0.83 而且字串长度大于4
animList=OntologyMatching.get_item("data/ratioAnim")
dbpediaList=OntologyMatching.get_item("data/ratioDBpedia")
disDict=OntologyMatching.match_two_list_jaro(animList,dbpediaList)
OntologyMatching.dict_match("data/ratioAnim", "data/ratioDBpedia", disDict, "jaro")

animList=OntologyMatching.get_item("data/jaroAnim")
dbpediaList=OntologyMatching.get_item("data/jaroDBpedia")
disDict=OntologyMatching.match_two_list_jaroWinkler(animList,dbpediaList)
OntologyMatching.dict_match("data/jaroAnim", "data/jaroDBpedia", disDict, "jaroWinkler")

# todo
# 1.之前说的下划线没去掉；
# 1.统一大小写和分隔符；