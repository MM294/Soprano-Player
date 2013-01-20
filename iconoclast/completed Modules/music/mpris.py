import dbus
import dbus.service
import os.path
from time import time
from settings import sopranoGlobals
#props to raving rick @ http://theravingrick.blogspot.co.uk for his tutorial & code
class SoundMenuControls(dbus.service.Object):
	def __init__(self, desktop_name):
		self.desktop_name = desktop_name
		bus_name = dbus.service.BusName("""org.mpris.MediaPlayer2.%s""" % desktop_name, bus=dbus.SessionBus())
		dbus.service.Object.__init__(self, bus_name, "/org/mpris/MediaPlayer2")
		self.__playback_status = "Stopped"    

		self.set_metadata()
		self.eventtime = 0

	@property
	def DesktopEntry(self):
		return self.desktop_name

	@property
	def PlaybackStatus(self):
		return self.__playback_status

	@property
	def MetaData(self):
        	return self.__meta_data

	@dbus.service.method('org.mpris.MediaPlayer2')
	def Raise(self):
		localtime = time() # hack to workaround the fact sound menu emits raise twice per click
		#print(int(self.eventtime), int(localtime))
		if int(self.eventtime) == int(localtime):		
			pass
		else:
			self.signal_raise(False)
		self.eventtime = time()


	def signal_raise(self, justshow=None):
		pass

	@dbus.service.method(dbus.PROPERTIES_IFACE, in_signature='ss', out_signature='v')
	def Get(self, interface, prop):
		#print(prop)
		my_prop = self.__getattribute__(prop)
		return my_prop

	@dbus.service.method(dbus.PROPERTIES_IFACE, in_signature='ssv')
	def Set(self, interface, prop, value):
		my_prop = self.__getattribute__(prop)
		my_prop = value

	@dbus.service.method(dbus.PROPERTIES_IFACE, in_signature='s', out_signature='a{sv}')
	def GetAll(self, interface):
        	return [DesktopEntry, PlaybackStatus, MetaData]

	@dbus.service.method('org.mpris.MediaPlayer2.Player')
	def Next(self):
		self.signal_next()

	def signal_next(self):
		pass

	@dbus.service.method('org.mpris.MediaPlayer2.Player')
	def Previous(self):
		self.signal_prev()

	@dbus.service.method('org.mpris.MediaPlayer2.Player')
	def Stop(self):
		self.signal_stopped()

	def signal_prev(self):
		pass

	@dbus.service.method('org.mpris.MediaPlayer2.Player')
	def PlayPause(self):
		if self.PlaybackStatus == "Stopped" or self.PlaybackStatus == "Paused":
			self.signal_playing()
		else:
			self.signal_paused()
		self.signal_play_pause()

	def signal_play_pause(self):
		pass

	def signal_playing(self):
		self.__playback_status = "Playing"
		d = dbus.Dictionary({"PlaybackStatus":self.__playback_status, "Metadata":self.__meta_data},
		                            "sv",variant_level=1)
		self.PropertiesChanged("org.mpris.MediaPlayer2.Player",d,[])

	def signal_paused(self):
		self.__playback_status = "Paused"
		d = dbus.Dictionary({"PlaybackStatus":self.__playback_status},
		                            "sv",variant_level=1)
		self.PropertiesChanged("org.mpris.MediaPlayer2.Player",d,[])

	def signal_stopped(self):
		self.__playback_status = "Stopped"
		d = dbus.Dictionary({"PlaybackStatus":self.__playback_status},
		                            "sv",variant_level=1)
		self.PropertiesChanged("org.mpris.MediaPlayer2.Player",d,[])
            

	@dbus.service.signal(dbus.PROPERTIES_IFACE, signature='sa{sv}as')
	def PropertiesChanged(self, interface_name, changed_properties,
                          invalidated_properties):
        	pass

	def set_metadata(self, artists = None, album = None, title = None, arturl = None):        
		if artists is None:
			artists = ["Artist Unknown"]
		if album is None:
			album = "Album Uknown"
		if title is None:
			title = "Title Uknown"
		if arturl is None:
			arturl = "file://" + os.path.join(sopranoGlobals.DATADIR ,'crashbit-soprano.png')
   
		self.__meta_data = dbus.Dictionary({"xesam:album":album,"xesam:title":title,"xesam:artist":artists,"mpris:artUrl":arturl,}, "sv", variant_level=1)
