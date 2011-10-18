from gi.repository import Gtk, GdkPixbuf, Gdk, GObject
import os.path
import cPickle as pickle
from music.tagreading import TrackMetaData

class IconoListView():
	def __init__(self):
		self.sw = Gtk.ScrolledWindow()

		builder = Gtk.Builder()
		filename = os.path.join('builder', 'treeview.ui')
		builder.add_from_file(filename)
		self.abox = builder.get_object('treeview1')
		self.abox.set_reorderable(True)
		self.abox.set_search_column(1)
		self.abox.get_selection().set_mode(Gtk.SelectionMode.MULTIPLE)
		acol1 = builder.get_object('trackCol')
		acol2 = builder.get_object('titleCol')
		acol3 = builder.get_object('artistCol')
		acol4 = builder.get_object('albumCol')
		acol5 = builder.get_object('lengthCol')
		acol6 = builder.get_object('genreCol')
		acol7 = builder.get_object('pathCol')

	       	acol1.set_sort_column_id(1)
		acol2.set_sort_column_id(2)
		acol3.set_sort_column_id(3)
		acol4.set_sort_column_id(4)
		acol5.set_sort_column_id(5)
		acol6.set_sort_column_id(6)

		self.sw.drag_source_set(0, [], 0)
		self.sw.drag_dest_set(0, [], 0)
		self.sw.connect('drag_motion', self.drag_motion_cb)
		self.sw.connect('drag_drop', self.drop_cb)
		self.sw.connect('drag_data_received', self.got_data_cb)
	
		self.sw.add(self.abox)

	def drag_motion_cb(self, wid, context, x, y, time):
		Gdk.drag_status(context, Gdk.DragAction.COPY, time)
		return True

	def drag_data_get_data(self, treeview, context, selection, target_id, etime):
		treeselection = treeview.get_selection()
		model, iter = treeselection.get_selected()
		data = model.get_value(iter, 0)
		selection.set(selection.target, 8, data)

	def add_row(self, action, widget):
		getmesumdatabruv = TrackMetaData()
		x = getmesumdatabruv.getTrackType(action)
		if x != False:
			x.insert(0, None)
			widget.append(x)

	def got_data_cb(self, windowid, context, x, y, data, info, time):
		# detach model for performance
		model = windowid.get_child().get_model()
		windowid.get_child().set_model(None)
		#fuckin file managers handling differently :( nautilus sends text, but pcman sends uris
		tempArray = []
		if data.get_text():
			for i in data.get_text().splitlines():
				tempArray.append(i)
		for i in data.get_uris():
			tempArray.append(i)
		#got the data now split it up
		for i in tempArray:
			i = i.replace('file://','').replace('%20',' ') #simple but was way too slow
			if os.path.isdir(i):
				for root, dirs, files in os.walk(i):
					for name in files:
						self.add_row(os.path.join(root, name), model)
			else:
				self.add_row(i, model)
		# reattach model
		windowid.get_child().set_model(model)
		context.finish(True, False, time)

	def drop_cb(self, windowid, context, x, y, time):
		# Some data was dropped, get the data
		windowid.drag_get_data(context, context.list_targets()[-1], time)
		return True

	def load_shelf(self, path):
		import cPickle as pickle
		model = self.return_model()
		self.abox.set_model(None)
		db = pickle.load(open(path, "rb"))
		for i in xrange(0, len(db), 8):
			templist = []
			for j in xrange(0, 8):
				#print i+j
				templist.append(db[i+j])
			#print templist
			model.append(templist)
		self.abox.set_model(model)
	
	def save_shelf(self, path):
		import cPickle as pickle
		count = 0
		settings = []
		def writeouttree(model, path, iter, data):
			for i in xrange(0, 8):
				settings.append(model.get_value(iter, i))
				
		self.return_model().foreach(writeouttree, None)
		db = pickle.dump(settings, open(path, "wb" ) )

	def get_sw(self):
		return self.sw

	def return_model(self):
		return self.abox.get_model()

"""def on_exit(sw):
	sw.save_shelf('/home/mike/Desktop/treedata.icono')
	Gtk.main_quit()

def main():
	win = Gtk.Window()
	sw = IconoListView()
	sw.load_shelf('/home/mike/Desktop/treedata.icono')

	win.connect('destroy', lambda x: on_exit(sw))
	win.set_default_size(550, 400)	
	win.add(sw.get_sw())
	win.show_all()

	if __name__ == '__main__':
		Gtk.main()

main()"""
