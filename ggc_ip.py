import re, os,  itertools

import IPy

import Con_Test

IPPool = []
InitFlag = False
root = os.path.split(os.path.realpath(__file__))[0]+"/"

def v4_Tran(String):
	"""
	In V4 you can write ip range like:
		/ None 1.2.3.0
		/prefix 1.2.3.0/24
		/netmask 1.2.3.0/255.255.255.0
		-lastip 1.2.3.0-1.2.3.255
		-(I dont know how to express it ) 1.2.0-3.0-255
		
		But All of those should follow CIDR
	"""
	if re.findall(":",String):
		raise ValueError, "Its an v6"
	if re.findall("(\d+(-\d+)?\.){3}(\d+-\d+)", String):
		if len(re.split("\.", String) ) == 4:
			F = re.split("\.", String)
			G = []
			for i in F:
				if len(re.split("-",i))==2:
					G.append(re.split("-",i))
					break
				elif len(re.split("-",i))==1:
					G.append([i,])
				else:
					raise ValueError
			for j in range(4-len(G)):
				G.append(["0","255"])
			A = []
			B = []
			for k in G:
				if len(k ) == 1:
					A.append(k[0])
					B.append(k[0])
				else:
					A.append(k[0])
					B.append(k[1])
			#print ("%s."*3+"%s"+"-"+"%s."*3+"%s")%tuple(A+B)
			res =  IPy.IP(("%s."*3+"%s"+"-"+"%s."*3+"%s")%tuple(A+B))
		else:
			raise ValueError
	else:
		try:
			res = IPy.IP(String)
		except:
			raise
	return res	
				
	
def v6_Tran(String):
	"""
	Its just IPy.IP Copy
	"""
	return IPy.IP(String)

def GGCIPS(File):
	try:
		F = open(File)
	except:
		raise IOError, "%s is not exist"%File
	IPS =  re.split("[\r\n]+",F.read())
	V4s = []
	V6s = []
	for IPD in IPS:
		IPD = re.sub("\s+","", IPD)
		if len(IPD) == 0:
			continue
		if IPD[0] == "#":
			continue
		try:
			V4s.append(v4_Tran(IPD))
		except:
			
			try:
				V6s.append(v6_Tran(IPD))
			except:
				print(IPD) 
				raise
	#print V4s, V6s
	return [IPy.IPSet(V4s), IPy.IPSet(V6s)]
def GetGGCIP(File = (root+"ggc.txt")):
	global InitFlag, IPPool 
	if InitFlag:
		pass
	else:
		IPPool = GGCIPS(File) 
		C = Con_Test.Con_Test()
		if not C["v4"]:
			IPPool[0] = []
			print "IPv4 is not avalible"
		if not C["v6"]:
			IPPool[1] = []
			print "IPv6 is not avalible"
		IPPool = [list(itertools.chain.from_iterable(j)) for j in map(lambda x:[list(i) for i in x], IPPool)]
		InitFlag = True
	return IPPool[:]
if __name__ == "__main__":
	#print GetGGCIP(root + "ggc.txt")
	print len(GetGGCIP(root + "ggc.txt")[0])
	print len(GetGGCIP(root + "ggc.txt")[1])

