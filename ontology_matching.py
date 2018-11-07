import Levenshtein
from utils import *


class OntologyMatching():
	"""
	 fixme 以下函数分析用，实际匹配需要修改文件
	"""

	def get_item(filePath):
		"""
		获取没有匹配的item数据行
		"""
		with open(filePath) as file:
			fileContent = file.readlines()
			res = []
			for line in fileContent:
				try:
					listx = line.split(";")
					if (len(listx) > 2):  # 如果已经匹配过
						continue
					# res.append(line.split(";")[1].strip())
					res.append(line.strip()) #获取没有匹配的item数据行,类似于  DefaultOWLNamedClass(http://www.owl-ontologies.com/Ontology1290308675.owl#TV);tv
				except:
					pass
				# print(line.strip() + " has no term")
		return res

	def match_two_list_equal(listx, listy):
		"""
		以字典的形式返回连个数据集的交集
		"""
		# res = [val for val in listx if val in listy]

		res={}
		for animLine in listx:
			animTerm=animLine.split(";")[1]
			for dbpediaLine in listy:
				dbpediaTerm=dbpediaLine.split(";")[1]
				if animTerm.strip() == dbpediaTerm.strip():
					res[animLine.split(";")[0]]= dbpediaLine.split(";")[0]
					break
		return res

	def match_two_list_levDis(listx, listy):
		"""
		编辑距离为1，而且字符串长度大于等于5
		"""
		res = {}
		for animLine in listx:
			animTerm=animLine.split(";")[1]
			for dbpediaLine in listy:
				dbpediaTerm=dbpediaLine.split(";")[1]
				if Levenshtein.distance(animTerm, dbpediaTerm) < 2 and len(animTerm) > 4 and len(dbpediaTerm) > 4:
					res[animLine.split(";")[0]]= dbpediaLine.split(";")[0]
		return res

	def match_two_list_ratio(listx, listy):
		"""
		编辑距离为1，而且字符串长度大于等于5
		"""
		res = {}
		for animLine in listx:
			animTerm=animLine.split(";")[1]
			for dbpediaLine in listy:
				dbpediaTerm=dbpediaLine.split(";")[1]
				if Levenshtein.ratio(animTerm, dbpediaTerm) > 0.75 and len(animTerm) > 4 and len(dbpediaTerm) > 4:
					res[animLine.split(";")[0]]= dbpediaLine.split(";")[0]
		return res

	def match_two_list_jaro(listx, listy):
		res = {}
		for animLine in listx:
			animTerm=animLine.split(";")[1]
			for dbpediaLine in listy:
				dbpediaTerm=dbpediaLine.split(";")[1]
				if Levenshtein.jaro(animTerm, dbpediaTerm) > 0.83 and len(animTerm) > 4 and len(dbpediaTerm) > 4:
					res[animLine.split(";")[0]] = dbpediaLine.split(";")[0]
		return res

	def match_two_list_jaroWinkler(listx, listy):
		res = {}
		for animLine in listx:
			animTerm=animLine.split(";")[1]
			for dbpediaLine in listy:
				dbpediaTerm=dbpediaLine.split(";")[1]
				if Levenshtein.jaro_winkler(animTerm, dbpediaTerm) > 0.95 and len(animTerm) > 4 and len(dbpediaTerm) > 4:
					res[animLine.split(";")[0]] = dbpediaLine.split(";")[0]
		return res

	"""
	 fixme 以下函数匹配并修改文件
	"""

	def someway_match(animPath, dbpediaPath, matchDict, matWay):
		"""
		创建新文件保存匹配上的term及匹配方式，例如 Book以equal的方式匹配上了，则两个文件相应列修改为： .../book,book->.../book,book,equal
		:param dbpediaPath: 需要被修改的文件路径
		:param matchDict:  匹配列表
		:param matWay:  匹配方式
		"""
		with open("data/" + matWay + "Anim", "w") as matchedAnim:
			with open(animPath) as animfile:
				animContent = animfile.readlines()
				for line in animContent:
					ele = line.split(";")[0].strip()
					if ele in matchDict.keys():
						matchedAnim.write(line.strip() + ";" + matWay +";"+matchDict[ele]+ "\n")
					else:
						matchedAnim.write(line.strip() + "\n")
		with open("data/" + matWay + "DBpedia", "w") as matchedDBpedia:
			with open(dbpediaPath) as dbpediaFile:
				dbpediaContent = dbpediaFile.readlines()
				for line in dbpediaContent:
					if line.split(";")[0].strip() in matchDict.values():
						content=line.strip() + ";" + matWay+";"+list(matchDict.keys())[list(matchDict.values()).index(line.split(";")[0].strip())]
						matchedDBpedia.write(line.strip() + ";" + matWay+";"+
											list(matchDict.keys())[list(matchDict.values()).index(line.split(";")[0].strip())]#fixme 根据value得到key
						                     + "\n")
					else:
						matchedDBpedia.write(line.strip() + "\n")

	def clz2entity_match(animPath,matchList):
		"""
		动画类对应实例，主要是查看 	"SELECT COUNT(*) as ?cou WHERE { <http://dbpedia.org/resource/" + term.title() + "> rdfs:label ?label }" 能不能查出东西
		"""
		with open("data/clz2entityAnim","w") as c2eAnim:
			with open(animPath) as animfile:
				animContent=animfile.readlines()
				for line in animContent:
					ele=line.split(";")[1].strip()
					if ele in matchList:
						c2eAnim.write(line.strip()+";clz2entity\n")
					else:
						c2eAnim.write(line.strip()+"\n")

	def dict_match(animPath, dbpediaPath, matchDict, matWay):
		"""
		创建新文件保存匹配上的term及匹配方式，例如 Book以equal的方式匹配上了，则两个文件相应列修改为： .../book,book->.../book,book,equal
		:param dbpediaPath: 需要被修改的文件路径
		:param matchList:  匹配列表
		:param matWay:  匹配方式
		"""
		with open("data/" + matWay + "Anim", "w") as matchedAnim:
			with open(animPath) as animfile:
				animContent = animfile.readlines()
				for line in animContent:
					ele = line.split(";")[0].strip()
					if ele in matchDict.keys():
						matchedAnim.write(line.strip() + ";" + matWay +";"+matchDict[ele] + "\n")
					else:
						matchedAnim.write(line.strip() + "\n")
		with open("data/" + matWay + "DBpedia", "w") as matchedDBpedia:
			with open(dbpediaPath) as dbpediaFile:
				dbpediaContent = dbpediaFile.readlines()
				for line in dbpediaContent:
					if line.split(";")[0].strip() in matchDict.values():
						matchedDBpedia.write(line.strip() + ";" + matWay +";"+
						                     list(matchDict.keys())[list(matchDict.values()).index(line.split(";")[0].strip())]+
						                     "\n")
					else:
						matchedDBpedia.write(line.strip() + "\n")


