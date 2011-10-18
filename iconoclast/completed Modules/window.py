from gi.repository import Gtk
import os

class IconoWindow(Gtk.Window):
	def __init__(self, width, height):
		Gtk.Window.__init__(self)
		
		builder = Gtk.Builder()
		filename = os.path.join('builder', 'MainWindow.glade')
		builder.add_from_file(filename)
		builder.connect_signals(self)

		self = builder.get_object('win-main')
		self.set_default_size(width,height)
		self.connect('destroy', lambda x: self.on_exit())
		self.show_all()

	def toggle(self, widget=None):
		if self.get_property("visible"):
			self.hide()
		else:
			self.show()

moo = IconoWindow(900,550)
Gtk.main()
