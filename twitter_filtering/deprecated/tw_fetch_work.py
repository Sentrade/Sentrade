__author__ = "Fengming Liu"
__status__ = "prototype"

import paramiko
import subprocess
import time
import re
import json
import os

year = 2019
month = 9
day = 16

# establish the connection
remote_dir = "/vol/project/2019/530/g1953004/"
ssh_client = paramiko.SSHClient()
ssh_client.load_system_host_keys()
ssh_client.connect("shell2.doc.ic.ac.uk", username="fl719", password="22htliIc!")
ftp = ssh_client.open_sftp()

for hour in range(0, 24):
	for minute in range(0, 59):
		# start time
		time_log = open("./keyword_search_time.log", 'a')
		start_tick = time.time()

		# try to downlad the remote file
		filename = "{0}/{1}/{2}.json".format(str(day).zfill(2), str(hour).zfill(2), str(minute).zfill(2))
		print("Fetching {0}...".format(filename))
		try:
			file = ftp.get(remote_dir + filename, filename)
		except FileNotFoundError:
			print(filename, " doesn't exist")

		# search for the keyword
		keyword_list = ["netflix", "amazon", "apple", "microsoft", "google", "tesla", "facebook"]
		date = "{0}-{1}-{2}".format(year, str(month).zfill(2), str(day).zfill(2))
		local_dir = "./subjecet_tw/raw/"
		if not os.path.exists(local_dir):
			os.makedirs(local_dir)

		for keyword in keyword_list:
			print("Searching for the keyword", keyword)
			tw_text_file_keyword = open(local_dir + "{0}_{1}.json".format(keyword, date), 'a')
			
			# load the data into the memory
			with open(filename, 'r') as f:
				data = [json.loads(line) for line in f]

			# write the selected items into a new json file
			for item in data:
				keys = item.keys()
				if "text" in keys and "lang" in keys and item["lang"] == "en":
					if re.search(re.compile(keyword), item["text"].lower()): # search based on the lower case
						json.dump(item, tw_text_file_keyword)
						tw_text_file_keyword.write('\n')
			tw_text_file_keyword.close()

		# remove the fetched file at the local
		subprocess.run("rm {0}".format(filename), shell=True)

		# end time
		end_tick = time.time()
		time_log.write("{0:15s}	{1:.3f}\n".format(filename, end_tick - start_tick))
		time_log.close()

ftp.close()