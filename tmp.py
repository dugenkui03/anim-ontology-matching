v = set();

filex = open('EntityClass')

for line in filex:
	v.add(line)

print(len(v))

for ele in v:
	print(ele[21:-2])
