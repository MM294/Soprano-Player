import os
from os.path import splitext

fileFormats = {'.mp3','.ogg','.oga','.wma','.flac','.m4a','.mp4'}

def processDirectory ( args, dirname, filenames ):                              
    for filename in filenames:     
	if splitext(filename.lower())[1] in fileFormats:
		print dirname + '/' + filename                                               
                                                                                
top_level_dir = "/media/Media/Music"                                                    
os.path.walk(top_level_dir, processDirectory, None )                            
                                                                                
##os.path.walk() works with a callback: processDirectory() will be              
##called for each directory encountered.
