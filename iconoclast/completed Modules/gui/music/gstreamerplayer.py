import gst

class MusicPlayer:
	def __init__(self, enableVideo=False):
		self.player = gst.element_factory_make("playbin2", "player")
		fakesink = gst.element_factory_make("fakesink", "fakesink")
		if not enableVideo:
			self.player.set_property("video-sink", fakesink)

	def change_volume(self, volume):		
		self.player.set_property('volume', volume)

	def set_track(self, filepath):
		#replace characters that gstreamer doesnt like as a uri
		self.player.set_property("uri", filepath.replace('%', '%25').replace('#', '%23'))

	def get_track(self):
		return self.player.get_property("uri")

	def play_item(self):
		self.player.set_state(gst.STATE_PLAYING)

	def pause_item(self):
		self.player.set_state(gst.STATE_PAUSED)

	def stop_play(self):
		self.player.set_state(gst.STATE_NULL)

	def seek(self, where):
		currtracklength = self.player.query_duration(gst.FORMAT_TIME, None)[0]
		self.player.seek_simple(gst.FORMAT_TIME, gst.SEEK_FLAG_FLUSH, (currtracklength / 100)* where)

	def track_percent(self):
		tracklength = self.player.query_duration(gst.FORMAT_TIME, None)[0]
		position = self.player.query_position(gst.FORMAT_TIME, None)[0]
		return ((float(position)/tracklength)*100)

	def get_tracklength(self):
		tracklength = self.player.query_duration(gst.FORMAT_TIME, None)[0]
		return self.convert_ns(tracklength)

	def get_trackposition(self):
		position = self.player.query_position(gst.FORMAT_TIME, None)[0]
		return self.convert_ns(position)

	def get_state(self):
		return self.player.get_state()[1]

	def get_player(self):
		return self.player

	def on_eos(self, function):
		bus = self.player.get_bus()
		bus.add_signal_watch()
		bus.connect("message::eos", function)

	def convert_ns(self, t):
		#convert nanoseconds to hours minutes and seconds
		# This method was taken from a web tutorial by Sam Mason.
		s,ns = divmod(t, 1000000000)
		m,s = divmod(s, 60)

		if m < 60:
			return "%02i:%02i" %(m,s)
		else:
			h,m = divmod(m, 60)
			return "%i:%02i:%02i" %(h,m,s)


#debugging function
"""import time
def main():
	app = MusicPlayer(True)
	app.set_track("file:///media/Media/Music/Bob Dylan/Modern Times/06 - Workingman's Blues #2.ogg")
	app.change_volume(1.5)
	app.play_item()
	print app.get_track()
	time.sleep(5)
	app.seek(25)
	time.sleep(5)
	app.pause_item()
	print(app.get_state())
	app.change_volume(3)
	time.sleep(1)
	app.play_item()
	time.sleep(5)
	app.stop_play()

main()"""
