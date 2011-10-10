from gi.repository import Gtk, GdkPixbuf, Gdk
import os

def got_data_cb(windowid, context, x, y, data, info, time):
	# Got data.
	tempArray = data.get_text().splitlines()
	for i in tempArray:
		i = i.replace('file://','')
		i = i.replace('%20',' ')
		print i
		windowid.get_model().append([i])
	context.finish(True, False, time)

def drop_cb(windowid, context, x, y, time):
	# Some data was dropped, get the data
	windowid.drag_get_data(context, context.list_targets()[-1], time)
	return True

def main():
	win = Gtk.Window()
	win.connect('destroy', lambda x: Gtk.main_quit())
	win.set_default_size(450, 400)

	amodel = Gtk.ListStore(str)
	column = Gtk.TreeViewColumn()
	title = Gtk.CellRendererText()
	column.pack_start(title, True)
	column.add_attribute(title, "text", 0)
	atree = Gtk.TreeView(amodel)
	atree.append_column(column)

	builder = Gtk.Builder()
	filename = os.path.join('', 'treeview.ui')
	builder.add_from_file(filename)
	abox = builder.get_object('treeview1')
	abox.set_reorderable(True)

	atree.drag_dest_set(0, [], 0)
	atree.connect('drag_motion', lambda v,w,x,y,z: True)
	atree.connect('drag_drop', drop_cb)
	atree.connect('drag_data_received', got_data_cb)
	
	win.add(atree)
	win.show_all()

	if __name__ == '__main__':
		Gtk.main()

main()