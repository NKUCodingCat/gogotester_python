import os, json, time

def HTMLGEN(Json, File):
	Array = json.loads(Json)
	Array = sorted(Array, key=lambda x:x[0][-1])
	File.write("Updated at %s\n"%time.ctime())
	File.write("Copy the last line and paste in proxy.ini of goagent\n")
	File.write("%15s  %5s   %s\n"%("IP", "Delay", "SSL_cert"))
	for i in Array:
		File.write( "%15s   %04d   %s\n"%(i[0][1], i[0][2]*1000, i[1]["cname"]))
	File.write("\n"+"|".join([str(i[0][1]) for i in Array]))
	return File

if __name__ == "__main__":
	import RootPath
	root = RootPath.RootPath()
	HTMLGEN(open(root+"ip_ava.txt").read(), open(root+"ip.txt", "w"))