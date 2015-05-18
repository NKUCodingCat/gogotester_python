from gevent import monkey
monkey.patch_os()
monkey.patch_socket()
monkey.patch_ssl()

import ggc_ip, socket, time, os, json
from multiprocessing.dummy import Pool as ThreadPool 
import SSL_Test2
import Socket_Test
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
def Socket_TestNext(ippool):
	global Flag, Wait_for_SSL, Succ, InProcess, isEnd 
	Lock.acquire()
	InProcess.append(1)
	Lock.release()
	while not isEnd:
		try:
			Lock.acquire()
			ip = ippool.pop()
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
		except IndexError:
			Lock.release()
			Flag = True
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

		

jobs = [gevent.spawn(Socket_TestNext, ippool) for i in range(75)]  
jobs.extend([gevent.spawn(SSL_TestNext ) for i in range(60)])

#print jobs
try:
	log = open(root+"log.log", "w")
	res_out = open(root+"ip_ava.txt", "w")
	gevent.joinall(jobs)
	res_out.write(json.dumps(Succ))

	
except:
	pass
finally:
	log.close()
	res_out.close()
#print len(Succ),"/",len(ippool)


#print jobs