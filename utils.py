v = set();

filex = open('EntityInstance.txt')

for line in filex:
	v.add(line)

print(len(v))

for ele in v:
	print(ele[21:-2])
