import re
import time
import requests
import threading

from ontology_matching import OntologyMatching


class LookUpThread(threading.Thread):
	"""
	1. 从一个列表中取item；
	2. 在lookup接口中查找item：
		2.1 如果能找到就添加到字典中：[anim_item_uri,dbpedia_resource_instance_uri]
		2.2 找不到则pass；
	"""

	def __init__(self, animList):
		threading.Thread.__init__(self)
		self.animList = animList

	def run(self):
		listLockForLookUp.acquire()
		try:
			animLine = self.animList.pop()
			test_lookup(animLine)# todo something
		except:
			pass
		listLockForLookUp.release()

def test_lookup(animLine):
	item=animLine.split(";")[1].title().replace("scene","")
	item=item.replace("shape","")
	# if(len(item)>10):
		# print(item+":"+str(len(item)))
	# 	return
	api_lookup = "http://lookup.dbpedia.org/api/search.asmx/KeywordSearch?QueryClass=&QueryString=" + item
	print("start:\t"+api_lookup)
	res = requests.get(api_lookup).content
	tmpStrx=res.decode("ascii").replace("\n","")
	matchObjx = re.match(reStr,tmpStrx,re.I)
	# print(len(tmpStrx))
	if len(tmpStrx)>214:
		print("dugenkui")
		# print(animLine.split(";")[0]+":\t"+matchObjx.group()[5:matchObjx.group().rindex("</URI>")])
	else:
		print("can't find for item:\t"+item)


reStr="<URI>.*</URI>"

remainderItem = OntologyMatching.get_item("data/clz2entityAnim")
listLockForLookUp=threading.Lock()

remainderx=[]
for line in remainderItem:
	ele=line.split(";")[1]
	if len(ele)<=10:
		remainderx.append(line)
	else:
		print("abandon:\t"+ele)

threadList=[]
while len(remainderItem)!=0:
	threadx=LookUpThread(remainderx)
	threadList.append(threadx)
	threadx.start()
	time.sleep(0.1)

for t in threadList:
	t.join()

