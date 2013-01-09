#Preferences window
#Author: Mike Morley (mmorely19@gmail.com)
from gi.repository import Gtk, GdkPixbuf
import os

PREF_LOCATION='/home/mike/Desktop/Python/IconoClast/iconoclast/prefs.conf'

class PrefWin(Gtk.Window):
	def __init__(self):
		Gtk.Window.__init__(self, title="Preferences")
		self.connect('destroy', lambda x: self.destroy())
		self.set_default_size(450, 400)

		self.categorylist = []

		#create category treeview
		self.categorys = Gtk.ListStore(GdkPixbuf.Pixbuf, str)
		column = Gtk.TreeViewColumn()
		title = Gtk.CellRendererText()
		piccy = Gtk.CellRendererPixbuf()
		column.pack_start(piccy, True)
		column.pack_start(title, True)
		column.add_attribute(piccy, "pixbuf", 0)
		column.add_attribute(title, "text", 1)
		self.tree = Gtk.TreeView(self.categorys)
		self.tree.set_headers_visible(False)
		self.tree.append_column(column)
		self.tree.get_selection().connect('changed', self.on_activated)
		
		#create notebook
		self.notebook = Gtk.Notebook()
		self.notebook.set_show_tabs(False)	
		
		#create the Holding Pane
		self.pane = Gtk.Paned()
		self.pane.pack1(self.tree, resize=False, shrink=False)
		self.pane.pack2(self.notebook, shrink=False)
		self.pane.set_position(100)

		#Padding container
		paddingbox = Gtk.Box()
		paddingbox.pack_start(self.pane, expand=True, fill=True, padding=5)

		self.add(paddingbox)
		self.show_all()

	def create_category(self, name, icon, widgetpage):
		exists = 0
		for i in range(0, len(self.categorylist)):
			#print str(self.categorylist[i])
			if  self.categorylist[i] == name:
				print("oh shit already a category called this!")
				exists = 1
		if exists == 0:
			pic = Gtk.IconTheme.get_default().load_icon(icon, 32, Gtk.IconLookupFlags.FORCE_SIZE)
			self.categorys.append([pic, name])
			label = Gtk.Label(str(name))
			self.notebook.insert_page(widgetpage, label, -1)
			self.notebook.show_all()
			self.categorylist.append(name)

	def on_activated(self, arg1):
		modelvalue = self.categorys.get_value(self.tree.get_selection().get_selected()[1], 1)
		for i in range(0, self.notebook.get_n_pages()):
			if modelvalue == self.notebook.get_tab_label_text(self.notebook.get_nth_page(i)):
				self.notebook.set_current_page(i)

"""def main():
	abox = Gtk.Box()
	alabel = Gtk.Label("First Option!")
	acheckbox = Gtk.Switch()
	abox.pack_start(alabel, expand=True, fill=True, padding=5)
	abox.pack_start(acheckbox, expand=True, fill=True, padding=5)

	abox2 = Gtk.Box()
	alabel2 = Gtk.Label("Second Option!")
	acheckbox2 = Gtk.Switch()
	abox2.add(alabel2)
	abox2.add(acheckbox2)
	
	win = PrefWin()
	win.connect("delete_event", Gtk.main_quit)
	win.create_category("Desktop", "folder", abox)
	win.create_category("Network", "network", abox2)
	if __name__ == '__main__':
		Gtk.main()
main()"""
