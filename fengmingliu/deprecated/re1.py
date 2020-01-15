import re

f = open("./htmlcode.txt", 'r')
text = f.read()
pattern = re.compile(r'[Dd][Aa][Tt][Ee].{0,20}:.{0,20}\d{4}-\d{2}-\d{2}')
for item in re.findall(pattern, text):
	print(item)

f.close()