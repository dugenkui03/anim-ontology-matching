import time


print(time.time())
with open("E:\TDB原始数据\DBpedia数据\instance_types_en\instance_types_en.nt") as triple_file:
	triple_content=triple_file.readlines()
	for line in triple_content:
		print(line)
print(time.time())
