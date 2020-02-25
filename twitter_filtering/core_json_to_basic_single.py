__author__ = "Fengming Liu"
__status__ = "prototype"

import tarfile
import subprocess
import time
import os
import json
import re
import sys
import tw_funcs

year = 2019
month = 9
day = sys.argv[1].zfill(2)
hour = sys.argv[2].zfill(2)
minute = sys.argv[3].zfill(2)
local_dir = sys.argv[4]

# start time
# time_log = open("./keyword_search_time.log", 'a')
# start_tick = time.time()

# search keywords in the file
tw_json_filename = "./{0}/{1}/{2}.json".format(day, hour, minute)
print(tw_json_filename)
keyword_list = ["netflix", "amazon", "apple", "microsoft", "google", "tesla", "facebook"]
for keyword in keyword_list:
	tw_funcs.search_keyword(keyword, tw_json_filename, local_dir, "{0}-{1}-{2}.json".format(year, str(month).zfill(2), day))
# subprocess.run("rm " + tw_json_filename, shell=True)

# end time
# end_tick = time.time()
# time_log.write("{0:15s}	{1:.3f}\n".format(tw_json_filename, end_tick - start_tick))
# time_log.close()