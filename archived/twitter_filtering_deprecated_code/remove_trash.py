__author__ = "Fengming Liu"
__status__ = "prototype"

import calendar
import os
import pymongo
import sys
import tarfile
import time
from tw_funcs import create_dir, process_bz2_db, download_archive
import subprocess

# essential variables
year = 2018
month = sys.argv[1]
day_start = int(sys.argv[2])
day_end = int(sys.argv[3])
time_log_dir = create_dir("./time_log/")
db_client = pymongo.MongoClient(os.environ["CLIENT_ADDR"])
# db_client = pymongo.MongoClient(os.environ["CLIENT_ADDR"])
# db = db_client["temp"]
db = db_client["twitter_data"]
keyword_list = ["netflix", "amazon", "apple", "microsoft", "google", "tesla", "facebook", "uber"]
month_abbr_to_num = {name: num for num, name in enumerate(calendar.month_abbr) if num}

for keyword in keyword_list:
	db[keyword]