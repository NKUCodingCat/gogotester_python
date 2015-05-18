import re, os, numpy
root = os.path.split(os.path.realpath(__file__))[0]+"/"
IPPool = []
InitFlag = False
def ipList(Str):
	S = re.split("\.", Str)
	if len(S) != 4:
		raise ValueError, "It Should be an ip-like String But we got \"%s\""%Str
	res = []
	for i in S:
		try:
			ran = int(i)
			if ran>=0 and ran<=255:
				res.append([ran,])
			else:
				raise ValueError, "It Should be an ip-like String But we got \"%s\""%Str
		except:
			ran = re.split("-", i)
			if len(ran) != 2:
				raise ValueError, "It Should be an ip-like String But we got \"%s\""%Str
			for j in ran:
				try:
					j = int(j)
				except:	
					raise ValueError, "It Should be an ip-like String But we got \"%s\""%Str
				if not (j>=0 and j<=255):
					raise ValueError, "It Should be an ip-like String But we got \"%s\""%Str
			if int(ran[0])>int(ran[1]):
				raise ValueError, "It Should be an ip-like String But we got \"%s\""%Str
			res.append(range(int(ran[0]), int(ran[1])+1 ))
	return res
def ListAll(Array, Src):
	try:
		Next = Src[0]
	except:
		return Array	
	New = []
	for NextNum in Next:
		for i in Array:
			New.extend([i+[NextNum, ]])
	if Src[1:]:
		return ListAll(New, Src[1:])
	else:
		return New
def GGCIPS(File = (root+"ggc.txt")):
	try:
		F = open(File)
	except:
		raise IOError, "%s is not exist"%File
	IPS =  re.split("\s+",F.read())
	RES = []
	for IPD in IPS:
		RES.extend(ListAll([[]], ipList(IPD)))
	return RES
def GetGGCIP(File = (root+"ggc.txt")):
	if InitFlag:
		pass
	else:
		IPPool = GGCIPS(File) 
	return [("%s.%s.%s.%s")%tuple(i) for i in IPPool]