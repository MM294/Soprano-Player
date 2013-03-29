import os.path
from gi.repository import TotemPlParser

FILE_FORMATS = {'.m3u', '.pls'}

for i in dir(TotemPlParser):
	output = open('output.txt', 'a')
	output.write(i)
	output.write('\n')
	output.close()

aparser = TotemPlParser
print aparser.Parser().parse('file:///home/mike/Desktop/Python/IconoClast/Sample Files/playlists/hardradio192.pls', False)
apls = aparser.Playlist.new()
aniter = aparser.get_iter_first(apls)
print aparser.Playlist.get_value(aparser.Playlist.new().iter_first(),'uri', 'TOTEM_PL_PARSER_FIELD_URI', False)
print dir(TotemPlParser.Playlist)


"""class PlaylistHandler:
	def isSupported(self, filepath):
	   	fileExtension = os.path.splitext(filepath.lower())[1]
		if fileExtension in FILE_FORMATS:
			self.openpls(filepath)

	def openpls(self, filepath):
		output = open(filepath, 'rb')
		data = output.read()
		print data
		output.close()

ahandler = PlaylistHandler()
ahandler.isSupported('/home/mike/Desktop/Python/IconoClast/Sample Files/playlists/hardradio192.pls')"""
