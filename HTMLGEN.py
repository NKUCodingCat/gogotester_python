import os, json

def HTMLGEN(Json, File):
	Array = json.loads(Json)
	Array = sorted(Array, key=lambda x:x[0][-1])
	File.write("%15s  %5s   %s\n"%("IP", "Delay", "SSL_cert"))
	for i in Array:
		File.write( "%15s   %04d   %s\n"%(i[0][1], i[0][2]*1000, i[1]["cname"]))
	return File





if __name__ == "__main__":
	root = os.path.split(os.path.realpath(__file__))[0]+"/"
	HTMLGEN(open(root+"ip_ava.txt").read(), open(root+"ip.txt", "w"))