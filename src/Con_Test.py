import  urllib2

def Con_Test(v4 = "www.baidu.com", v6 = "ipv6.he.net"):
	RES = {}
	#v4
	try:
		RES["v4"] = True
		urllib2.urlopen("https://%s"%v4, timeout = 5)
	except:
		RES["v4"] = False
	#v6
	try:
		RES["v6"] = True
		urllib2.urlopen("https://%s"%v6, timeout = 5)
	except:
		RES["v6"] = False
	return RES
if __name__ == "__main__":
	print Con_Test()