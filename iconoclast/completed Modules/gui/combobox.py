#Icon Combobox 
#Author: Mike Morley (mmorely19@gmail.com)
from gi.repository import Gtk, GdkPixbuf

class HeaderedComboBox(Gtk.ComboBox):
	def __init__(self):
		Gtk.ComboBox.__init__(self)

		self.name_store = Gtk.ListStore(int, int, str, GdkPixbuf.Pixbuf)
		self.set_model(self.name_store)

		renderertext = Gtk.CellRendererText()
		self.pack_end(renderertext, True)
		self.add_attribute(renderertext, "markup", 2) # use renderertext with "text" from name_store model data at 1

		rendererpb = Gtk.CellRendererPixbuf()
		self.pack_start(rendererpb, False)
		self.add_attribute(rendererpb, "pixbuf", 3) # use rendererpb with a "pixbuf" from name_store model data at 2

		self.set_entry_text_column(1)

	def add_entry(self, index, header, Name, pixbuf=None, insertHere=None):
		if insertHere == -1:
			self.name_store.append([index, header, Name, pixbuf])
		else:
			self.name_store.insert(insertHere+1, [index, header, Name, pixbuf])

"""#testing and debugging bits below
folderpb = Gtk.IconTheme.get_default().load_icon('folder', 16, Gtk.IconLookupFlags.FORCE_SIZE)
win = Gtk.Window()
cbbox = HeaderedComboBox()

cbbox.add_entry(1, 1, "<b>Folders</b>", None)
cbbox.add_entry(1, 0, "Home", folderpb)
cbbox.add_entry(1, 0, "Media", folderpb)
cbbox.add_entry(1, 1, "<b>Library</b>", None)
cbbox.add_entry(1, 0, "Music", folderpb)

win.add(cbbox)
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()"""
