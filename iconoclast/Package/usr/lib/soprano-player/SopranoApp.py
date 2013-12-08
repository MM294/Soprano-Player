#!/usr/bin/python3
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gtk, GdkPixbuf, GObject, Notify, Gst# about 8.5 Mb memory used here
try:
	from gi.repository import AppIndicator3
except:
	print("No Indicator Support")
import os.path#, gst #gst uses 4.5 Mb of memory alone

from settings import settings
from settings import sopranoGlobals

from music.mediakeys import mediakeys
from music.tagreading import TrackMetaData
from music.cdcover import getCover # 10.6 Mb of Memory
from music.gstreamerplayerGOBJECT import MusicPlayer
from music.mpris import SoundMenuControls
from music.musicdb import MusicDB

from gui.combobox import HeaderedComboBox
from gui.aboutbox import aboutBoxShow
from gui.propertreefilebrowser import IconoTreeFile # about 14.5mb of memory
from gui.AudioCD import IconoAudioCD # 14.3mb of Memory
from gui.NetRadio import IconoRadio
from gui.liststore import IconoListView # about 11.2mb of memory
from gui.prefs import SopranoPrefWin
from gui.trayicon import IconoTray
from gui.medialibrary import IconoMediaLibrary

class SopranoApp:
	def __init__(self):
		#Global Variables (keep to a minimum)
		self.settings = settings.IconoSettings(sopranoGlobals.SETTINGS_DATA)
		self.taglookup = TrackMetaData()
		self.seekingnow = False		
		#load settings
		self.currentview, self.winwidth, self.winheight, self.defaultexplorer, self.shuffle, self.repeat, self.showtrayicon, self.closetotray = self.settings.get_settings()

		libraryFolderlist = settings.IconoPrefs(sopranoGlobals.LIBRARY_DATA)
		self.SopranoDB = MusicDB(os.path.join(sopranoGlobals.CONFIGDIR, 'sopranoDB.db'))
		libraryFolderlist.add_radio(('/media/Media/Music','/media/Media/Music'))
		for key,value in libraryFolderlist.get_radioStations().items():
			self.SopranoDB.add_folder(value)

		#turn on the dbus mainloop for sound menu
		from dbus.mainloop.glib import DBusGMainLoop
		DBusGMainLoop(set_as_default=True)
		#Start Sound Menu Support
		self.sopranompris = SoundMenuControls("soprano-player")
		self.sopranompris.signal_next = self.play_next
		self.sopranompris.signal_prev = self.play_prev
		self.sopranompris.signal_play_pause = self.play_pause
		self.sopranompris.signal_raise = self.toggle_window

		#Enable Notifications
		Notify.init ("Soprano")
		self.notification = Notify.Notification.new("","","")

		#Window Creation
		self.builder = Gtk.Builder()
		filename = os.path.join('data', 'MainWindow.glade')
		self.builder.add_from_file(filename)
		self.builder.connect_signals(self)

		self.window = self.builder.get_object('win-main')
		self.window.set_default_size(self.winwidth,self.winheight)
		self.window.connect('delete-event', self.pre_exit)
		
		#radiowindow
		self.aRadio = IconoRadio()

		#Gstreamer sink
		self.player = MusicPlayer()
		self.player.on_eos(self.on_message)
		#media keys setup
		self.mediakeys = mediakeys(self.play_prev, self.play_pause, self.play_next)

		timer = GObject.timeout_add(500, self.update_time_items)

		#trayicon
		self.tray = IconoTray("soprano-player-tray") 
		self.trayshowhide = self.tray.add_menu_item(self.toggle_window, "Hide/Show")
		self.tray.add_seperator()
		self.trayplaypause = self.tray.add_menu_item(self.play_pause, "Play/Pause")
		self.tray.add_menu_item(self.play_next, "Next")
		self.tray.add_menu_item(self.play_prev, "Previous")
		self.tray.add_seperator()
		self.tray.add_menu_item(self.on_exit, "Quit")
		self.update_tray_icon(self.showtrayicon)


		#View Menu#
		menuvfull = self.builder.get_object('menu-mode-full')
		menuvfull.connect('activate', self.to_full_mode)
		menuvmini = self.builder.get_object('menu-mode-mini')
		menuvmini.connect('activate', self.to_mini_mode)
		menuvplist = self.builder.get_object('menu-mode-playlist')
		menuvplist.connect('activate', self.to_playlist_mode)

		#Quit, About Menus
		menuaqt = self.builder.get_object('menu-quit')
		menuaqt.connect('activate',self.on_exit)
		menuabt = self.builder.get_object('menu-about')
		menuabt.connect('activate', aboutBoxShow, self.window)

		#Edit Menu#
		menuaddfolder = self.builder.get_object('menu-folderadd')
		#menuaddfolder.connect('activate', lambda x: self.addFolderExplorer(('Video','/media/Media/Videos')))
		menuaddfolder.connect('activate', self.show_pref_win)

		menuaddradio = self.builder.get_object('menu-radioadd')
		#menuaddradio.connect('activate', lambda x: self.delFolderExplorer(('Video','/media/Media/Videos')))
		menuaddradio.connect('activate', self.aRadio.addStationDialog)

		#playing Toolbar
		self.toolnext = self.builder.get_object('btn-next')
		self.toolnext.connect('clicked', self.play_next)

		self.toolprev = self.builder.get_object('btn-previous')
		self.toolprev.connect('clicked', self.play_prev)

		self.toolstop = self.builder.get_object('btn-stop')
		self.toolstop.connect('clicked', self.stop_play)

		self.toolplay = self.builder.get_object('btn-play')
		self.toolplay.connect('clicked', self.play_pause)

		self.toolSeekBar = self.builder.get_object('scl-position')
		self.toolSeekBar.connect('button-release-event', self.seek)
		self.toolSeekBar.connect('button-press-event', self.seekevent)

		self.toolVolume = self.builder.get_object('btn-volume')
		self.toolVolume.connect('value-changed', self.change_volume)

		#Text Displays
		self.titleText = self.builder.get_object('lbl-trkTitle')
		self.infoText = self.builder.get_object('lbl-trkMisc')
		self.lengthLabel = self.builder.get_object('lbl-length')
		self.elapsedLabel = self.builder.get_object('lbl-elapsed')

		#bottom toolbar
		barclr = self.builder.get_object('btn-tracklistClear')
		barclr.connect('clicked', self.clear_liststore)

		barshfl = self.builder.get_object('btn-tracklistShuffle')
		if self.shuffle == True:
			barshfl.set_active(True)
		barshfl.connect('clicked', self.shuffleliststore)

		barrpt = self.builder.get_object('btn-tracklistRepeat')
		if self.repeat == True:
			barrpt.set_active(True)
		barrpt.connect('toggled', self.setrepeat)

		#listview
		self.iconoListView = IconoListView()
		self.iconoListView.get_sw().get_child().connect('row-activated', self.on_activated)
		#self.iconoListView.get_sw().get_child().connect('button-press-event', self.on_right_click)
		vbox2 = self.builder.get_object('vbox2')
		vbox2.add(self.iconoListView.get_sw())
		vbox2.reorder_child(self.iconoListView.get_sw(), 1)
		if os.path.exists(sopranoGlobals.TREE_DATA):
			GObject.idle_add(self.iconoListView.load_shelf, sopranoGlobals.TREE_DATA)

		#combobox
		self.hCombo = HeaderedComboBox()
		self.hCombo.connect("changed", self.on_name_combo_changed)		

		self.builder.get_object('box-combo-explorer').add(self.hCombo)
		
		GObject.idle_add(self.setup_explorer)
		GObject.idle_add(self.cover_update)
		self.window.show_all()
		if self.currentview == 'playlist':
			menuvplist.set_active(True)
			self.to_playlist_mode()
		elif self.currentview == 'mini':
			menuvmini.set_active(True)
			self.to_mini_mode()
		#Notebook
		self.notebook = self.builder.get_object('notebook-explorer')

	def update_tray_icon(self, enabled=True):
		if enabled:
			try:	self.tray.myStatusIcon.set_visible(True)
			except: self.tray.ind.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
		elif not enabled:
			try:	self.tray.myStatusIcon.set_visible(False)
			except: self.tray.ind.set_status(AppIndicator3.IndicatorStatus.PASSIVE)
			

	def show_pref_win(self, widget=None):
		newWin = SopranoPrefWin(self.showtrayicon, self.closetotray, self.window)
		newWin.win.set_transient_for(self.window)
		newWin.win.show_all()
		newWin.win.connect("destroy", self.pref_win_closed)


	def pref_win_closed(self, widget):
		currentpage = self.notebook.get_current_page()
		currentactive = self.hCombo.get_active()
		self.clear_notebook()
		self.setup_explorer()
		self.notebook.set_current_page(currentpage + widget.change)
		self.hCombo.set_active(currentactive + widget.change)
		self.showtrayicon = widget.traycheckbox.get_active()
		if self.showtrayicon:
			self.closetotray = widget.closecheckbox.get_active()
		else:
			self.closetotray = False
		self.update_tray_icon(self.showtrayicon)

	def toggle_window(self, justShow=True):
		if self.window.get_property("visible") and not justShow == True:
			self.window.hide()
			#self.trayshowhide.set_label("Show")
		else:
			self.window.show()
			#self.trayshowhide.set_label("Hide")

	def pre_exit(self, widget, var):
		if widget == self.window and self.closetotray:
			self.window.hide()
			return True
		else:
			self.on_exit(widget)

	def on_exit(self, widget):
		#hide window and tray icon first to give appearence of instant close
		self.window.hide()
		self.tray = None
		if self.currentview != 'mini':
			size = self.window.get_size()
			winheight = size[1]#.height
			winwidth = size[0]#.width
		else:
			winheight = self.winheight
			winwidth = self.winwidth
		self.settings.write_settings([self.currentview, winwidth, winheight ,self.notebook.get_current_page()+1, self.shuffle, self.repeat, self.showtrayicon, self.closetotray])
		self.iconoListView.save_shelf(sopranoGlobals.TREE_DATA)
		Gtk.main_quit()

	def addFolderExplorer(self, station):		
		explorer = IconoTreeFile(station[1], sopranoGlobals.FILE_FORMATS)
		audioFolderlist = settings.IconoPrefs(sopranoGlobals.EXPLORER_DATA)
		audioFolderlist.add_radio(station)
		self.setup_explorer_page(self.notebook, explorer.get_sw(), self.hCombo, [len(audioFolderlist.get_radioStations()), 0, station[0], sopranoGlobals.FOLDERPB], self.notebook.get_n_pages()-2)
		#Update the audioCD and Radio Indexes
		model = self.hCombo.get_model()
		length = len(model)
		for i in range(1,3):
			iter = model.get_iter(length-i)
			model.set_value(iter, 0, length-(1+i))

	def clear_notebook(self, widget=None):
		for i in range(self.notebook.get_n_pages(), 0, -1):
			self.notebook.remove_page(i-1)
		self.hCombo.get_model().clear()

	def delFolderExplorer(self, station):
		self.clear_notebook()
		audioFolderlist = settings.IconoPrefs(sopranoGlobals.EXPLORER_DATA)
		audioFolderlist.delete_radio(station)
		self.setup_explorer()
		

	#explorer and combobox Handlers
	def setup_explorer(self, widget=None):
		self.hCombo.add_entry(None, 1, "<b>Folders</b>", None, -1)

		explorer = IconoTreeFile('/', sopranoGlobals.FILE_FORMATS)
		self.setup_explorer_page(self.notebook, explorer.get_sw(), self.hCombo, [self.notebook.get_n_pages(), 0, "Root", sopranoGlobals.FOLDERPB])

		audioFolderlist = settings.IconoPrefs(sopranoGlobals.EXPLORER_DATA)
		for key, value in audioFolderlist.get_radioStations().items():
			explorer = IconoTreeFile(value, sopranoGlobals.FILE_FORMATS)	
			self.setup_explorer_page(self.notebook, explorer.get_sw(), self.hCombo, [self.notebook.get_n_pages(), 0, key, sopranoGlobals.FOLDERPB])
		#aCdTree = IconoAudioCD()
		#self.setup_explorer_page(self.notebook, aCdTree.get_sw(), self.hCombo, [self.notebook.get_n_pages(), 0, "<b>Audio CD</b>", sopranoGlobals.TRACKPB])		
		self.setup_explorer_page(self.notebook, self.aRadio.get_sw(), self.hCombo, [self.notebook.get_n_pages(), 0, "<b>Radio</b>", sopranoGlobals.RADIOPB])

		self.medialib = IconoMediaLibrary(self.SopranoDB)
		self.setup_explorer_page(self.notebook, self.medialib.get_sw(), self.hCombo, [self.notebook.get_n_pages(), 0, "<b>Library</b>", sopranoGlobals.USERSPB])

		self.notebook.set_current_page(self.defaultexplorer)
		self.hCombo.set_active(self.defaultexplorer)		

	def setup_explorer_page(self, notebook, widget, combo, arglist, insertHere=-1):
		combo.add_entry(arglist[0], arglist[1], arglist[2], arglist[3], insertHere)
		label = Gtk.Label(arglist[2])
		notebook.insert_page(widget, label, insertHere)
		notebook.show_all()

	def on_name_combo_changed(self, combo):
		tree_iter = combo.get_active_iter()
		if tree_iter != None:
			model = combo.get_model()
			index, row_id, name = model[tree_iter][:3]
			if row_id == 1:
				combo.set_active_iter(model.iter_next(tree_iter)) # if they try and select a header move to the real entry below instead
			else:
				self.notebook.set_current_page(index)

	#ListStore Handlers
	def on_activated(self, widget, row, col):
		model = widget.get_model()
		text = model[row][7]
		GObject.idle_add(self.playitem, text)
		self.iconoListView.set_playmark(row)

	#View Menu Handlers
	def to_full_mode(self, unused=None):
		self.window.resize(self.winwidth,self.winheight)
		self.builder.get_object('pan-main').get_child1().show()
		self.builder.get_object('statusbar').show()
		self.builder.get_object('box-btn-tracklist').show()
		self.iconoListView.get_sw().show()
		self.currentview = 'full'

	def to_mini_mode(self, unused=None):
		self.builder.get_object('pan-main').get_child1().hide()
		self.builder.get_object('statusbar').hide()
		self.builder.get_object('box-btn-tracklist').hide()
		self.iconoListView.get_sw().hide()
		self.window.resize(600, 150)
		self.currentview = 'mini'

	def to_playlist_mode(self, unused=None):
		self.to_full_mode(None)	
		self.window.resize(self.winwidth, self.winheight)
		self.builder.get_object('pan-main').get_child1().hide()
		self.currentview = 'playlist'

	#Bottom Toolbar Handlers#
	def clear_liststore(self, action):
		GObject.idle_add(self.stop_play)
		self.iconoListView.return_model().clear()

	def shuffleliststore(self, button):
		self.shuffle = not(self.shuffle)

	def setrepeat(self, arg1):
		self.repeat = not(self.repeat)

	#Data Display Handlers
	def update_time_items(self):
		if (self.player.get_state() == Gst.State.PLAYING):
			if not(self.seekingnow):
				self.toolSeekBar.set_value(self.player.track_percent())
			self.elapsedLabel.set_text(self.player.get_trackposition())
			self.lengthLabel.set_text('/' + self.player.get_tracklength())
		return True

	def update_labels(self, title, artist, album):
		self.titleText.set_text(title)
		self.infoText.set_text("By " + artist + " from " + album)

	def clear_labels(self):
		self.titleText.set_text("Soprano Audio Player")
		self.infoText.set_text("...One Goal, Be Epic")
		self.lengthLabel.set_text("")
		self.elapsedLabel.set_text("")

	def cover_update(self):
		filepath = self.player.get_track()
		if filepath != None:
			data = self.taglookup.getTrackType(filepath)
		try: artist = data[3].replace(' ','%20')
		except: artist = ""
		try: album = data[4].replace(' ','%20')
		except: album = ""

		coverFetch = getCover(artist, album, filepath)
		img = coverFetch.run()
		coverart = self.builder.get_object('img-cover')
		coverart.set_from_pixbuf(img.scale_simple(100,100,GdkPixbuf.InterpType.BILINEAR))

	#Play Handlers
	def on_message(self, bus, message):
		self.play_next()

	def seekevent(self, widget, event):
		self.seekingnow = True

	def seek(self, widget, test):
		self.seekingnow = False
		self.player.seek(widget.get_value())

	def change_volume(self, widget, volume):
		self.player.change_volume(volume)

	def play_prev(self, widget=None):
		for x in range(1,len(self.iconoListView.return_model())):
			if self.iconoListView.return_model()[x][0] == 'media-playback-start':
				GObject.idle_add(self.playitem, self.iconoListView.return_model()[x-1][7])
				self.iconoListView.set_playmark(x-1)
				break

	def play_next(self, widget=None):
		listlength = len(self.iconoListView.return_model())
		if self.shuffle:
			import random
			arand = random.randrange(0, listlength)
			self.iconoListView.set_playmark(arand)
			self.iconoListView.get_sw().get_child().scroll_to_cell(arand)
			GObject.idle_add(self.playitem, self.iconoListView.return_model()[arand][7])
			return
		for x in range(0, listlength):
			#if there on the last track, and they press next without repeat enabled, do nothing
			if x == listlength-1 and not(self.repeat) and widget == self.toolnext:
				break
			#if the last track finished without repeat enabled, stop playing
			elif x == listlength-1 and not(self.repeat) and widget != self.toolnext:
				GObject.idle_add(self.stop_play)
				break
			#if there on the last track and repeat is enabled go back to the first track
			elif x == listlength-1 and self.repeat:
				self.iconoListView.set_playmark(0)
				self.iconoListView.get_sw().get_child().scroll_to_cell(0)
				GObject.idle_add(self.playitem, self.iconoListView.return_model()[0][7])
				break
			#if not the last track, just find the playmark and play the track below
			if self.iconoListView.return_model()[x][0] == 'media-playback-start':
				self.iconoListView.set_playmark(x+1)
				self.iconoListView.get_sw().get_child().scroll_to_cell(x+1)
				GObject.idle_add(self.playitem, self.iconoListView.return_model()[x+1][7])
				break

	def playitem(self, filepath):
		self.player.stop_play()
		self.player.set_track(filepath)
		self.player.play_item()
		data = self.taglookup.getTrackType(filepath)
		#print(data)
		if data != False:
			self.update_labels(str(data[2]), str(data[3]), str(data[4]))

			#Notifications
			self.notification.update (str(data[2]), str(data[3]), "media-playback-start")
			self.notification.show()
			#set Sound Menu Data
			self.sopranompris.set_metadata(str(data[2]), str(data[3]), str(data[4]), "file://" + sopranoGlobals.CACHEFILE)
			self.sopranompris.signal_playing()

			self.toolSeekBar.set_sensitive(True)
			toolplayimg = self.builder.get_object('image3')
			toolplayimg.set_from_icon_name('media-playback-pause', Gtk.IconSize.LARGE_TOOLBAR)
			GObject.idle_add(self.cover_update)
		else:
			self.clear_labels()
			self.play_next()

	def stop_play(self, *args):
		self.player.stop_play()
		self.iconoListView.clear_playmark()
		self.clear_labels()
		self.toolSeekBar.set_sensitive(False)
		self.toolSeekBar.set_value(0)
		toolplayimg = self.builder.get_object('image3')
		toolplayimg.set_from_icon_name('media-playback-start', Gtk.IconSize.LARGE_TOOLBAR)
		GObject.idle_add(self.cover_update)

	def play_pause(self, filepath=None):
		#print(self.player.get_state())
		toolplayimg = self.builder.get_object('image3')
		if (self.player.get_state() == Gst.State.PLAYING):
			if self.player.get_track()[:7] == 'http://' or self.player.get_track()[:6] == 'mms://':
				self.player.stop_play()
				print("Radio Stop")
			else:
				self.player.pause_item()
			toolplayimg.set_from_icon_name('media-playback-start', Gtk.IconSize.LARGE_TOOLBAR)
			#self.trayplaypause.set_label("Play")			
		elif (self.player.get_state() == Gst.State.PAUSED):
			self.player.play_item()
			toolplayimg.set_from_icon_name('media-playback-pause', Gtk.IconSize.LARGE_TOOLBAR)
			#self.trayplaypause.set_label("Pause")			
		else:#if os.path.isfile(filepath):
			selected = self.iconoListView.get_sw().get_child().get_selection()
			if selected.get_selected_rows()[1] != []:
				modeliter = self.iconoListView.return_model().get_iter(selected.get_selected_rows()[1][0])
			elif self.player.get_state() == Gst.State.NULL and self.iconoListView.get_playmark() != None:
				modelrow = self.iconoListView.get_playmark()
				modeliter = self.iconoListView.return_model().get_iter(modelrow)
			elif self.iconoListView.return_model().get_iter_first() != None:
				modeliter = self.iconoListView.return_model().get_iter_first()

			try: filepath = self.iconoListView.return_model().get_value(modeliter, 7)
			except: return
			#self.trayplaypause.set_label("Pause")			
			GObject.idle_add(self.playitem, filepath)
			self.iconoListView.set_playmark(modeliter)
			toolplayimg.set_from_icon_name('media-playback-pause', Gtk.IconSize.LARGE_TOOLBAR)
			GObject.idle_add(self.cover_update)
import sys
import fcntl
LOCK_PATH = os.path.join(os.path.expanduser('~'), '.sopranolock')
fd = open(LOCK_PATH, 'w')
fcntl.lockf(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
app = SopranoApp()
if __name__ == '__main__':
	Gtk.main()
