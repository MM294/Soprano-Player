import gst
import time

class MusicPlayer:
	def __init__(self, enableVideo=False):
		self.player = gst.element_factory_make("playbin2", "player")
		fakesink = gst.element_factory_make("fakesink", "fakesink")
		if not enableVideo:
			print('No Video')
			self.player.set_property("video-sink", fakesink)

	def change_volume(self, volume):		
		self.player.set_property('volume', volume)

	def set_track(self, filepath):
		self.player.set_property("uri", filepath)

	def play_item(self):
		self.player.set_state(gst.STATE_PLAYING)

	def pause_item(self):
		self.player.set_state(gst.STATE_PAUSED)

	def stop_play(self):
		self.player.set_state(gst.STATE_NULL)

	def seek(self, where):
		self.player.seek_simple(gst.FORMAT_TIME, gst.SEEK_FLAG_FLUSH, where)

	def get_state(self):
		return self.player.get_state()[1]

	def get_player(self):
		return self.player


#debugging function
def main():
	app = MusicPlayer(True)
	app.set_track("file:///media/Media/Music/Carlos Santana/Playin With Carlos/02-carlos_santana-too_late_too_late_(feat_gregg_rolie).mp3")
	app.change_volume(1.5)
	app.play_item()
	time.sleep(5)
	app.seek(50000000000)
	time.sleep(5)
	app.pause_item()
	print(app.get_state())
	app.change_volume(3)
	time.sleep(1)
	app.play_item()
	time.sleep(5)
	app.stop_play()

main()
