__author__ = "Fengming Liu"
__status__ = "prototype"

import calendar
import os
import pymongo
import sys
import tarfile
import time
from tw_funcs import create_dir, process_bz2_db, download_archive

# essential variables
year = sys.argv[1]
month = sys.argv[2]
day = sys.argv[3]
time_log_dir = create_dir("./time_log/")
# db_client = pymongo.MongoClient("mongodb://admin:sentrade@45.76.133.175", 27017)
db_client = pymongo.MongoClient("mongodb://admin:sentrade@127.0.0.1", 27017)
# db = db_client["temp"]
db = db_client["twitter_data"]
keyword_list = ["netflix", "amazon", "apple", "microsoft", "google", "tesla", "facebook"]
month_abbr_to_num = {name: num for num, name in enumerate(calendar.month_abbr) if num}

date = "{0}_{1}_{2}".format(year, str(month).zfill(2), str(day).zfill(2))

# downlaod archive zip
date_tar_filename = "./twitter_stream_{0}.tar".format(date)
if not os.path.exists(date_tar_filename):
	if download_archive(year, str(month).zfill(2), str(day).zfill(2)) == False:
		subprocess.run("rm " + date_tar_filename, shell=True)
		exit(0)

# extract bz2 files
date_tar = tarfile.open(date_tar_filename, 'r')
for mem in date_tar.getmembers():
	# start time
	time_log = open(time_log_dir + "{0}.log".format(date), 'a')
	start_tick = time.time()

	# extract the member out
	if mem.isfile():
		date_tar.extract(mem)
	else:
		continue

	# unzip the bz2 file to json file
	tw_json_bz2_filename = mem.name
	tw_json_filename = tw_json_bz2_filename.split('.')[0] + ".json"
	process_bz2_db(tw_json_bz2_filename, keyword_list, db, year, month, month_abbr_to_num)

	# end time
	end_tick = time.time()
	time_log.write("{0:15s}	{1:.3f}\n".format(tw_json_filename, end_tick - start_tick))
	time_log.close()
	date_tar.close()