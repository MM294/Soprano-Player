from gi.repository import Gtk, GdkPixbuf, Gdk, Gio, GObject
import os
import gst

from aboutbox import aboutBoxShow
from tagreading import TrackMetaData
from FileExplorer import FileBrowser

def widget_hide(widget, button):
    widget.hide()

class BuilderApp:
	def __init__(self):
		#Gstreamer Bits#
		self.player = gst.element_factory_make("playbin2", "player")
		fakesink = gst.element_factory_make("fakesink", "fakesink")
		self.player.set_property("video-sink", fakesink)
		#timer to update the time labels and seek bar#
		self.timer = GObject.timeout_add(500, self.update_time_labels)

		#Window Creation
		self.builder = Gtk.Builder()
		filename = os.path.join('', 'MainWindow.glade')        

		self.builder.add_from_file(filename)
		self.builder.connect_signals(self)	

		self.window = self.builder.get_object('win-main')
		self.window.set_default_size(900, 550)
		self.window.connect('destroy', lambda x: Gtk.main_quit())
		self.window.show_all()
		#register drag and drop
	
		self.treeview = self.builder.get_object('treeview1')
		self.treeview.drag_dest_set(0, [], 0)
		self.treeview.connect('drag_motion', self.motion_cb)
		self.treeview.connect('drag_drop', self.drop_cb)
		self.treeview.connect('drag_data_received', self.got_data_cb)

		#Quit, About Menus
		self.menuaqt = self.builder.get_object('menu-quit')
		self.menuaqt.connect('activate', self.quit_activate)

		self.menuabt = self.builder.get_object('menu-about')
		self.menuabt.connect('activate', self.about_activate)

		#View Menu#
		self.menuvfull = self.builder.get_object('menu-mode-full')
		self.menuvfull.connect('activate', self.to_full_mode)

		self.menuvlean = self.builder.get_object('menu-mode-lean')
		self.menuvlean.connect('activate', self.to_lean_mode)

		self.menuvmini = self.builder.get_object('menu-mode-mini')
		self.menuvmini.connect('activate', self.to_mini_mode)

		self.menuvplist = self.builder.get_object('menu-mode-playlist')
		self.menuvplist.connect('activate', self.to_playlist_mode)

		#playing Toolbar
		self.toolprev = self.builder.get_object('btn-previous')
		self.toolprev.connect('clicked', self.stop_play)

		self.toolstop = self.builder.get_object('btn-stop')
		self.toolstop.connect('clicked', self.stop_play)

		self.toolplay = self.builder.get_object('btn-play')
		self.toolplay.connect('clicked', self.play_pause)

		self.toolSeekBar = self.builder.get_object('scl-position')
		self.toolSeekBar.connect('change-value', self.seek)

		self.toolVolume = self.builder.get_object('btn-volume')
		self.toolVolume.connect('value-changed', self.change_volume)

		#listview#
		self.listview = self.builder.get_object('treeview1')
		self.listview.connect('row-activated', self.on_activated)

		#listviewModel
		self.model = self.builder.get_object('liststore1')

		self.notebook = self.builder.get_object('notebook-explorer')
		self.explorer = FileBrowser('/media/Media/Music')
		self.notebook.add(self.explorer.get_sw())
		self.notebook.show_all()


	#Math Funcs and Other Handlers#

	def update_time_labels(self):
		playstate = self.player.get_state()[1]
		if (playstate == gst.STATE_PLAYING):
			self.seek_scale_set(None)
			self.sclSeek = self.builder.get_object('scl-position')
			self.position = self.player.query_position(gst.FORMAT_TIME, None)[0]
			self.sclSeek.set_value(self.position)

			self.currTrackPosText = self.convert_ns(self.position)
			self.timeLabel = self.builder.get_object('lbl-elapsedTime')
			self.timeLabel.set_text(self.currTrackPosText)
		return True
		
	def convert_ns(self, t):
		# This method was taken from a web tutorial by Sam Mason.
		s,ns = divmod(t, 1000000000)
		m,s = divmod(s, 60)

		if m < 60:
			return "%02i:%02i" %(m,s)
		else:
			h,m = divmod(m, 60)
			return "%i:%02i:%02i" %(h,m,s)

	def about_activate(self, action):
		aboutBoxShow(self.window)

	def quit_activate(self, action):
        	Gtk.main_quit()

	#Listbox Handlers
	def add_row(self, action):
		action = action.replace('%20',' ')
		getmesumdatabruv = TrackMetaData()
		x = getmesumdatabruv.getTrackType(action)
		x.insert(0, None)
		#print x
		if getmesumdatabruv.getTrackType(action) != False:
			self.model.append(x)

	def on_activated(self, widget, row, col):        
		model = widget.get_model()

		text = model[row][7]
		text = "file://" + text 
		self.playitem(text)
		
		self.set_playmark(row)

	def clear_playmark(self):
		i = 0
		while i != len(self.model):
			self.model.set_value(self.model.get_iter(i), 0, '')
			i = i+1

	def set_playmark(self, row):
		self.clear_playmark()		
		try: self.model.set_value(row, 0, 'media-playback-start')
		except: self.model.set_value(self.model.get_iter(row), 0, 'media-playback-start')

	#Drag and Drop Handling
	def motion_cb(self, windowid, context, x, y, time):
		#windowid.drag_get_data(context, context.list_targets()[-1], time)
		return True

	def drop_cb(self, windowid, context, x, y, time):
		# Some data was dropped, get the data
		windowid.drag_get_data(context, context.list_targets()[-1], time)
		return True

	def got_data_cb(self, windowid, context, x, y, data, info, time):
		# Got data.
		tempArray = data.get_text().splitlines()
		for i in tempArray:
			i = i.replace('file://','')
			#print i
			self.add_row(i)
		context.finish(True, False, time)

	#View Mode Menu Handlers#
	def to_full_mode(self, unused):
		self.builder.get_object('pan-main').get_child1().show()
		self.builder.get_object('statusbar').show()
		self.builder.get_object('box-btn-tracklist').show()
		self.builder.get_object('scrolled-tracklist').show()
		self.window.resize(900, 550)

	def to_lean_mode(self, unused):
		self.to_full_mode(None)	
		self.builder.get_object('box-btn-tracklist').hide()

	def to_mini_mode(self, unused):
		self.to_full_mode(None)	
		self.builder.get_object('pan-main').get_child1().hide()
		self.builder.get_object('statusbar').hide()
		self.builder.get_object('box-btn-tracklist').hide()
		self.builder.get_object('scrolled-tracklist').hide()
		self.window.resize(600, 150)

	def to_playlist_mode(self, unused):
		self.to_full_mode(None)	
		self.window.resize(600, 550)
		self.builder.get_object('pan-main').get_child1().hide()

	#Bottom Toolbar Handlers#
	def clear_liststore(self, action):
		self.model.clear()    

	#Audio Control Widget Handlers#
	def change_volume(self, volume, unused):
		volume = self.builder.get_object('btn-volume').get_value()
		self.player.set_property('volume', volume)

	def seek_scale_set(self, unused):
		self.sclSeek = self.builder.get_object('scl-position')

		self.currTrackLength = (self.player.query_duration(gst.FORMAT_TIME, None)[0])
		self.sclSeek.set_range(0, self.currTrackLength)

		self.currTrackLengthText = self.convert_ns(self.currTrackLength)
		self.timeLabel = self.builder.get_object('lbl-remainingTime')
		self.timeLabel.set_text(self.currTrackLengthText)

	#Gstreamer Player Handlers#
	def play_pause(self, filepath):
		selected = self.builder.get_object('treeview-selection1')

		if selected.get_selected()[1] != None:
			modeliter = selected.get_selected()[1]
			self.set_playmark(modeliter)
		elif self.model.get_iter_first() != None:
			modeliter = self.model.get_iter_first()
			self.set_playmark(0)

		filepath = self.model.get_value(modeliter, 7)

		toolplayimg = self.builder.get_object('image3')
		playstate = self.player.get_state()[1]
		if (playstate == gst.STATE_PLAYING):
			self.player.set_state(gst.STATE_PAUSED)

			toolplayimg.set_from_icon_name('media-playback-start', Gtk.IconSize.LARGE_TOOLBAR)			
		elif os.path.isfile(filepath):
			self.player.set_property("uri", "file://" + filepath)
			self.player.set_state(gst.STATE_PLAYING)

			toolplayimg.set_from_icon_name('media-playback-pause', Gtk.IconSize.LARGE_TOOLBAR)

	def playitem(self, filepath):
		self.player.set_state(gst.STATE_NULL)
		self.player.set_property("uri", filepath)
		self.player.set_state(gst.STATE_PLAYING)

		toolplayimg = self.builder.get_object('image3')
		toolplayimg.set_from_icon_name('media-playback-pause', Gtk.IconSize.LARGE_TOOLBAR)	

	def stop_play(self, unused):
		self.player.set_state(gst.STATE_NULL)

		self.timeLabel = self.builder.get_object('lbl-remainingTime')
		self.timeLabel.set_text('')
		self.elapsedTimeLabel = self.builder.get_object('lbl-elapsedTime')
		self.elapsedTimeLabel.set_text('')

		self.clear_playmark()
		toolplayimg = self.builder.get_object('image3')
		toolplayimg.set_from_icon_name('media-playback-start', Gtk.IconSize.LARGE_TOOLBAR)

	def seek(self, widget, test, where):
		self.player.seek_simple(gst.FORMAT_TIME, gst.SEEK_FLAG_FLUSH, where)
		self.update_time_labels()

def main(iconoclast=None):
	app = BuilderApp()
	#default to playlist till i fix other shit#
	#app.to_playlist_mode(None)      

	#bottom toolbar
	barclr = app.builder.get_object('btn-tracklistClear')
	barclr.connect('clicked', app.clear_liststore)

	if __name__ == '__main__':
		Gtk.main()

main()
