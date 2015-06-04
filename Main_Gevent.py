#coding=utf-8
#ippool will like [ [ipv4 ips] , [v6 ips] ]
import gevent
from gevent import coros
from gevent import monkey
monkey.patch_os()
monkey.patch_socket()
monkey.patch_ssl()

import socket, time, os, json, random, itertools
import ggc_ip
import IPy
import SSL_Test2
import Socket_Test
import HTMLGEN
import gogo_cfg

cfg = gogo_cfg.gogo_cfg()
sock_thread_num = float(cfg.get("TPool", "sock_thread_num"))
ssl_thread_num = float(cfg.get("TPool", "ssl_thread_num"))
v4_limit = float(cfg.get("Num","Limit"))
v6_limit = float(cfg.get("Num","Limit_v6"))
Lock = coros.Semaphore()
root = os.path.split(os.path.realpath(__file__))[0]+"/"
ippool = ggc_ip.GetGGCIP(root+"ggc.txt")
ippool = [list(itertools.chain.from_iterable(j)) for j in map(lambda x:[list(i) for i in x], ippool)]
Last_time = time.time()

#ippool[0] is v4 pool, ippool[1] is v6 pool


STAT = {
	"v4":{
		"Total":len(ippool[0]),
		"Tested":0,
		"Succ":0
	},
	"v6":{
		"Total":len(ippool[1]),
		"Tested":0,
		"Succ":0
	}
}
STOP ={
	"v4":False,
	"v6":False
}

Wait_for_SSL = []
Succ = []

def STATOut():
	global STAT, STOP
	for i in STAT.keys():
		for j in STAT[i].keys():
			print "%s_%s: %s /"%(i,j,STAT[i][j]) , 
		print "%s_STOP: %s"%(i,STOP[i])
	print time.ctime()
	

def LimitCheck():
	global ippool, STAT, v4_limit, v6_limit, Lock, STOP
	if v4_limit <= 0:
		ippool[0] = []
		STOP["v4"] = True
	if v6_limit <= 0:
		ippool[1] = []
		STOP["v6"] = True
	print "Start Check"
	while (len(ippool[0]) > 0 or len(ippool[1]) > 0):
		Lock.acquire()
		if STAT["v4"]["Succ"] >=v4_limit:
			ippool[0] = []
			STOP["v4"] = True
		if STAT["v6"]["Succ"] >=v6_limit:
			ippool[1] = []
			STOP["v6"] = True
		Lock.release()
		gevent.sleep()
	if len(ippool[0]) <= 0:
		STOP["v4"] = True
	if len(ippool[1]) <= 0:
		STOP["v6"] = True
	print "Limit UP"
	print STOP
	return 
	

def Socket_TestNext(ippool, isv4 = True):
	global Wait_for_SSL, Succ, STOP, Last_time
	STA = True and isv4
	#print "In"
	while True:
		gevent.sleep()
		if (time.time()-Last_time) > 5 :
			STATOut()
			Last_time = time.time()
		#STATOut()
		if(STOP["v4"] and STOP["v6"]):
			return
		try:
			Lock.acquire()
			if isv4:
				ip = ippool[0].pop(random.randrange(len(ippool[0])))
				STAT["v4"]["Tested"] += 1
			else:
				ip = ippool[1].pop(random.randrange(len(ippool[1])))
				STAT["v6"]["Tested"] += 1
			Lock.release()
			gevent.sleep()
			Soc = Socket_Test.Socket_Test(str(ip))
			if Soc[0] == True:
				Lock.acquire()
				Wait_for_SSL.append(Soc)
				Lock.release()
			gevent.sleep()
		except KeyboardInterrupt:
			Lock.release()
			STOP["v4"] = True
			STOP["v6"] = True
			return 
		except (ValueError , IndexError):	
			if STA == True: #原来是v4
				if isv4 == True: #没变
					isv4 = False
					Lock.release()
					continue
				else:
					STOP["v4"] = True
					STOP["v6"] = True
					Lock.release()
					return
			else:
				if isv4 == False:
					isv4 = True
					Lock.release()
					continue
				else:
					STOP["v4"] = True
					STOP["v6"] = True
					Lock.release()
					return
		except:
			raise


def SSL_TestNext():
	global Wait_for_SSL, Succ, STAT, Lock, STOP, log
	#return
	while True:
		gevent.sleep()
		try:
			Lock.acquire()
			Data = Wait_for_SSL.pop()
			Lock.release()
		except IndexError:
			Lock.release()
			if(STOP["v4"] and STOP["v6"]):
				return
		except KeyboardInterrupt:
			Lock.release()
			STOP["v4"] = True
			STOP["v6"] = True
			return 0
		else:
			gevent.sleep()
			print "Test", Data[1]
			SSLRes = SSL_Test2.SSL_Test(Data[1])
			print "Tested %s"%Data[1], time.time()
			if SSLRes:
				print json.dumps(SSLRes)
				log.write(json.dumps(SSLRes)+"\n")
				Lock.acquire()
				Succ.append((Data , SSLRes))
				if IPy.IP(Data[1]).version()==4:
					STAT["v4"]["Succ"] += 1
				else:
					STAT["v6"]["Succ"] += 1
				Lock.release()
	return
try:
	log = open(root+"log.log", "w")
	jobs = [gevent.spawn(LimitCheck),]+[gevent.spawn(Socket_TestNext,ippool) for i in range(int(sock_thread_num)/2)]+[gevent.spawn(Socket_TestNext,ippool, False) for i in range(int(sock_thread_num)-int(sock_thread_num)/2)] +[gevent.spawn(SSL_TestNext) for i in range(int(ssl_thread_num))]
	gevent.joinall(jobs)

finally:
	HTMLGEN.HTMLGEN(json.dumps([i for i in Succ if IPy.IP(i[0][1]).version() == 4]), open(root+"ip_4.txt", "w")).close()
	HTMLGEN.HTMLGEN(json.dumps([i for i in Succ if IPy.IP(i[0][1]).version() == 6]), open(root+"ip_6.txt", "w")).close()
	log.close()