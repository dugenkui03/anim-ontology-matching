import re
import requests
import threading
import time

import bs4


ope_lock=threading.Lock()

class ThesauruThread(threading.Thread):
	def __init__(self,anim_line,syno_dic):
		threading.Thread.__init__(self)
		self.anim_line=anim_line
		self.syno_dic=syno_dic

	def run(self):
		find_syno_by_thesauru(self.anim_line,self.syno_dic)


def find_syno_by_thesauru(anim_line, syno_dic):
	"""
	返回term的近义词，数据结构为字典嵌套列表
	"""
	term = anim_line.split(";")[1].lower().strip()
	pattern = re.compile("/browse/[a-zA-Z]*")
	syno_api = "https://www.thesaurus.com/browse/"

	element_content = bs4.BeautifulSoup(requests.get(syno_api + term).content.decode("utf-8", "HTML")).find_all(id='loadingContainer')
	match_list = pattern.findall(str(element_content))

	resList = []
	for match_ele in match_list:
		if match_ele.split("/")[2] == term:
			continue
		resList.append(match_ele.split("/")[2])
	ope_lock.acquire()
	# print(str(anim_line.split(";")[0].lower().strip())+":\t"+str(resList))
	syno_dic[anim_line.split(";")[0].lower().strip()] = resList
	ope_lock.release()


dbpedia_term_list=[]
with open("data/dbpedia") as dbpedia_file:
	dbpedia_content=dbpedia_file.readlines()
	for dbpedia_line in dbpedia_content:
		dbpedia_term_list.append(dbpedia_line.split(";")[1].lower().strip())


syno_dic={}
threadList=[]
cou=1
with open("data/anim") as anim_file:
	anim_content=anim_file.readlines()
	for anim_line in anim_content:
		cou+=1
		# if cou>66:
		# 	break
		threadx=ThesauruThread(anim_line,syno_dic)
		threadList.append(threadx)
		threadx.start()
		time.sleep(0.005)

	for t in threadList:
		t.join()

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
