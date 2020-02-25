__author__ = "Fengming Liu"
__status__ = "prototype"

import random

def alter_keyword(filename, keyword):
	# load the data into the memory
	with open(filename, 'r') as f:
		data = [json.loads(line) for line in f]

	# write the selected items into a new json file
	with open(filename, 'w') as f:
		for item in data:
			if "text" in item.keys() and re.search(keyword.lower(), item["text"].lower()):
					re.sub(keyword.lower(), keyword, item["text"])
			json.dump(item, f)
			f.write('\n')

# construct the local directory containing the result
org_dir = "./collection/basic_org/"
test_dir = "./collection/basic/"

keyword_list = ["netflix", "amazon", "apple", "microsoft", "google", "tesla", "facebook"]
for keyword in keyword_list:
	org_file = org_dir + keyword + "_2019-09-16.json"
	test_file = test_dir + keyword + "_2019-09-16.json"

	for i in range(len(keyword)):
		r = random.randint(0, 1)
		if r == 0:
			keyword = keyword[:i] + keyword[i].lower() + keyword[i+1:]
		else:
			keyword = keyword[:i] + keyword[i].upper() + keyword[i+1:]
	print(keyword)
	alter_keyword(test_file, keyword)


	# org_content = org_file.read().lower()
	# test_content = test_file.read().lower()
	# print(keyword, org_content == test_content)