#jimjamjihah i love you!
from gi.repository import GObject
import dbus, sys
from dbus.mainloop.glib import DBusGMainLoop

class mediakeys(object):
	def __init__(self, prevfunc, playfunc, nextfunc):
		self.prevfunc = prevfunc
		self.playfunc = playfunc
		self.nextfunc = nextfunc  
		self.getkeys()

	def getkeys(self):
		DBusGMainLoop(set_as_default=True)
		self.bus = dbus.SessionBus()

		"""running = self.bus.get_object('org.freedesktop.DBus', '/org/freedesktop/DBus').ListNames()
		sopranobusName = dbus.service.BusName('org.freedesktop.sopranoaudioplayer', bus=self.bus)
		dbus.service.Object.__init__(sopranobusName, self, '/')
		f = open('/home/mike/Desktop/output.txt', 'a')
		for i in running:
			f.write(i)
			f.write('\n')
		f.close()
		
		sopranobusName
		if sopranobusName in running:
			print "oh shit another instance!"
			sys.exit(1)
		#print running"""		

		self.bus_object = self.bus.get_object('org.gnome.SettingsDaemon', '/org/gnome/SettingsDaemon/MediaKeys')
		self.bus_object.GrabMediaPlayerKeys('Soprano', 0, dbus_interface='org.gnome.SettingsDaemon.MediaKeys')
		self.bus_object.connect_to_signal('MediaPlayerKeyPressed', self.handle_mediakeys)
        
	def handle_mediakeys(self, caller, command):
		print command
		if command == 'Previous':
			self.prevfunc()
		elif command == 'Play':
			self.playfunc()
		elif command == 'Next':
			self.nextfunc()
"""if __name__ == "__main__":
    mediakeys()
    GObject.MainLoop().run()"""
