import re


# 提取出 动画知识库中属性uri的命名后缀
def test():
	with open("data/prop_data/propDataPrepro","w") as empty_file:
	    with open("data/prop_data/propData") as entity_file:
	        entity_file_content=entity_file.readlines()
	        for line in entity_file_content:
	            try:
	                lindex=line.index("#")+1
	                rindex=len(line)-2
	                empty_file.write(line.strip()+";"+line[lindex:rindex].strip()+"\n")
	            except:
	                pass





