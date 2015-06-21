import  socket, Socket_Test, IPy
def GetAdd(Name, Type):
	try:
		J = socket.getaddrinfo(Name, 80, 0, 0, socket.IPPROTO_TCP)
		K = [i for i in J if IPy.IP(i[4][0]).version()==Type]
		if len(K) == 0:
			raise socket.error, "No ipv%s Addr found in this find"%Type
	except socket.error:
		raise
	except:
		raise
	else:
		return K[0]
def Conn(ip, port=80):
	return Socket_Test.Socket_Test(ip, port)[0]
def Con_Test(v4 = "www.baidu.com", v6 = "ipv6.baidu.com"):
	RES = {}
	#v4
	try:
		RES["v4"] = Socket_Test.Socket_Test(GetAdd(v4, 4)[4][0], 80)[0]
	except:
		RES["v4"] = False
	#v6
	try:
		RES["v6"] = Socket_Test.Socket_Test(GetAdd(v6, 6)[4][0],80)[0]
	except:
		RES["v6"] = False
	return RES
if __name__ == "__main__":
	print Con_Test()