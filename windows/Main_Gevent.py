#coding=utf-8
#ippool will like [ [ipv4 ips] , [v6 ips] ]

Ver = "0.7.0 alpha"

import sys
import os
import glob

reload(sys).setdefaultencoding('UTF-8')
sys.dont_write_bytecode = True
sys.path += glob.glob('%s/*.egg' % os.path.dirname(os.path.abspath(__file__)))

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
import RootPath

cfg = gogo_cfg.gogo_cfg()
sock_thread_num = float(cfg.get("TPool", "sock_thread_num"))
ssl_thread_num = float(cfg.get("TPool", "ssl_thread_num"))
v4_limit = float(cfg.get("Num","Limit"))
v6_limit = float(cfg.get("Num","Limit_v6"))
Lock = coros.Semaphore()
root = RootPath.RootPath()
ippool = ggc_ip.GGC_IP(root+"ggc.txt").IPPool
Last_time = time.time()

#ippool[0] is v4 pool, ippool[1] is v6 pool

import logging  
logging.basicConfig(level=logging.DEBUG,  format='%(levelname)s - [%(asctime)s] %(message)s',  datefmt='%a, %d %b %Y %H:%M:%S' )  


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


import IPy
def IntToIPString(Int):
	return str(IPy.IP(Int))

def STATOut():
	global STAT, STOP
	
	for i in STAT.keys():
		Str = "IP pool Status: "
		for j in STAT[i].keys():
			Str +=  "%s_%s: %s, "%(i,j,STAT[i][j]) 
		logging.info(Str[:-2])
	
	import gc  
	gc.collect()
	

def LimitCheck():
	global ippool, STAT, v4_limit, v6_limit, Lock, STOP
	if v4_limit <= 0:
		ippool[0] = []
		STAT["v4"]["Total"] = 0
		STOP["v4"] = True
	if v6_limit <= 0:
		ippool[1] = []
		STAT["v6"]["Total"] = 0
		STOP["v6"] = True
	logging.info("Watch Dog Start Working")
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
	logging.info("Socket Test Work Done")
	if len(Wait_for_SSL)>0:
		logging.info("Still have %s IPs wait to be test by SSL"%len(Wait_for_SSL))
	#print STOP
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
				ip = IntToIPString(ippool[0].pop(random.randrange(len(ippool[0]))))
				STAT["v4"]["Tested"] += 1
			else:
				ip = IntToIPString(ippool[1].pop(random.randrange(len(ippool[1]))))
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
			logging.error("KeyboardInterrupt")  
			STOP["v4"] = True
			STOP["v6"] = True
			return 
		except (ValueError , IndexError):
			#logging.info("Thread Switced")  
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
			logging.error("KeyboardInterrupt")  
			Lock.release()
			STOP["v4"] = True
			STOP["v6"] = True
			return 0
		else:
			gevent.sleep()
			#logging.info("SSL Test %s"%Data[1])
			SSLRes = SSL_Test2.SSL_Test(Data[1])
			if SSLRes:
				#print json.dumps(SSLRes)
				logging.info("%s is avaliable, cert: %s, delay: %.4f "%(Data[1],SSLRes["cname"],Data[2]))
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
	print "\n\n\nGoGo Tester Py - Ver %s\n\nDevloped by NKUCodingcat <admin@nkucodingcat.com>\n\n"%Ver
	log = open(root+"log.log", "w")
	jobs = [gevent.spawn(LimitCheck),]+[gevent.spawn(Socket_TestNext,ippool) for i in range(int(sock_thread_num)/2)]+[gevent.spawn(Socket_TestNext,ippool, False) for i in range(int(sock_thread_num)-int(sock_thread_num)/2)] +[gevent.spawn(SSL_TestNext) for i in range(int(ssl_thread_num))]
	gevent.joinall(jobs)
	

finally:
	print "\n\nSearch Complete. The result will be saved at %s/res"%root
	if not os.path.exists(root+"res"):
		os.mkdir(root+"res")
	HTMLGEN.HTMLGEN(json.dumps([i for i in Succ if IPy.IP(i[0][1]).version() == 4]), open(root+"res/ip_4.txt", "w")).close()
	HTMLGEN.HTMLGEN(json.dumps([i for i in Succ if IPy.IP(i[0][1]).version() == 6]), open(root+"res/ip_6.txt", "w")).close()
	log.close()
	print "\n\n"
