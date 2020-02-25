__author__ = "Fengming Liu"
__status__ = "prototype"

# construct the local directory containing the result
org_dir = "./collection/basic_org/"
test_dir = "./collection/basic/"

keyword_list = ["netflix", "amazon", "apple", "microsoft", "google", "tesla", "facebook"]
for keyword in keyword_list:
	org_file = open(org_dir + keyword + "_2019-09-16.json", 'r')
	org_content = org_file.read().lower()
	test_file = open(test_dir + keyword + "_2019-09-16.json", 'r')
	test_content = test_file.read().lower()
	
	print(keyword, org_content == test_content)
	org_file.close()
	test_file.close()