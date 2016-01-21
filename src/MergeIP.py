import IPy
import RootPath
import ggc_ip
import time

import RootPath
root = RootPath.RootPath()

FromFile = root+"/IP_in.txt"
ToFile = root+"/IP_out.txt"

RD = ggc_ip.GGC_IP(File = FromFile,ConnChk = False, IntIPPool = False).IPPool
with open(ToFile, "w") as fp:
	fp.write("#Generate Automatically at %s \n#include %s IPv4 Address and %s IPv6 Address\n\n"%(time.ctime(), len(RD[0]), len(RD[1])))
	fp.write("#=========v4=========\n\n")
	for i in RD[0]:
		fp.write(str(i)+"\n")
	fp.write("\n\n")
	fp.write("#=========v6=========\n\n")
	for i in RD[1]:
		fp.write(str(i)+"\n")

print "Mission Complete"
fp.close()