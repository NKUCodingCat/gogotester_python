from gevent import monkey
monkey.patch_os()
monkey.patch_socket()
monkey.patch_ssl()
import time
timelimit = 1.5
loop = 3
from gevent import socket
def Socket_Test(IP, Port = 443):
	STA = time.time()
	#==============
	#print "Start", IP
	try:
		for i in range(loop):
			s = socket.socket()
			s.settimeout(timelimit)
			s.connect((IP, Port))
			s.close()
		cost = time.time()-STA			
		return True ,IP ,	cost/loop				
	except socket.error:
		s.close()
		return False, IP , 65536
	#finally:
		#print "End", IP
if __name__ == "__main__":
	print Socket_Test("64.233.188.85")
	print Socket_Test("64.233.188.77")
	print Socket_Test("127.0.0.1")
	
	