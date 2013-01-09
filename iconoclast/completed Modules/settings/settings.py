import os.path
try: import cPickle as pickle
except: import pickle

class IconoSettings:
	def __init__(self, filelocation):
		self.path = filelocation

	def write_settings(self, data):
		settings = []
		for setting in data:
			settings.append(setting)
		pickle.dump(settings, open(self.path, "wb"),2)

	def get_settings(self):
		if os.path.exists(self.path):
			settings = pickle.load( open(self.path, "rb" ) )
		else:
			settings = ['full', 900, 550, 2, False, False, True]
		return settings

class IconoPrefs(object):
	def __init__(self, filelocation):
		self.path = filelocation

	def add_radio(self, station):
		try: settings = pickle.load( open(self.path, "rb" ) )
		except: settings = {}
		settings[station[0]] = station[1]
		pickle.dump(settings, open(self.path, "wb"),2)

	def delete_radio(self, station):
		settings = pickle.load( open(self.path, "rb" ) )
		del settings[station[0]]
		pickle.dump(settings, open(self.path, "wb"),2)

	def get_radioStations(self):
		try: prefs = pickle.load( open(self.path, "rb" ) )
		except: prefs = {}
		return prefs

"""i = IconoSettings('/home/mike/.config/sopranoplayer/settings.icono')
i.write_settings(['full', '1200','750' ,'3'])
print(i.get_settings())"""


