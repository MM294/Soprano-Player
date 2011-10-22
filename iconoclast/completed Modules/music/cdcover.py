#Many props to Francois Inglerest, much of this cdcover code is based on the knowledge from decibel
import urllib2, os
from gi.repository import GdkPixbuf
import threading
from settings import sopranoGlobals

LASTFM_API_KEY = 'e92e11a5f1a8f8f154b45face4398499' #My Personal LastFM key, get your own if using this code in another application
USERAGENT = 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008072820 Firefox/7.0.0'

class getCover(threading.Thread):
	def __init__(self, artist, album, filelocation=None):
		self.artist = artist
		self.album = album	
		self.filelocation = filelocation

	def getLastFMCover(self, artist, album):
		url = 'http://ws.audioscrobbler.com/2.0/?method=album.getinfo&api_key=%s&artist=%s&album=%s' % (LASTFM_API_KEY, artist, album)
		request = urllib2.Request(url, headers = {'User-Agent': USERAGENT})
		try:
			stream = urllib2.urlopen(request)
			data = stream.read()

			startIdx  = data.find('<image size="large">')
			endIdx    = data.find('</image>', startIdx)
			if startIdx != -1 and endIdx != -1:
			    coverURL    = data[startIdx+len('<image size="large">'):endIdx]

			request = urllib2.Request(coverURL, headers = {'User-Agent': USERAGENT})
			stream  = urllib2.urlopen(request)
			data    = stream.read()
			output = open(sopranoGlobals.CACHEFILE, 'wb')
			output.write(data)
			output.close()
			return True
		except:
			return False

	def getLocalCover(self, filelocation=None):
		if filelocation:
			self.folderjpg = os.path.split(filelocation)[0] + '/' + 'Folder.jpg'
			if os.path.exists(self.folderjpg):
				stream = open(self.folderjpg, 'r')
				data = stream.read()			
				return True
			else:
				return False
		return False	

	def run(self):
		if self.getLocalCover(self.filelocation):
			img = GdkPixbuf.Pixbuf().new_from_file(self.folderjpg)
		elif self.getLastFMCover(self.artist, self.album):		
			img = GdkPixbuf.Pixbuf().new_from_file(sopranoGlobals.CACHEFILE)
		else:
			img = sopranoGlobals.PLACEHOLDER
		return img

#Debugging stuff and example usage below this, comment out when in use
"""from gi.repository import Gtk
coverFetch = getCover('Bob%20Dylan', 'Modern%20Times')
img = Gtk.Image()
img.set_from_pixbuf(coverFetch.run())


win = Gtk.Window()
win.connect("delete-event", Gtk.main_quit)
win.add(img)

win.show_all()
Gtk.main()"""
