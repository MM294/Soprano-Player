from mutagen.mp3 import MP3
from mutagen.id3 import ID3
from mutagen.mp4 import MP4
from mutagen.oggvorbis import OggVorbis
from mutagen.flac import FLAC
from mutagen.asf import ASF
import os.path

FILE_FORMATS = {'.mp3','.ogg','.oga','.wma','.flac','.m4a','.mp4'}

class TrackMetaData:
	def getTrackType(self, filepath):
		options = {'.ogg' : self.oggInfo, '.oga' : self.oggInfo, '.mp4' : self.m4aInfo, '.m4a' : self.m4aInfo, '.mp2' : self.id3Info, '.mp3' : self.id3Info, '.flac' : self.flacInfo, '.wma' : self.wmaInfo,}

		fileExtension = os.path.splitext(filepath.lower())[1]
		if fileExtension in FILE_FORMATS:
			filepath = filepath.replace('%5B','[')
			filepath = filepath.replace('%5D',']')
			filepath = filepath.replace('file://','')
			filepath = filepath.replace('%25', '%')
			filepath = filepath.replace('%23', '#')
			return options[fileExtension](filepath)
		elif filepath[:7] == 'cdda://':#not filepath.find('cdda://') == -1:
			return self.cdtrkInfo(filepath)
		elif filepath[:7] == 'http://' or filepath[:6] == 'mms://':
			return self.radioInfo(filepath)
		else:
			return False

	def radioInfo(self, filepath):
		tracknum = None
		songtitle = "Unknown Title"
		artist = "Radio Station"
		album = "Radio Station"
		genre = None
		
		tracklength = "N/A"

		return [tracknum, songtitle, artist, album, tracklength, genre, filepath]		

	def cdtrkInfo(self, filepath):
		tracknum = int(filepath.replace('cdda://',''))
		songtitle = "Unknown Title"
		artist = "Unknown Artist"
		album = "Unknown Album"
		genre = None
		
		tracklength = "%02i:%02i" %(0,0)

		return [tracknum, songtitle, artist, album, tracklength, genre, filepath]

	def getTracklength(self, filepath):
		tracklength = int(round(MP3(filepath).info.length))
		m,s = divmod(tracklength, 60)
		tracklength = "%02i:%02i" %(m,s)
		return tracklength
		
	def id3Info(self, filepath):
		try: audio = MP3(filepath)
		except: return [0, '', '', '', self.getTracklength(filepath), '', filepath]

		try: tracknum = audio["TRCK"][0]
		except: tracknum = None
		if tracknum is not None:
			try:    tracknum = int(tracknum.split('/')[0])
			except ValueError: tracknum = 0
			except: tracknum = int(tracknum)
		try: songtitle = audio["TIT2"][0]
		except: songtitle = "Unknown Title"
		try: artist = audio["TPE1"][0]
		except: artist = "Unknown Artist"
		try: album = audio["TALB"][0]
		except: album = "Unknown Album"
		try: genre = audio["TCON"][0]
		except: genre = None

		tracklength = int(round(audio.info.length))
		m,s = divmod(tracklength, 60)
		tracklength = "%02i:%02i" %(m,s)
		filepath = "file://" + filepath
		return [tracknum, songtitle, artist, album, tracklength, genre, filepath]

	def m4aInfo(self, filepath):
		try: audio = MP4(filepath)
		except: return [0, '', '', '', self.getTracklength(filepath), '', filepath]

		try: tracknum = audio["trkn"][0][0]
		except: tracknum = None
		if tracknum is not None:
			try:    tracknum = int(tracknum.split('/')[0])
			except ValueError: tracknum = 0
			except: tracknum = int(tracknum)
		try: songtitle = audio["\xa9nam"][0]
		except: songtitle = "Unknown Title"
		try: artist = audio["\xa9ART"][0]
		except: artist = "Unknown Artist"
		try: album = audio["\xa9alb"][0]
		except: album = "Unknown Album"
		try: genre = audio["\xa9gen"][0]
		except: genre = None

		tracklength = int(round(audio.info.length))
		m,s = divmod(tracklength, 60)
		tracklength = "%02i:%02i" %(m,s)
		filepath = "file://" + filepath
		return [tracknum, songtitle, artist, album, tracklength, genre, filepath]

	def oggInfo(self, filepath):
		try: audio = OggVorbis(filepath)
		except: return [0, '', '', '', self.getTracklength(filepath), '', filepath]

		try: tracknum = audio["tracknumber"][0] 
		except: tracknum = None
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
		except: genre = None

		tracklength = int(round(audio.info.length))
		m,s = divmod(tracklength, 60)
		tracklength = "%02i:%02i" %(m,s)
		filepath = "file://" + filepath
		return [tracknum, songtitle, artist, album, tracklength, genre, filepath]

	def flacInfo(self, filepath):
		try: audio = FLAC(filepath)
		except: return [0, '', '', '', self.getTracklength(filepath), '', filepath]

		try: tracknum = audio["tracknumber"][0] 
		except: tracknum = None
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
		except: genre = None

		tracklength = int(round(audio.info.length))
		m,s = divmod(tracklength, 60)
		tracklength = "%02i:%02i" %(m,s)
		filepath = "file://" + filepath
		return [tracknum, songtitle, artist, album, tracklength, genre, filepath]

	def wmaInfo(self, filepath):
		try: audio = ASF(filepath)
		except: return [0, '', '', '', self.getTracklength(filepath), '', filepath]

		try: tracknum = audio["WM/TrackNumber"][0]
		except: tracknum = None
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
		except: genre = None

		tracklength = int(round(audio.info.length))
		m,s = divmod(tracklength, 60)
		tracklength = "%02i:%02i" %(m,s)
		filepath = "file://" + filepath
		return [tracknum, songtitle, artist, album, tracklength, genre, filepath]

#getmesumdatabruv = TrackMetaData()
#print(getmesumdatabruv.getTrackType("/media/Media/Music/Carlos Santana/Playin With Carlos/02-carlos_santana-too_late_too_late_(feat_gregg_rolie).mp3"))
