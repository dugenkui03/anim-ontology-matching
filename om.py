file_anim = open("anim");
file_dbpedia = open("dbpedia");


# 相等的15个
count = 0;
for line_anim in file_anim:
	termx = line_anim.split(";")[3].strip('\n')
	if termx == '':
		continue;
	for line_dbpedia in file_dbpedia:
		termy = line_dbpedia.split(";")[3].strip('\n')
		# if termy == "":
		# 	print(termy)
		# 	break;
		if (termx == termy):
			print("equal:"+termx);
			count += 1;
			break;
		# if termx.find(termy) >= 0:
		# 	print("contain:"+termx.strip('\n')+"\t"+termy+"end")
		# 	count += 1;
		# 	break;
		# if termy.find(termx) >= 0:
		# 	print("contain:"+termx.strip('\n')+"\t"+termy+"\tend")
		# 	count += 1;
		# 	break;
	file_dbpedia.seek(0);

print(count);
file_anim.close();
file_dbpedia.close();



#近义词：调用https://www.thesaurus.com/browse/XXX
file_anim = open("anim");
file_dbpedia = open("dbpedia");

api_uri="https://www.thesaurus.com/browse/human";

