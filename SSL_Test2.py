#coding=utf-8
from gevent import monkey
monkey.patch_os()
monkey.patch_socket()
monkey.patch_ssl() 
import socket
import ssl  
import platform
import random
import re
import sys, traceback
import gogo_cfg
import Socket_Test
import IPy


"""
IPV6 Complete
"""

"""
Hack for Py 2.7.9+
"""
import SSLHack
SSLHack.SSLHACK()

cfg = gogo_cfg.gogo_cfg()
socket_timeout = float(cfg.get("SSL", "socket_timeout"))
ssl_timeout = float(cfg.get("SSL", "ssl_timeout"))

import RootPath
root = RootPath.RootPath()
RxResult = re.compile("""^(HTTP/... (\d+).*|Server:\s*(\w.*))$""", re.IGNORECASE|re.MULTILINE)

def Par_res(String):
	try:
		Arr = RxResult.findall(String)
		status = "NN"
		for i in Arr:
			if i[1] == "200":
				for j in Arr:
					if j[2] == "gws\r":
						status = "GA"
					elif j[2] == "Google Frontend\r":
						status = "A"
					else:
						pass
	except:
		return None
	if status == "NN":
		return None
	else:
		return status		
		

def SSL_Test(ip):
	"""
	if this ip is available as GAE ip, the func will return like: {"ip": ip, "cname": CName, "Status": status}
	if not , return None
	"""
	try:
		s = Socket_Test.BuildSocket(ip)
	except KeyboardInterrupt:
		raise
	except:
		#raise
		return None
	try:     #Gernel
		s.settimeout(socket_timeout)  
		try:
			c = ssl.wrap_socket(s, cert_reqs=ssl.CERT_REQUIRED, ca_certs=root+'cacert.pem', ciphers='ECDHE-RSA-AES128-SHA')   
			c.settimeout(ssl_timeout)  
			c.connect((ip, 443))
		except (socket.error, socket.timeout):
			return None
		except :
			print "Warning: Some Unexcepted Error Occured: %s While Testing %s\nTry Another way to Connect......\n"%(sys.exc_info()[0], ip)
			s = BuildSocket(ip)
			s.settimeout(socket_timeout)  
			c = ssl.wrap_socket(s, cert_reqs=ssl.CERT_REQUIRED, ca_certs=root+'cacert.pem')   
			c.settimeout(ssl_timeout)  
			c.connect((ip, 443))
		
			
		cert = c.getpeercert()  
		c.write("HEAD /search?q=g HTTP/1.1\r\nHost: www.google.com.hk\r\n\r\nGET /%s HTTP/1.1\r\nHost: azzvxgoagent%s.appspot.com\r\nConnection: close\r\n\r\n"%(platform.python_version() , random.randrange(7)))
		res = c.read(2048)
		Cer = [j for j in [i[0] for i in cert["subject"]] if j[0] == "commonName"][0][1]
		status =  Par_res(res)
	except KeyboardInterrupt:
		raise
	except:
		exc_type, exc_value, exc_traceback = sys.exc_info()
		print "\nWarning: Some Unexcepted Error Occured: %s\nIP: %s maybe avaliable but we can not Test it by SSL\n"%("".join(traceback.format_exception(exc_type, exc_value,exc_traceback)), ip)
		return None
	if status:
		return {"ip": ip, "cname": Cer, "Status": status}
	else:
		return None
if __name__ == "__main__":
	import ggc_ip, os
	import RootPath
	root = RootPath.RootPath()
	ippool = ggc_ip.GGC_IP(root+"ggc_test.txt").IPPool
	#print SSL_Test("2404:6800:4008:c03::8b")
	for i in ippool:
		for  j in i:
			print SSL_Test(str(IPy.IP(j)))
