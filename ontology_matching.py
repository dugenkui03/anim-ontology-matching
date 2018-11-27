import Levenshtein
from nltk.corpus import wordnet as wn
from SPARQLWrapper import SPARQLWrapper, JSON

import threading
import time
import re
import requests
import bs4

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

	def get_item_without_filter(filePath):
		"""
		获取所有item数据行，因为有的数据可以重复匹配
		"""
		with open(filePath) as file:
			fileContent = file.readlines()
			res = []
			for line in fileContent:
				try:
					# listx = line.split(";")
					# if (len(listx) > 2):  # 如果已经匹配过
					# 	continue
					# res.append(line.split(";")[1].strip())
					res.append(line.strip()) #获取没有匹配的item数据行,类似于  DefaultOWLNamedClass(http://www.owl-ontologies.com/Ontology1290308675.owl#TV);tv
				except:
					pass
				# print(line.strip() + " has no term")
		return res

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
					ele = {}
					ele[arr[2]] = arr[3]
					matched_anim_dict[arr[1]] = ele
		#对字典进行排序，按照key，item:item[1]表示按照value元素进行排序。fixme：1.返回的是list；2.不会修改原始数据，因此需要用引用接收修改后的数据
		# matched_anim_dict=sorted(matched_anim_dict.items(), key=lambda item: item[0])
		return matched_anim_dict

	def complete_repeated_matched_data(matched_data_dict, matched_file_path="data/finalMatchedAnim",
	                                   data_file_path="data/animThesuaruSynoClz2EntityAnim"):
		"""
		对于动画知识库中term相同但是只匹配上一个的情况，另一个term名称相同的anim_term也以相同的方式匹配到同一个DBpedia_term上。方式如下：
			遍历data_file_path中的数据行，如果此数据行是没有匹配上的数据(if not regex.match(anim_line)，并且anim_term可以在matched_data_dict中找到
			，则使用此数据行的term_uri构造新数据(term_uri,matched_way,matched_dbpedia_term_uri)
		:param matched_data_dict: 记录已经匹配上的数据，格式是<anim_term,<matched_way,matched_dbpedia_term_uri>>
		:param matched_file_path: 要写入的文件路径
		:param data_file_path:  数据来源文件
		:return:
		"""
		with open(matched_file_path, "w") as new_file:
			with open(data_file_path) as anim_file:
				regex = re.compile(".*;.*;.*")
				anim_content = anim_file.readlines()
				for anim_line in anim_content:
					"""
					如果是没有匹配上的数据"""
					if not regex.match(anim_line):
						"""
						如果是没有匹配上的，则需要处理:
						1. 查看是否有同名term已经匹配上DBpedia数据：
							1)如果有的话，则 
						"""
						arr = anim_line.split(";")
						if arr[1].strip() in matched_data_dict.keys():
							# print(arr[0] + ";" +arr[1].strip()+";"+ list(matched_data_dict[arr[1].strip()].keys())[0] + ";" +
							#                matched_data_dict[arr[1].strip()][
							# 	               list(matched_data_dict[arr[1].strip()].keys())[0]] + "\n")
							new_file.write(arr[0] + ";"  +arr[1].strip()+";"+ list(matched_data_dict[arr[1].strip()].keys())[0] + ";" +
							               matched_data_dict[arr[1].strip()][
								               list(matched_data_dict[arr[1].strip()].keys())[0]] + "\n")
						else:
							new_file.write(anim_line)
					else:
						new_file.write(anim_line)

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
					matched_dbpedia_term_uri=line.split(";")[0]
					if matched_dbpedia_term_uri in matchDict.values():
						content=line.strip() + ";" + matWay+";"+list(matchDict.keys())[list(matchDict.values()).index(line.split(";")[0].strip())]
						matchedDBpedia.write(line.strip() + ";" + matWay+";"+
											list(matchDict.keys())[list(matchDict.values()).index(line.split(";")[0].strip())]#fixme 根据value得到key
						                     + "\n")
					else:
						matchedDBpedia.write(line.strip() + "\n")

	def match_two_list_equal(animList, dbpediaList):
		"""
		以字典的形式返回连个数据集的交集
		"""
		res={}
		for animLine in animList:
			animTerm=animLine.split(";")[1]
			for dbpediaLine in dbpediaList:
				dbpediaTerm=dbpediaLine.split(";")[1]
				if animTerm.strip() == dbpediaTerm.strip():
					res[animLine.split(";")[0]]= dbpediaLine.split(";")[0]
					# break fixme 可以多对多
		return res


	def get_wordNet_syno_dic(placeholder):
		"""
			1.获取anim term对应的近义词列表；
			2.如果anim_term的近义词可以再dbpedia中找到，则将(anim_term_uri,dbpedia_term_uri)加入到字典。可以多对多；
			3. todo: 可以多对多，但是不在去匹配已经精确匹配的数据
		"""
		res = {}

		dbpedia_term_dict = {}
		with open("data/equalDBpedia") as dbpedia_file:
			"""
			获取dbpedia数据键值对，key是term，value是uri，例如：
			'q5','<http://wikidata.dbpedia.org/resource/q5>'
			"""
			dbpedia_content = dbpedia_file.readlines()
			for line in dbpedia_content:
				# fixme 不去匹配已经精确匹配的数据
				if len(line.split(";")) > 2:
					continue
				dbpedia_term_dict[line.split(";")[1].lower().strip()] = line.split(";")[0].strip()

		with open("data/equalAnim") as anim_file:
			animContent = anim_file.readlines()
			for anim_line in animContent:
				# fixme 不去匹配已经精确匹配的数据
				if ";equal;" in anim_line:
					continue
				# 获取近义词列表
				anim_term = anim_line.split(";")[1].strip()
				syno_list = wn.synsets(anim_term)
				for anim_term_syno_info in syno_list:
					# 如果anim_term的近义词可以再dbpedia中找到，则将(anim_term_uri,dbpedia_term_uri)加入到字典。可以多对多
					syn_term_syno = anim_term_syno_info.name().split(".")[0]
					if syn_term_syno != anim_term and syn_term_syno in dbpedia_term_dict.keys():
						res[anim_line.split(";")[0]] = dbpedia_term_dict[syn_term_syno]
		return res


	def get_thesauru_syno_dic(dbpedia_term_dict):
		"""
		同上：
		1.获取anim term对应的近义词列表；
		2.如果anim_term的近义词可以再dbpedia中找到，则将(anim_term_uri,dbpedia_term_uri)加入到字典。可以多对多；
		3. todo: 可以多对多，但是不在去匹配已经精确匹配的数据
		"""
		res={}
		# anim_term_uri及term的近义词，格式是<uri,list<syno_word>>
		anim_syno_dic = {}
		threadList = []
		with open("data/wordNet_synoAnim") as anim_file:
			"""
			1.查找anim_term的近义词；
			2.如果近义词能在dbpedia_term中找到，则设置对应关系，可以多对多
			"""
			# 查找anim_term的近义词；
			anim_content = anim_file.readlines()
			# cout=0
			for anim_line in anim_content:
				# 不匹配已经匹配的数据
				if len(anim_line.split(";"))>2 :
					continue
				# cout+=1
				# if cout>100 :
				# 	break
				# 第二个参数保存值
				threadx = ThesauruThread(anim_line, anim_syno_dic)
				threadList.append(threadx)
				threadx.start()
				time.sleep(0.01)
			#等待所有查询完成在继续运行“启动线程”
			for t in threadList:
				t.join()

			# 如果近义词能在dbpedia_term中找到，则设置对应关系，可以多对多
			# 获取所有的anim_term的近义词列表
			syno_list_list = anim_syno_dic.values()
			for syno_list in syno_list_list:
				# 遍历某个term对应的近义词，查看是否能在dbpedia_term中找到相同的
				for anim_syno_term in syno_list:
					if anim_syno_term in dbpedia_term_dict.keys():
						# fixme 打印日志
						print(str(list(anim_syno_dic.keys())[list(anim_syno_dic.values()).index(syno_list)])+"的近义词"+anim_syno_term+
						      "在dbpedia中,对应dbpedia_ter为"+dbpedia_term_dict[anim_syno_term])
						res[
							list(anim_syno_dic.keys())[list(anim_syno_dic.values()).index(syno_list)]
						]=dbpedia_term_dict[anim_syno_term]
		return res


	def get_wrodNet_syno_dict_for_anim2Entity(anim_file_path):
		"""
		1. 获取anim_term对应的近义词列表，封装在字典中，精度控制到前五个；
		2. 网络接口查询这些近义词有没有对应的DBpedia实例，有则将<anim_term_uri,DBpedia实例_uri>放进字典。
		"""
		res={}
		threadlist=[]
		print("动画term的wordNet近义词对应DBpedia实例：")
		with open(anim_file_path) as anim_file:
			anim_content=anim_file.readlines()
			for anim_line in anim_content:
				if len(anim_line.split(";"))>2 :
					#不去匹配已经匹配的数据
					continue
				anim_term=anim_line.split(";")[1].strip()
				syno_list=wn.synsets(anim_term)
				for anim_term_syno_info in syno_list:
					syno_term_word=anim_term_syno_info.name().split(".")[0]
					if syno_term_word!=anim_term:
						threadx=Term2Entity(syno_term_word+";"+anim_line.split(";")[0].strip(),res)
						threadlist.append(threadx)
						threadx.start()
						time.sleep(0.005)

		for t in threadlist:
			t.join()

		return res

	def get_thesauru_syno_dict_for_anim2Entity(anim_file_path):
		"""
		1. 获取anim_term对应的近义词列表，封装在字典中，精度控制到前五个；
		2. 网络接口查询这些近义词有没有对应的DBpedia实例，有则将<anim_term_uri,DBpedia实例_uri>放进字典。
		"""
		res={}
		threadlist=[]
		pattern = re.compile("/browse/[a-zA-Z]*")
		syno_api = "https://www.thesaurus.com/browse/"
		print("动画term的thesauru近义词对应DBpedia实例：")
		with open(anim_file_path) as anim_file:
			anim_content=anim_file.readlines()
			for anim_line in anim_content:
				#不去匹配已经匹配的数据
				if len(anim_line.split(";"))>2 :
					continue
				anim_term=anim_line.split(";")[1].strip()

				element_content = bs4.BeautifulSoup(
					requests.get(syno_api + anim_term).content.decode("utf-8", "HTML")).find_all(id='loadingContainer')
				match_list = pattern.findall(str(element_content))

				syno_list = []
				count = 0
				for match_ele in match_list:
					count += 1
					if count > syno_list_capacity-4:
						break;
					if match_ele.split("/")[2] == anim_term:
						continue
					syno_list.append(match_ele.split("/")[2])

				for syno_term_word in syno_list:
					if syno_term_word!=anim_term:
						threadx=Term2Entity(syno_term_word+";"+anim_line.split(";")[0].strip(),res)
						threadlist.append(threadx)
						threadx.start()
						time.sleep(0.01)

		for t in threadlist:
			t.join()

		return res

class Term2Entity(threading.Thread):
	"""
	寻找term对应的DBpedia实例，并将结果放进字典参数
	"""
	def __init__(self,anim_info_line,res_dict):
		threading.Thread.__init__(self)
		self.anim_info_line=anim_info_line
		self.res_dict=res_dict

	def run(self):
		anim_term2_dbpedia_ins(self.anim_info_line,self.res_dict)


def anim_term2_dbpedia_ins(anim_info_line,res_dict):
	"""
	如果anim_info_line的term在dbpedia中可以查询到实例，则将<term_uri,dbpedia_instance_uri>放入字典
	anim_info_line内容形式<近义词，anim_term_uri>：television;DefaultOWLNamedClass(http://www.owl-ontologies.com/Ontology1290308675.owl#TV)
	"""
	term_syno=anim_info_line.split(";")[0].strip()
	term_uri=anim_info_line.split(";")[1].strip()
	sparql.setQuery("SELECT COUNT(*) as ?cou WHERE { <http://dbpedia.org/resource/" + term_syno.title() + "> rdfs:label ?label }")
	sparql.setReturnFormat(JSON)
	results = sparql.query().convert()
	for result in results["results"]["bindings"]:
		if result["cou"]["value"]!="0" and result["cou"]["value"]!="1":
			print(term_syno+":\t"+str(term_uri)+":\t"+"<http://dbpedia.org/resource/"+str(term_syno.title())+">")
			add_data_lock.acquire()
			res_dict[term_uri]="<http://dbpedia.org/resource/"+term_syno.title()+">"
			add_data_lock.release()

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


	def clz2entity_match(animPath,clz2entityList):
		"""
		动画类对应实例，主要是查看 	"SELECT COUNT(*) as ?cou WHERE { <http://dbpedia.org/resource/" + term.title() + "> rdfs:label ?label }" 能不能查出东西
		"""
		with open("data/clz2entityAnim","w") as c2eAnim:
			with open(animPath) as animfile:
				animContent=animfile.readlines()
				for line in animContent:
					ele=line.split(";")[1].strip()
					if ele in clz2entityList:
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

ope_lock=threading.Lock()
syno_list_capacity=5
class ThesauruThread(threading.Thread):
	""""
	每个任务进行一次网络调用，去查询一次网络词典
	"""
	def __init__(self,anim_line,syno_dic):
		threading.Thread.__init__(self)
		self.anim_line=anim_line
		self.syno_dic=syno_dic

	def run(self):
		find_syno_by_thesauru(self.anim_line,self.syno_dic)

def find_syno_by_thesauru(anim_line, syno_dic):
	"""
	fixme 将anim_line中anim_term对应的anim_term_uri及近义词放进词典
	"""
	term = anim_line.split(";")[1].lower().strip()
	pattern = re.compile("/browse/[a-zA-Z]*")
	syno_api = "https://www.thesaurus.com/browse/"

	element_content = bs4.BeautifulSoup(requests.get(syno_api + term).content.decode("utf-8", "HTML")).find_all(id='loadingContainer')
	match_list = pattern.findall(str(element_content))

	resList = []
	count=0
	for match_ele in match_list:
		count+=1
		if count>syno_list_capacity :
			break;
		if match_ele.split("/")[2] == term:
			continue
		resList.append(match_ele.split("/")[2])
	ope_lock.acquire()
	# print(str(anim_line.split(";")[0].lower().strip())+":\t"+str(resList))
	syno_dic[anim_line.split(";")[0].strip()] = resList
	ope_lock.release()


def standardizing_data():
	"""
	1.统一到小写；
	2.去掉分隔符_和非中心词:topic、template
	"""
	with open("data/standanim", "w") as standanim:
		with open("data/anim") as animFile:
			animLines = animFile.readlines()
			for line in animLines:
				str = line.split(";")
				standanim.write(str[0] + ";" + str[1].strip().lower().replace("_", "").replace("topic","").replace("template","").replace("scene","").replace("marelated","").replace("related","").replace("plot","")+ "\n")

	#fixme  dbpedia数据统一大小写即可
	with open("data/standdbpedia", "w") as standdbpedia:
		with open("data/dbpedia") as dbpediaFile:
			dbpediaLines = dbpediaFile.readlines()
			for line in dbpediaLines:
				str = line.split(";")
				standdbpedia.write(str[0] + ";" + str[1].strip().lower() + "\n")


def get_term_dict(filePath, isFilter=1):
	"""
	获取此路径下的数据的term与其term_uri，放进词典;<uri,term>
	:param filePath:
	:param isFilter:  是否过滤已经匹配的数据
	:return:
	"""
	term_dict = {}
	with open(filePath) as dbpedia_file:
		dbpedia_content = dbpedia_file.readlines()
		for dbpedia_line in dbpedia_content:
			split_word=dbpedia_line.split(";")
			if isFilter and len(split_word)>2:
				continue
			term_dict[split_word[1].strip()]=(split_word[0])
	return term_dict

sparql = SPARQLWrapper("http://dbpedia.org/sparql")
remove_data_lock = threading.Lock()  # 全局锁
add_data_lock=threading.Lock()



def get_item(filePath):
	with open(filePath) as file:
		fileContent = file.readlines()
		res = []
		for line in fileContent:
			try:
				listx = line.split(";")
				if (len(listx) > 2):  # 如果已经匹配过
					continue
				res.append(line.split(";")[1].strip())
			except:
				pass
	# print(line.strip() + " has no term")
	return res

class SparqlCheckThread(threading.Thread):
	def __init__(self, anim_term_dict,res_dict):
		threading.Thread.__init__(self)
		self.anim_term_dict = anim_term_dict
		self.res_dict=res_dict

	def run(self):
		sparqlCheck(self.anim_term_dict,self.res_dict)

def sparqlCheck(anim_term_dict,res_dict):
	"""
	从字典中移除一个元素并进行sparql查询，存在相应实例则放进结果集
	"""
	remove_data_lock.acquire()
	#获取需要删除的key
	term=list(anim_term_dict.keys()).pop()
	# 删除元素并备份term_uri
	term_uri=anim_term_dict[term]
	del anim_term_dict[term]
	remove_data_lock.release()

	sparql.setQuery("SELECT COUNT(*) as ?cou WHERE { <http://dbpedia.org/resource/" + term.title() + "> rdfs:label ?label }")
	sparql.setReturnFormat(JSON)
	results = sparql.query().convert()
	for result in results["results"]["bindings"]:
		if result["cou"]["value"]!="0" and result["cou"]["value"]!="1":
			print(str(term_uri)+":"+"<http://dbpedia.org/resource/"+str(term.title())+">")
			add_data_lock.acquire()
			res_dict[term_uri]="<http://dbpedia.org/resource/"+term.title()+">"
			add_data_lock.release()

