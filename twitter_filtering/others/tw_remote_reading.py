__author__ = "Fengming Liu"
__status__ = "prototype"

import paramiko
import subprocess

day = 16
hour = 18
minute = 29
filename = "{0}/{1}/{2}.json".format(str(day).zfill(2), str(hour).zfill(2), str(minute).zfill(2))

# get remote file
remote_dir = "/vol/project/2019/530/g1953004/"
ssh_client = paramiko.SSHClient()
ssh_client.load_system_host_keys()
ssh_client.connect("shell2.doc.ic.ac.uk", username="fl719", password="22htliIc!")
ftp = ssh_client.open_sftp()
file = ftp.get(remote_dir + filename, filename)
ftp.close()