# 1.预处理term：统一到小写并去掉下划线分隔符；2.同义词匹配；3.anim中的类匹配dbpedia中的实例

def standardizing_data():
	"""
	将数据集anim和dbpedia格式化：统一为小写和去掉分隔符，然后保存在standXXX中
	"""
	with open("data/standanim", "w") as standanim:
		with open("data/anim") as animFile:
			animLines = animFile.readlines()
			for line in animLines:
				str = line.split(";")
				standanim.write(str[0] + ";" + str[1].strip().replace("_", "").lower() + "\n")

	with open("data/standdbpedia", "w") as standdbpedia:
		with open("data/dbpedia") as dbpediaFile:
			dbpediaLines = dbpediaFile.readlines()
			for line in dbpediaLines:
				str = line.split(";")
				standdbpedia.write(str[0] + ";" + str[1].strip().replace("_", "").lower() + "\n")


# 相等匹配
# animList = OntologyMatching.get_item("data/standanim")
# dbpediaList = OntologyMatching.get_item("data/standdbpedia")
# equalDict = OntologyMatching.match_two_list_equal(animList, dbpediaList)
# OntologyMatching.someway_match("data/standanim", "data/standdbpedia", equalDict, "equal")
#
# # 编辑距离为1匹配且字符串长度大于4的匹配
# animList = OntologyMatching.get_item("data/equalAnim")
# dbpediaList = OntologyMatching.get_item("data/equalDBpedia")
# disDict = OntologyMatching.match_two_list_levDis(animList, dbpediaList)
# OntologyMatching.dict_match("data/equalAnim", "data/equalDBpedia", disDict, "levdis")
#
# # ratio = (sum-dis)/sum > 0.75 而且字串长度大于4
# animList = OntologyMatching.get_item("data/levdisAnim")
# dbpediaList = OntologyMatching.get_item("data/levdisDBpedia")
# disDict = OntologyMatching.match_two_list_ratio(animList, dbpediaList)
# OntologyMatching.dict_match("data/levdisAnim", "data/levdisDBpedia", disDict, "ratio")
#
# # jaro  > 0.83 而且字串长度大于4
# animList = OntologyMatching.get_item("data/ratioAnim")
# dbpediaList = OntologyMatching.get_item("data/ratioDBpedia")
# disDict = OntologyMatching.match_two_list_jaro(animList, dbpediaList)
# OntologyMatching.dict_match("data/ratioAnim", "data/ratioDBpedia", disDict, "jaro")
#
# # jaroWinkler>0.95
# animList = OntologyMatching.get_item("data/jaroAnim")
# dbpediaList = OntologyMatching.get_item("data/jaroDBpedia")
# disDict = OntologyMatching.match_two_list_jaroWinkler(animList, dbpediaList)
# OntologyMatching.dict_match("data/jaroAnim", "data/jaroDBpedia", disDict, "jaroWinkler")
#
#
# # 动画类对实例
# clz2entityList=getClas2Instance()
# OntologyMatching.clz2entity_match("data/jaroWinklerAnim",clz2entityList)
#
# #lookup接口
# api_lookup="http://lookup.dbpedia.org/api/search.asmx/KeywordSearch?QueryClass=&QueryString="
# remainderItem=OntologyMatching.get_item("data/clz2entityAnim")

# for item in remainderItem:
