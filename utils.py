# import Levenshtein
# from nltk.corpus import wordnet as wn
# import nltk
from SPARQLWrapper import SPARQLWrapper, JSON
import threading
import time

sparql = SPARQLWrapper("http://dbpedia.org/sparql")
threadLock = threading.Lock()  # 全局锁
resultLock=threading.Lock() # 向结果数据集添加数据时用到的锁


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


animList = get_item("data/jaroWinklerAnim")
clz2entityList=[]

class LockThread(threading.Thread):
	def __init__(self, termList):
		threading.Thread.__init__(self)
		self.termList = termList

	def run(self):
		threadLock.acquire()
		term = self.termList.pop()
		threadLock.release()
		sparqlCheck(term)


def sparqlCheck(term):
	sparql.setQuery(
		"SELECT COUNT(*) as ?cou WHERE { <http://dbpedia.org/resource/" + term.title() + "> rdfs:label ?label }")
	sparql.setReturnFormat(JSON)
	results = sparql.query().convert()
	for result in results["results"]["bindings"]:
		if result["cou"]["value"]!="0":
			print(term + ":" + result["cou"]["value"])
			resultLock.acquire()
			clz2entityList.append(term)
			resultLock.release()

def getClas2Instance():
	threadList=[]
	cou=0
	while len(animList)!=0:
		cou+=1
		if cou%5==0:
			time.sleep(1)
		threadx=LockThread(animList)
		threadList.append(threadx)
		threadx.start()

	print(str(len(threadList))+"length")

	for t in threadList:
		t.join()
	return clz2entityList

#
# for term in listx:
#     sparql.setQuery("SELECT COUNT(*) as ?cou WHERE { <http://dbpedia.org/resource/"+term.title()+"> rdfs:label ?label }")
#     sparql.setReturnFormat(JSON)
#     results = sparql.query().convert()
#     for result in results["results"]["bindings"]:
#         print(result["cou"]["value"])
# for term in listx:
#     sparql.setQuery("""
#         PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
#         SELECT ?label
#         WHERE { <http://dbpedia.org/resource/Asturias> rdfs:label ?label }
#     """)
#     sparql.setReturnFormat(JSON)
#     results = sparql.query().convert()
#     for result in results["results"]["bindings"]:
#         print(result["label"]["value"])

# nltk.download('wordnet')


# s1="dugenkui"
# s2="dugenlong"
#
# print(Levenshtein.distance(s1, s2))
#
# Levenshtein.dis

# print("du,gen,kui".split(",")[3])

# print(Levenshtein.jaro_winkler("dugenlong", "dugenkui"))

# print(wn.synsets('wind'))
