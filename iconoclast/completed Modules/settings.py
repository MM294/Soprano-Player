import os
import cPickle as pickle

class IconoSettings:
	def __init__(self, filelocation):
		self.path = filelocation

	def write_settings(self, data):
		settings = []
		for setting in data:
			settings.append(setting)
		pickle.dump(settings, open(self.path, "wb"))

	def get_settings(self):
		if os.path.exists(self.path):
			settings = pickle.load( open(self.path, "rb" ) )
		else:
			settings = ['full', 900, 550, 2, False, False]
		return settings

#i = IconoSettings('/home/mike/Desktop/settings.icono')
#i.write_settings(['full', '1200','750' ,'3'])
#print i.get_settings()


