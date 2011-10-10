import threading
from music.tagreading import TrackMetaData

class myThread(threading.Thread):
	def run(self, action, widget):
		action = action.replace('%20',' ')
		getmesumdatabruv = TrackMetaData()
		x = getmesumdatabruv.getTrackType(action)		
		if x != False:
			x.insert(0, None)
			widget.append(x)
