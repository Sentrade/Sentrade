import tarfile
import subprocess
day_tar = tarfile.open("./twitter_stream_2019_09_16.tar", 'r')

for mem in day_tar.getmembers():
	if mem.isfile():
		day_tar.extract(mem)
		break

year = 2019
month = 9
day = 16
hour = 19
minute = 31

tw_json_bz2_filename = "./{0}/{1}/{2}.json.bz2".format(str(day).zfill(2),str(hour).zfill(2),str(minute).zfill(2))
subprocess.run("bunzip2 -k " + tw_json_bz2_filename, shell=True)