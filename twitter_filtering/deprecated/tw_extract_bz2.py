__author__ = "Fengming Liu"
__status__ = "prototype"

import tarfile
import subprocess

day = 16
hour = 19
minute = 31

tw_json_bz2_filename = "./{0}/*/*.json.bz2".format(str(day))
# .zfill(2),str(hour).zfill(2),str(minute).zfill(2))
subprocess.run("bunzip2 -k " + tw_json_bz2_filename, shell=True)
subprocess.run("rm " + tw_json_bz2_filename, shell=True)