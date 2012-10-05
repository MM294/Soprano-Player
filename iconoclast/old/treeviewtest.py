from gi.repository import Gtk, GdkPixbuf, Gdk
import os
from tagreading import TrackMetaData

class IconoListView:
	def __init__(self):
		self.sw = Gtk.ScrolledWindow()

		builder = Gtk.Builder()
		filename = os.path.join('', 'treeview.ui')
		builder.add_from_file(filename)
		abox = builder.get_object('treeview1')
		abox.set_reorderable(True)
		abox.set_search_column(1)

		acol = builder.get_object('trackCol')
		acol2 = builder.get_object('titleCol')
		acol3 = builder.get_object('artistCol')
		acol4 = builder.get_object('albumCol')
		acol5 = builder.get_object('lengthCol')
		acol6 = builder.get_object('genreCol')

	       	acol.set_sort_column_id(1)
		acol2.set_sort_column_id(2)
		acol3.set_sort_column_id(3)
		acol4.set_sort_column_id(4)
		acol5.set_sort_column_id(5)
		acol6.set_sort_column_id(6)

		self.sw.drag_source_set(0, [], 0)
		self.sw.drag_dest_set(0, [], 0)
		self.sw.connect('drag_motion', lambda v,w,x,y,z: True)
		self.sw.connect('drag_drop', self.drop_cb)
		self.sw.connect('drag_data_received', self.got_data_cb)
	
		self.sw.add(abox)

	def drag_data_get_data(self, treeview, context, selection, target_id,
		                   etime):
		treeselection = treeview.get_selection()
		model, iter = treeselection.get_selected()
		data = model.get_value(iter, 0)
		selection.set(selection.target, 8, data)

	def add_row(self, action, widget):
			action = action.replace('%20',' ')
			getmesumdatabruv = TrackMetaData()
			x = getmesumdatabruv.getTrackType(action)		
			if x != False:
				x.insert(0, None)
				widget.get_child().get_model().append(x)

	def got_data_cb(self, windowid, context, x, y, data, info, time):
		# Got data.
		tempArray = data.get_text().splitlines()
		for i in tempArray:
			i = i.replace('file://','')
			self.add_row(i, windowid)
		context.finish(True, False, time)

	def drop_cb(self, windowid, context, x, y, time):
		# Some data was dropped, get the data
		windowid.drag_get_data(context, context.list_targets()[-1], time)
		return True

	def get_sw(self):
		return self.sw

def main():
	win = Gtk.Window()
	win.connect('destroy', lambda x: Gtk.main_quit())
	win.set_default_size(550, 400)

	sw = IconoListView()
	
	win.add(sw.get_sw())
	win.show_all()

	if __name__ == '__main__':
		Gtk.main()

main()
