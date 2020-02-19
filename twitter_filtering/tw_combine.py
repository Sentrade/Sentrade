__author__ = "Fengming Liu"
__status__ = "prototype"

import json
import os

tw_folder = "./subject_tw/processed/"
tw_combined_json_file = open("./tw_all_companies.json", 'w')

total_data = []
for filename in os.listdir(tw_folder):
	[keyword, data, others] = filename.split('_')
	# load the json file into the memory
	with open(tw_folder + filename, 'r') as f:
		data = [json.loads(line) for line in f]

	# insert the company name
	for item in data:
		item["company"] = keyword

	# join the list
	total_data = total_data + data
	del data
		
	
	
json.dump(total_data, tw_combined_json_file)
tw_combined_json_file.close()