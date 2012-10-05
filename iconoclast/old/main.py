from gi.repository import Gtk, GdkPixbuf, Gdk, Gio, GObject, AppIndicator3
import os
import gst
import random

from aboutbox import aboutBoxShow
from tagreading import TrackMetaData

from propertreefilebrowser import IconoTreeFile
from liststore import IconoListView

def widget_hide(widget, button):
    widget.hide()

class BuilderApp:
	def __init__(self):

		#Window Creation
		self.builder = Gtk.Builder()
		filename = os.path.join('', 'MainWindow.glade')        

		self.builder.add_from_file(filename)
		self.builder.connect_signals(self)	

		self.window = self.builder.get_object('win-main')
		self.window.set_default_size(900, 550)
		self.window.connect('destroy', lambda x: Gtk.main_quit())
		self.window.show_all()

		#Quit, About Menus
		self.menuaqt = self.builder.get_object('menu-quit')
		self.menuaqt.connect('activate', lambda x: Gtk.main_quit())

		self.menuabt = self.builder.get_object('menu-about')
		self.menuabt.connect('activate', lambda x: aboutBoxShow(self.window))

		#listview
		self.iconoListView = IconoListView()
		vbox2 = self.builder.get_object('vbox2')
		vbox2.add(self.

		#notebook and contents
		self.explorer2 = IconoTreeFile('/media/Media/Music', {'.mp3','.ogg','.oga','.wma','.flac','.m4a','.mp4'})

		self.notebook = self.builder.get_object('notebook-explorer')
		self.notebook.add(self.explorer2.get_sw())

		self.notebook.show_all()

def main(iconoclast=None):
	app = BuilderApp()	

	if __name__ == '__main__':
		Gtk.main()

main()