def animClz2dbIns(anim_dict):
	res={}
	threadList=[]
	cou=0
	print("动画类对应DBpedia实例")
	while len(anim_dict)!=0:
		cou+=1
		if cou%5==0:
			time.sleep(0.5)
		threadx=SparqlCheckThread(anim_dict,res)
		threadList.append(threadx)
		threadx.start()

	for t in threadList:
		t.join()
	return res



# 标准化数据
# standardizing_data()

# 相等匹配:103(比之前多了近一倍）
# animList = OntologyMatching.get_item("data/standanim")
# dbpediaList = OntologyMatching.get_item("data/standdbpedia")
# equalDict = OntologyMatching.match_two_list_equal(animList, dbpediaList)
# OntologyMatching.someway_match("data/standanim", "data/standdbpedia", equalDict, "equal")

# # wordNet匹配
# syno_dict = OntologyMatching.get_wordNet_syno_dic("none")
# OntologyMatching.someway_match("data/equalAnim", "data/equalDBpedia", syno_dict, "wordNet_syno")
#
# #thesuaru匹配：精度控制5，即前五个同义词
# dbpedia_term_dict=get_term_dict("data/wordNet_synoDBpedia", 1)
# thesauru_dict=OntologyMatching.get_thesauru_syno_dic(dbpedia_term_dict)
# OntologyMatching.someway_match("data/wordNet_synoAnim", "data/wordNet_synoDBpedia", thesauru_dict, "thesuaru_syno")

#动画类对应DBpedia_category没有效果，程序备份在commit中

# 动画类对实例:360个。FIXME：animClz2EntityDBpedia中是没有类对应到实例的相关数据的，因为实例信息是通过网络查询sparql获取的，仅仅在animClz2EntityAnim中可见
# anim_dict = get_term_dict("data/thesuaru_synoAnim",1)
# clz2entityDict=animClz2dbIns(anim_dict)
# OntologyMatching.someway_match("data/thesuaru_synoAnim", "data/thesuaru_synoDBpedia", clz2entityDict, "animClz2Entity")


# 动画类wordNet近义词对实例:155个
# wordNet_syno_dict_for_anim2Entity=OntologyMatching.get_wrodNet_syno_dict_for_anim2Entity("data/animClz2EntityAnim")
# OntologyMatching.someway_match("data/animClz2EntityAnim", "data/animClz2EntityDBpedia", wordNet_syno_dict_for_anim2Entity, "animWordNetsynoClz2Entity")
#

# 动画类thesuaru近义词匹配实体
# thesuaru_syno_dict_for_anim2Entity=OntologyMatching.get_thesauru_syno_dict_for_anim2Entity("data/animWordNetsynoClz2EntityAnim")
# OntologyMatching.someway_match("data/animWordNetsynoClz2EntityAnim", "data/animWordNetsynoClz2EntityDBpedia", thesuaru_syno_dict_for_anim2Entity, "animThesuaruSynoClz2Entity")

# 动画知识库term命名会有重复，比如两个humna，一个指生物个体，子类是头胸腹，一个是指物种，子类是男女老少；
# 处理方式：没匹配的数据与其同名的匹配上的term匹配到同一个DBpedia数据就好。
# anim_matched_data_dict=OntologyMatching.get_matched_info("data/animThesuaruSynoClz2EntityAnim")# 有默认路径data/animsynoClz2EntityAnim
# OntologyMatching.complete_repeated_matched_data(anim_matched_data_dict)

"""
对于类匹配：获取DBpedia—schema类下的所有实例(fixme 接口最多可获取1w个实例)，数据格式如下：
<类信息>
uri_1
uri_2
...
如：
<http://dbpedia.org/ontology/Person>
http://dbpedia.org/resource/Andreas_Ekberg
http://dbpedia.org/resource/Danilo_Tognon
http://dbpedia.org/resource/Lorine_Livington_Pruette
...
<http://dbpedia.org/ontology/Animal>
http://dbpedia.org/resource/Amblycera
http://dbpedia.org/resource/Amblyopsidae
http://dbpedia.org/resource/American_black_bear
http://dbpedia.org/resource/American_pickerel
...
"""
equal_list=["equal","wordNet_syno","thesuaru_syno"]


# 编辑距离为1匹配且字符串长度大于4的匹配
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

#
# #lookup接口
# api_lookup="http://lookup.dbpedia.org/api/search.asmx/KeywordSearch?QueryClass=&QueryString="
# remainderItem=OntologyMatching.get_item("data/clz2entityAnim")

# for item in remainderItem: