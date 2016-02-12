import  urllib2

def Con_Test(v4 = "http://216.218.228.119/ip/?callback=?&testdomain=test-ipv6.com&testname=test_ipv4", v6 = "http://[2001:470:1:18::119]/ip/?callback=?&testdomain=test-ipv6.com&testname=test_ipv6"):
	RES = {}
	#v4
	try:
		RES["v4"] = True
		urllib2.urlopen(v4, timeout = 5)
	except:
		RES["v4"] = False
	#v6
	try:
		RES["v6"] = True
		urllib2.urlopen(v6, timeout = 5)
	except:
		RES["v6"] = False
	return RES
if __name__ == "__main__":
	print Con_Test()