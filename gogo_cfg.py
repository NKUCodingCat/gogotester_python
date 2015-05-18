import sys, os
import ConfigParser
root = os.path.split(os.path.realpath(__file__))[0]+"/"
class gogo_cfg:
	def __init__(self, config_file_path=(root+"config.ini")):
		self.cf = ConfigParser.ConfigParser()
		self.cf.read(config_file_path)
	def get(self, field, key):
		try:
			return self.cf.get(field, key)
		except:
			return None
	def showall(self):
		for i in self.cf.sections():
			print i+":"
			for j in self.cf.options(i):
				print "    "+j+" =",self.cf.get(i,j)
if __name__=="__main__":
	cfg = gogo_cfg()
	cfg.showall()