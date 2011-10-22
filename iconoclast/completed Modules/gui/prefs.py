from gi.repository import Gtk, GdkPixbuf
import PrefWin

def main():
	#Page 1
	vbox = Gtk.VBox()
	hbox = Gtk.HBox()
	alabel = Gtk.Label("Show Tray Icon")
	traycheckbox = Gtk.CheckButton()
	hbox.pack_start(alabel, True, False, 0)
	hbox.pack_end(traycheckbox, True, False, 0)

	categorys = Gtk.ListStore(GdkPixbuf.Pixbuf, str, str)
	column = Gtk.TreeViewColumn()
	title = Gtk.CellRendererText()
	piccy = Gtk.CellRendererPixbuf()
	column.pack_start(piccy, True)
	column.pack_start(title, True)
	column.add_attribute(piccy, "pixbuf", 0)
	column.add_attribute(title, "text", 1)
	tree = Gtk.TreeView(categorys)
	tree.set_headers_visible(False)
	tree.append_column(column)

	vbox.pack_start(tree, True, True, 0)
	vbox.pack_start(hbox, False, True, 0)
	
	win = PrefWin.PrefWin()
	win.create_category("Desktop", "folder", vbox)
	win.connect("delete_event", Gtk.main_quit)
	if __name__ == '__main__':
		Gtk.main()
main()
