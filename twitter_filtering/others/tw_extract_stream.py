__author__ = "Fengming Liu"
__status__ = "prototype"

import tarfile
import subprocess

year = 2019
month = 9
day = 16
time = "{0}_{1}_{2}".format(year, str(month).zfill(2), str(day).zfill(2))
day_tar = tarfile.open("../twitter_stream_{0}.tar".format(time), 'r')
# print(day_tar.getmembers())
for mem in day_tar.getmembers():
	if mem.isfile():
		day_tar.extract(mem)
		# print(mem.name)


hour = 19
minute = 31

# tw_json_bz2_filename = "./{0}/{1}/{2}.json.bz2".format(str(day).zfill(2),str(hour).zfill(2),str(minute).zfill(2))
# subprocess.run("bunzip2 -k " + tw_json_bz2_filename, shell=True)