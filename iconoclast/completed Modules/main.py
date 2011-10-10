from gi.repository import Gtk, GdkPixbuf, Gdk, Gio, GObject, AppIndicator3
import os
import gst
import random

from gui.aboutbox import aboutBoxShow
from gui.music.tagreading import TrackMetaData
from gui.music.cdcover import getCover
from gui.combobox import HeaderedComboBox

from gui.propertreefilebrowser import IconoTreeFile
from gui.liststore import IconoListView

class BuilderApp:
	def __init__(self):
		#Window Creation
		self.builder = Gtk.Builder()
		filename = os.path.join('builder', 'MainWindow.glade')        

		self.builder.add_from_file(filename)
		self.builder.connect_signals(self)	

		self.window = self.builder.get_object('win-main')
		self.window.set_default_size(900, 550)
		self.window.connect('destroy', lambda x: Gtk.main_quit())

		#View Menu#
		self.menuvfull = self.builder.get_object('menu-mode-full')
		self.menuvfull.connect('activate', self.to_full_mode)

		self.menuvlean = self.builder.get_object('menu-mode-lean')
		self.menuvlean.connect('activate', self.to_lean_mode)

		self.menuvmini = self.builder.get_object('menu-mode-mini')
		self.menuvmini.connect('activate', self.to_mini_mode)

		self.menuvplist = self.builder.get_object('menu-mode-playlist')
		self.menuvplist.connect('activate', self.to_playlist_mode)

		#Quit, About Menus
		self.menuaqt = self.builder.get_object('menu-quit')
		self.menuaqt.connect('activate', lambda x: Gtk.main_quit())

		self.menuabt = self.builder.get_object('menu-about')
		self.menuabt.connect('activate', lambda x: aboutBoxShow(self.window))

		#listview
		self.iconoListView = IconoListView()
		vbox2 = self.builder.get_object('vbox2')
		vbox2.add(self.iconoListView.get_sw())
		vbox2.reorder_child(self.iconoListView.get_sw(), 1)

		#combobox
		folderpb = Gtk.IconTheme.get_default().load_icon('folder', 16, Gtk.IconLookupFlags.FORCE_SIZE)
		self.hCombo = HeaderedComboBox()
		self.hCombo.add_entry(1, "<b>Folders</b>", None)
		self.hCombo.add_entry(0, "Music", folderpb)
		cboxholder = self.builder.get_object('box-combo-explorer')
		cboxholder.add(self.hCombo.get_ref())

		#notebook and contents
		self.explorer2 = IconoTreeFile('/media/Media/Music', {'.mp3','.ogg','.oga','.wma','.flac','.m4a','.mp4'})

		self.notebook = self.builder.get_object('notebook-explorer')
		self.notebook.add(self.explorer2.get_sw())

		self.window.show_all()

	def to_full_mode(self, unused):
		self.window.resize(900, 550)
		self.builder.get_object('pan-main').get_child1().show()
		self.builder.get_object('statusbar').show()
		self.builder.get_object('box-btn-tracklist').show()
		self.iconoListView.get_sw().show()
		self.window.resize(900, 550)

	def to_lean_mode(self, unused):
		self.to_full_mode(None)	
		self.builder.get_object('box-btn-tracklist').hide()

	def to_mini_mode(self, unused):
		self.to_full_mode(None)	
		self.window.resize(600, 150)
		self.builder.get_object('pan-main').get_child1().hide()
		self.builder.get_object('statusbar').hide()
		self.builder.get_object('box-btn-tracklist').hide()
		self.iconoListView.get_sw().hide()

	def to_playlist_mode(self, unused):
		self.to_full_mode(None)	
		self.window.resize(600, 550)
		self.builder.get_object('pan-main').get_child1().hide()

	def cover_update(self, artist, album, filepath):
		coverFetch = getCover()
		img = coverFetch.returnCover(artist, album, filepath)
		coverart = self.builder.get_object('img-cover')
		coverart.set_from_pixbuf(img.get_pixbuf().scale_simple(100,100,GdkPixbuf.InterpType.BILINEAR))

def main(iconoclast=None):
	app = BuilderApp()
	app.cover_update('', '', '/media/Media/Music/Babyshambles/Down2 In Albion/2 - Fuck Forever.mp3')

	app.cover_update('symphony%20X', 'Iconoclast', '/media/Media/Music/Babyshambles/Down In Albion/2 - Fuck Forever.mp3')

	if __name__ == '__main__':
		Gtk.main()

main()
