from gevent import monkey
monkey.patch_os()
monkey.patch_socket()
monkey.patch_ssl()

import ggc_ip, socket, time, os, json, random
from multiprocessing.dummy import Pool as ThreadPool 
import SSL_Test2
import Socket_Test
import HTMLGEN
import gogo_cfg
cfg = gogo_cfg.gogo_cfg()
sock_thread_num = float(cfg.get("TPool", "sock_thread_num"))
ssl_thread_num = float(cfg.get("TPool", "ssl_thread_num"))
ip_limit = float(cfg.get("Num","Limit"))
import gevent
from gevent import coros
Lock = coros.Semaphore()

root = os.path.split(os.path.realpath(__file__))[0]+"/"
Total = 0
Tested = 0
Succ = 0
ippool = ggc_ip.GetGGCIP(root+"ggc.txt")

Wait_for_SSL = []
Succ = []
Flag = False
InProcess = []
isEnd = False
Stop_the_World = False



def Socket_TestNext(ippool):
	global Flag, Wait_for_SSL, Succ, InProcess, isEnd 
	Lock.acquire()
	InProcess.append(1)
	Lock.release()
	while not isEnd:
		try:
			Lock.acquire()
			ip = ippool.pop(random.randrange(len(ippool)))
			Lock.release()
			if len(ippool)%1000 == 0:
				print len(Succ),"/",len(ippool), "/",len(Wait_for_SSL),"/",len(InProcess)
				print time.ctime(time.time())
			#print time.time()
			Soc = Socket_Test.Socket_Test(ip)
			if Soc[0] == True:
				Lock.acquire()
				Wait_for_SSL.append(Soc)
				Lock.release()
			gevent.sleep()
		except KeyboardInterrupt:
			isEnd = True
			return 0
		except (ValueError , IndexError):
			Lock.release()
			Flag = True
			Lock.acquire()
			InProcess.pop()
			Lock.release()
			return 0
	Lock.acquire()
	InProcess.pop()
	Lock.release()
	return 0
def SSL_TestNext():
	global Flag, Wait_for_SSL, Succ, InProcess
	while True:
		try:
			Lock.acquire()
			Data = Wait_for_SSL.pop()
			Lock.release()
		except IndexError:
			Lock.release()
			if Flag and len(InProcess)==0:
				return 
		except KeyboardInterrupt:
			isEnd = True
			return 0
		else:
			print "Test", Data[1]
			SSLRes = SSL_Test2.SSL_Test(Data[1])
			print "Tested %s"%Data[1], time.time()
			if SSLRes:
				print json.dumps(SSLRes)
				log.write(json.dumps(SSLRes)+"\n")
				Lock.acquire()
				Succ.append((Data , SSLRes))
				Lock.release()
		gevent.sleep()
	return 

def LimitCheck(limit, ippool):
	if limit <= 0:
		return
	else:
		global Flag, Wait_for_SSL, Succ, InProcess, isEnd 
		while((len(Succ) < limit) and (len(InProcess)!=0)):
			gevent.sleep()
		Wait_for_SSL = []
		ippool = []
		isEnd = True
		Flag = True
		#print "Limit UP"
		return
	

jobs = [gevent.spawn(Socket_TestNext, ippool) for i in range(int(sock_thread_num))]  
jobs.extend([gevent.spawn(SSL_TestNext ) for i in range(int(ssl_thread_num))])
jobs.extend([gevent.spawn(LimitCheck, ip_limit, ippool),])

#print jobs
try:
	log = open(root+"log.log", "w")
	res_out = open(root+"ip_ava.txt", "w")
	gevent.joinall(jobs)
	res_out.write(json.dumps(Succ))
	HTMLGEN.HTMLGEN(json.dumps(Succ), open(root+"ip.txt", "w")).close()

	
except:
	pass
finally:
	log.close()
	res_out.close()