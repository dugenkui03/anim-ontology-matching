import re
import requests
import threading
import time

import bs4


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
	syno_dic[anim_line.split(";")[0].lower().strip()] = resList
	ope_lock.release()



# 获取dbpedia中所有term放进列表
dbpedia_term_list=[]
with open("data/wordNet_synoDBpedia") as dbpedia_file:
	dbpedia_content=dbpedia_file.readlines()
	for dbpedia_line in dbpedia_content:
		dbpedia_term_list.append(dbpedia_line.split(";")[1].lower().strip())


syno_dic={}
threadList=[]
with open("data/wordNet_synoAnim") as anim_file:
	"""
	1.查找anim_term的近义词；
	2.如果近义词能在dbpedia_term中找到，则设置对应关系，可以多对多
	"""

	# 查找anim_term的近义词；
	anim_content=anim_file.readlines()
	for anim_line in anim_content:
		threadx=ThesauruThread(anim_line,syno_dic)
		threadList.append(threadx)
		threadx.start()
		time.sleep(0.01)
	for t in threadList:
		t.join()

	# 如果近义词能在dbpedia_term中找到，则设置对应关系，可以多对多
	syno_list_ele=syno_dic.values()
	for syno_list in syno_list_ele:
		for anim_syno_term in syno_list:
			if anim_syno_term in dbpedia_term_list:
				print(
					str(
						list(syno_dic.keys())[list(syno_dic.values()).index(syno_list)]
					)
					                          +":\t"+anim_syno_term
					    )
