import requests

api ='http://dbpedia.org/page/'

count=0;
file_anim=open('anim.txt')
for line_anim in file_anim:
	term=line_anim.split(";")[2].strip("\n")
	print(term)
	resp=requests.get("https://www.baidu.com/")
	if(resp.status_code==200):
		print("success")
		count+=1

print(count)
file_anim.close()