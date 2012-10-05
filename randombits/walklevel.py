import os
from os.path import splitext
from tagreading import TrackMetaData

def get_music_library(top_level_dir=None):
	fileFormats = {'.mp3','.ogg','.oga','.wma','.flac','.m4a','.mp4'}
	songList = []

	def processDirectory ( args, dirname, filenames ):                              
	    for filename in filenames:     
		if splitext(filename.lower())[1] in fileFormats:
			#print dirname + '/' + filename
			songList.append(dirname + '/' + filename) 
		                                                                        
	if top_level_dir == None:
		top_level_dir = "/media/Media/Music"                                                    
	os.path.walk(top_level_dir, processDirectory, None )
	return songList

##os.path.walk() works with a callback: processDirectory() will be              
##called for each directory encountered.

#nosklo from stackoverflow i love you for this class!
class AutoVivification(dict):
    """Implementation of perl's autovivification feature."""
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value

aviv = AutoVivification()

resultArray = {}
metaData = TrackMetaData()
songList = get_music_library()
for i in songList:
	Title = metaData.getTrackType(i)[1]
	Artist = metaData.getTrackType(i)[2]
	Album = metaData.getTrackType(i)[3]
	if Artist == None:
		Artist = 'Unknown Artist'
	if Album == None:
		Album = 'Unknown Album'
	if Title == None:
		Title = 'Unknown Album'

	aviv[Artist][Album][Title][i]
print aviv
