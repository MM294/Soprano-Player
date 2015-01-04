from mutagenx.mp3 import MP3
from mutagenx.id3 import ID3
from mutagenx.mp4 import MP4
from mutagenx.oggvorbis import OggVorbis
from mutagenx.flac import FLAC
from mutagenx.asf import ASF
import os.path, magic
from settings import sopranoGlobals, settings


FILE_FORMATS = {'.mp3','.ogg','.oga','.wma','.flac','.m4a','.mp4','.aac'}
#FILE_FORMATS = {'.audio/mp4; charset=binary','audio/mpeg; charset=binary','application/ogg; charset=binary','audio/x-flac; charset=binary','audio/x-wav; charset=binary','audio/x-ms-asf; charset=binary','video/x-ms-asf; charset=binary','application/octet-stream; charset=binary'}
#Including octet-stream to work around magic not correctly identifying mp3 with image metadata

class TrackMetaData:
	def getTrackType(self, filepath):
		m = magic.open(magic.MAGIC_MIME)
		m.load()
#		options = {	'application/ogg; charset=binary' : self.oggInfo,
#					'.audio/mp4; charset=binary' : self.m4aInfo,
#					'audio/mpeg; charset=binary' : self.id3Info,
#					'audio/x-flac; charset=binary' : self.flacInfo,
#					'audio/x-ms-asf; charset=binary' : self.wmaInfo,
#					'video/x-ms-asf; charset=binary' : self.wmaInfo,
#					'audio/x-wav; charset=binary' : self.id3Info}

		options = {	'.ogg' : self.oggInfo,
					'.oga' : self.oggInfo,
					'.mp4' : self.m4aInfo,
					'.m4a' : self.m4aInfo,
					'.mp3' : self.id3Info,
					'.flac' : self.flacInfo,
					'.wma' : self.wmaInfo,
					'.asf' : self.wmaInfo,
					'.wav' : self.id3Info}

		fileExtension = os.path.splitext(filepath.lower())[1]
		filepath = filepath.replace('file://','')
		#try: fileDescription = m.file(filepath)
		#except: fileDescription = "Invalid Format"
		if filepath[:7] == 'http://' or filepath[:6] == 'mms://':
			return self.radioInfo(filepath)
		elif fileExtension in FILE_FORMATS:
			filepath = filepath.replace('%5B','[').replace('%5D',']').replace('%25', '%').replace('%23', '#')
			if os.path.exists(filepath):
				return options[fileExtension](filepath)
				#return options[fileDescription](filepath)
			else:
				return False
		elif filepath[:7] == 'cdda://':
			return self.cdtrkInfo(filepath)
		else:
			return False

	def radioInfo(self, filepath):
		self.editPref = settings.IconoPrefs(sopranoGlobals.RADIO_DATA)
		stations = self.editPref.get_radioStations()
		for key, value in self.editPref.get_radioStations().items():
			if filepath == value:
				songtitle = key
				break
			else:
				songtitle = "Unknown Title"

		tracknum = 0		
		artist = "Radio Station"
		album = "Radio Station"
		genre = "None"
		
		tracklength = "N/A"

		return [None, tracknum, songtitle, artist, album, tracklength, genre, filepath]		

	def cdtrkInfo(self, filepath):
		tracknum = int(filepath.replace('cdda://',''))
		songtitle = "Track " + str(tracknum)
		artist = "Unknown Artist"
		album = "Compact Disc"
		genre = "None"
		
		tracklength = "%02i:%02i" %(0,0)

		return [None, tracknum, songtitle, artist, album, tracklength, genre, filepath]

	def getTracklength(self, filepath):
		tracklength = int(round(MP3(filepath).info.length))
		m,s = divmod(tracklength, 60)
		tracklength = "%02i:%02i" %(m,s)
		return tracklength
		
	def id3Info(self, filepath):
		#from time import time as systime
		#systime1 = systime()
		try: audio = MP3(filepath)
		except: return [None, 0, '', '', '', self.getTracklength(filepath), '', filepath]
		#print(systime() - systime1)
		try: tracknum = audio["TRCK"][0]
		except: tracknum = 0
		if tracknum is not None:
			try:    tracknum = int(tracknum.split('/')[0])
			except ValueError: tracknum = 0
			except: tracknum = int(tracknum)
		#print (audio["TIT2"][0]).encode('ascii', 'replace')
		try: songtitle = (audio["TIT2"][0])#.encode('ascii', 'replace')
		except: songtitle = "Unknown Title"
		try: artist = audio["TPE1"][0]
		except: artist = "Unknown Artist"
		try: album = audio["TALB"][0]
		except: album = "Unknown Album"
		try: genre = audio["TCON"][0]
		except: genre = "None"

		tracklength = int(round(audio.info.length))
		m,s = divmod(tracklength, 60)
		tracklength = "%02i:%02i" %(m,s)
		filepath = "%s%s" % ("file://",filepath)
		return [None, tracknum, songtitle, artist, album, tracklength, genre, filepath]

	def m4aInfo(self, filepath):
		try: audio = MP4(filepath)
		except: return [None, 0, '', '', '', self.getTracklength(filepath), '', filepath]

		try: tracknum = audio["trkn"][0][0]
		except: tracknum = 0
		if tracknum is not None:
			try:    tracknum = int(tracknum.split('/')[0])
			except ValueError: tracknum = 0
			except: tracknum = int(tracknum)

		#python3.x
		try: songtitle = audio[b"\xa9nam"][0]
		except: songtitle = "Unknown Title"
		try: artist = audio[b"\xa9ART"][0]
		except: artist = "Unknown Artist"
		try: album = audio[b"\xa9alb"][0]
		except: album = "Unknown Album"
		try: genre = audio[b"\xa9gen"][0]
		except: genre = "None"""

		"""#python2.7
		try: songtitle = audio["\xa9nam"][0]
		except: songtitle = "Unknown Title"
		try: artist = audio["\xa9ART"][0]
		except: artist = "Unknown Artist"
		try: album = audio["\xa9alb"][0]
		except: album = "Unknown Album"
		try: genre = audio["\xa9gen"][0]
		except: genre = "None"""

		tracklength = int(round(audio.info.length))
		m,s = divmod(tracklength, 60)
		tracklength = "%02i:%02i" %(m,s)
		filepath = "%s%s" % ("file://",filepath)
		return [None, tracknum, songtitle, artist, album, tracklength, genre, filepath]

	def oggInfo(self, filepath):
		try: audio = OggVorbis(filepath)
		except: return [None, 0, '', '', '', self.getTracklength(filepath), '', filepath]

		try: tracknum = audio["tracknumber"][0] 
		except: tracknum = 0
		if tracknum is not None:
			try:    tracknum = int(tracknum.split('/')[0])
			except ValueError: tracknum = 0
			except: tracknum = int(tracknum)
		try: songtitle = audio["title"][0]
		except: songtitle = "Unknown Title"
		try: artist = audio["artist"][0]
		except: artist = "Unknown Artist"
		try: album = audio["album"][0]
		except: album = "Unknown Album"
		try: genre = audio["genre"][0]
		except: genre = "None"

		tracklength = int(round(audio.info.length))
		m,s = divmod(tracklength, 60)
		tracklength = "%02i:%02i" %(m,s)
		filepath = "%s%s" % ("file://",filepath)
		return [None, tracknum, songtitle, artist, album, tracklength, genre, filepath]

	def flacInfo(self, filepath):
		try: audio = FLAC(filepath)
		except: return [None, 0, '', '', '', self.getTracklength(filepath), '', filepath]

		try: tracknum = audio["tracknumber"][0] 
		except: tracknum = 0
		if tracknum is not None:
			try:    tracknum = int(tracknum.split('/')[0])
			except ValueError: tracknum = 0
			except: tracknum = int(tracknum)
		try: songtitle = audio["title"][0]
		except: songtitle = "Unknown Title"
		try: artist = audio["artist"][0]
		except: artist = "Unknown Artist"
		try: album = audio["album"][0]
		except: album = "Unknown Album"
		try: genre = audio["genre"][0]
		except: genre = "None"

		tracklength = int(round(audio.info.length))
		m,s = divmod(tracklength, 60)
		tracklength = "%02i:%02i" %(m,s)
		filepath = "%s%s" % ("file://",filepath)
		return [None, tracknum, songtitle, artist, album, tracklength, genre, filepath]

	def wmaInfo(self, filepath):
		try: audio = ASF(filepath)
		except: return [None, 0, '', '', '', self.getTracklength(filepath), '', filepath]

		try: tracknum = audio["WM/TrackNumber"][0]
		except: tracknum = 0
		if tracknum is not None:
			try:    tracknum = int(tracknum.split('/')[0])
			except ValueError: tracknum = 0
			except: tracknum = int(tracknum)
		try: songtitle = str(audio["Title"][0])
		except: songtitle = "Unknown Title"
		try: artist = str(audio["Author"][0])
		except: artist = "Unknown Artist"
		try: album = str(audio["WM/AlbumTitle"][0])
		except: album = "Unknown Album"
		try: genre = str(audio["WM/Genre"][0])
		except: genre = "None"

		tracklength = int(round(audio.info.length))
		m,s = divmod(tracklength, 60)
		tracklength = "%02i:%02i" %(m,s)
		filepath = "%s%s" % ("file://",filepath)
		return [None, tracknum, songtitle, artist, album, tracklength, genre, filepath]

#getmesumdatabruv = TrackMetaData()
#print(getmesumdatabruv.getTrackType("/media/Media/Music/Noel Gallagher/High Flying Birds/01 Everybody's On The Run.mp3"))
