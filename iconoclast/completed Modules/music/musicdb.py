#!/usr/bin/python
import sqlite3,os

from music.tagreading import TrackMetaData


class MusicDB:
	def __init__(self,dblocation):
		self.initialize_database(dblocation)

	def initialize_database(self,dblocation):
		self.conn = sqlite3.connect(dblocation)
		self.cursor = self.conn.cursor()
		#Create Table
		try:	self.cursor.execute("CREATE TABLE Songs(Id INTEGER PRIMARY KEY, TrackNum INTEGER, Title TEXT, Artist TEXT, Album TEXT,Length TEXT, Genre TEXT, Url TEXT);")
		except:	print("Table Exists")


	def rebuild_database(self,path):
		from time import time as systime
		systime1 = systime()

		trackparser = TrackMetaData()

		path = path.replace('file://','').replace('%20',' ') #simple but is a bit slow
		if os.path.isdir(path):
			for root, dirs, files in os.walk(path):
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
						self.cursor.execute("SELECT * FROM Songs WHERE Url='{}'".format(metadata[7]))
						if self.cursor.fetchone() == None:
							query = "INSERT INTO Songs(TrackNum,Title,Artist,Album,Length,Genre,Url) VALUES ({},'{}','{}','{}','{}','{}','{}');".format(metadata[1],metadata[2],metadata[3],metadata[4],metadata[5],metadata[6],metadata[7])
							self.cursor.execute(query)	
						else:
							query = "UPDATE Songs SET TrackNum='{}',Title='{}',Artist='{}',Album='{}',Length='{}',Genre='{}' WHERE Url='{}';".format(metadata[1],metadata[2],metadata[3],metadata[4],metadata[5],metadata[6],metadata[7])
							self.cursor.execute(query)	
			self.conn.commit()
		print("%s%f" % ("Operation took ",systime() - systime1))


"""#Example code
print(os.path.join(sopranoGlobals.CONFIGDIR, 'sopranoDB.db'))
SopranoDB = MusicDB(os.path.join(sopranoGlobals.CONFIGDIR, 'sopranoDB.db'))

SopranoDB.rebuild_database("file:///media/Media/Music")

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

