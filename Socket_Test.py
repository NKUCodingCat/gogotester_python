from gevent import monkey
from gevent import socket
monkey.patch_os()
monkey.patch_socket()
monkey.patch_ssl()
import time
import gogo_cfg

import IPy

cfg = gogo_cfg.gogo_cfg()
timelimit = float(cfg.get("Socket", "timeout"))
loop = float(cfg.get("Socket", "loop"))


"""
IPV6 Complete
"""


def BuildSocket(ip):
	if IPy.IP(ip).version() == 4:
		s = socket.socket()  
	elif IPy.IP(ip).version() == 6:
		s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM, 0)  
	else:
		print "There is an invalid string in SSL_Test Func:",ip
		raise socket.error
	s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
	return s
def Socket_Test(IP, Port = 443):
	STA = time.time()
	#==============
	#print "Start", IP
	try:
		for i in range(int(loop)):
			s = BuildSocket(IP)
			s.settimeout(timelimit)
			s.connect((IP, Port))
			s.close()
		cost = time.time()-STA			
		return True ,IP ,	cost/loop				
	except socket.error:
		#raise
		s.close()
		return False, IP , 65536
	#finally:
		#print "End", IP
if __name__ == "__main__":
	print Socket_Test("2404:6800:4008:c03::8b")
	print Socket_Test("61.135.169.121")
	print Socket_Test("127.0.0.1")
	
	