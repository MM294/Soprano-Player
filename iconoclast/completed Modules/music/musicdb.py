#!/usr/bin/python
import sqlite3,os,threading

from music.tagreading import TrackMetaData


class MusicDB(threading.Thread):
	def __init__(self,dblocation):
		threading.Thread.__init__(self)
		self.initialize_database(dblocation)
		self.dblocation = dblocation
		self.libraryfolders = []

	def add_folder(self,folder):
		if folder not in self.libraryfolders:
			self.libraryfolders.append(folder)

	def initialize_database(self,dblocation):
		self.conn = sqlite3.connect(dblocation)
		self.cursor = self.conn.cursor()
		#Create Table
		try:	self.cursor.execute("CREATE TABLE Songs(Id INTEGER PRIMARY KEY, TrackNum INTEGER, Title TEXT, Artist TEXT, Album TEXT,Length TEXT, Genre TEXT, Url TEXT);")
		except:	print("Table Exists")


	def rebuild_database(self):
		#Tempory Database connection for thread
		conn = sqlite3.connect(self.dblocation)
		cursor = conn.cursor()
		trackparser = TrackMetaData()

		#clear out current database
		cursor.execute("DELETE FROM Songs")

		for libraryfolder in self.libraryfolders:
			libraryfolder = libraryfolder.replace('file://','').replace('%20',' ') #simple but is a bit slow
			if os.path.isdir(libraryfolder):
				for root, dirs, files in os.walk(libraryfolder):
					for name in files:
						metadata = trackparser.getTrackType(os.path.join(root, name))
						if metadata != False:
							#escape single quotes for sql query
							metadata[2] = metadata[2].replace("'","''")#Title
							metadata[3] = metadata[3].replace("'","''")#Artist
							metadata[4] = metadata[4].replace("'","''")#Album
							metadata[6] = metadata[6].replace("'","''")#Genre
							metadata[7] = metadata[7].replace("'","''")#Url

							#build query and encode to ascii for python 2
							#query = "INSERT INTO Songs(TrackNum,Title,Artist,Album,Length,Genre,Url) VALUES ({},'{}','{}','{}','{}','{}','{}');".format(metadata[1],metadata[2].encode('ascii','ignore'),metadata[3].encode('ascii','ignore'),metadata[4].encode('ascii','ignore'),metadata[5].encode('ascii','ignore'),metadata[6].encode('ascii','ignore'),metadata[7])
							
							#since we truncate anyway, checking for existing entrys is redundant for now
							"""cursor.execute("SELECT * FROM Songs WHERE Url='{}'".format(metadata[7]))
							if cursor.fetchone() == None:
								query = "INSERT INTO Songs(TrackNum,Title,Artist,Album,Length,Genre,Url) VALUES ({},'{}','{}','{}','{}','{}','{}');".format(metadata[1],metadata[2],metadata[3],metadata[4],metadata[5],metadata[6],metadata[7])
								cursor.execute(query)	
							else:
								query = "UPDATE Songs SET TrackNum='{}',Title='{}',Artist='{}',Album='{}',Length='{}',Genre='{}' WHERE Url='{}';".format(metadata[1],metadata[2],metadata[3],metadata[4],metadata[5],metadata[6],metadata[7])
								cursor.execute(query)"""
							query = "INSERT INTO Songs(TrackNum,Title,Artist,Album,Length,Genre,Url) VALUES ({},'{}','{}','{}','{}','{}','{}');".format(metadata[1],metadata[2],metadata[3],metadata[4],metadata[5],metadata[6],metadata[7])
							cursor.execute(query)	
				conn.commit()

	def run(self):
		self.rebuild_database()


"""#Example code
from settings import sopranoGlobals
SopranoDB = MusicDB(os.path.join(sopranoGlobals.CONFIGDIR, 'sopranoDB.db'))

SopranoDB.add_folder("file:///media/Media/Music")
SopranoDB.add_folder("file:///media/Media/Music/Aerosmith")

SopranoDB.run()
while SopranoDB.is_alive():
	pass

#SopranoDB.cursor.execute("SELECT * FROM Songs ORDER BY RANDOM() LIMIT 1")
#SopranoDB.cursor.execute("SELECT count(*) FROM Songs WHERE Artist='Foo Fighters'")
SopranoDB.cursor.execute("SELECT DISTINCT Artist FROM Songs")
rows = SopranoDB.cursor.fetchall()
print("Artists", len(rows))

SopranoDB.cursor.execute("SELECT DISTINCT Album FROM Songs")
rows = SopranoDB.cursor.fetchall()
print("Albums", len(rows))

SopranoDB.cursor.execute("SELECT count(*) FROM Songs;")
rows = SopranoDB.cursor.fetchall()
print("Songs", rows[0][0])"""

