#got_data_cb needs to be rewritten aswell as improve internal drag-drop performance, possibly do manipulation in a structure before updating the treeview
#init function needs rewrite too
from gi.repository import Gtk, GdkPixbuf, Gdk, GObject
import os.path
import cPickle as pickle
from music.tagreading import TrackMetaData

class IconoListView():
	def __init__(self):
		self.sw = Gtk.ScrolledWindow()

		builder = Gtk.Builder()
		filename = os.path.join('data', 'treeview.ui')
		builder.add_from_file(filename)
		self.abox = builder.get_object('treeview1')

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

		#anEntry = Gtk.TargetEntry.new("abox",Gtk.TargetFlags.SAME_WIDGET, 10)
		self.abox.enable_model_drag_source(Gdk.ModifierType.BUTTON1_MASK, [('TREE_MODEL_ROW', Gtk.TargetFlags.SAME_WIDGET, 0),], Gdk.DragAction.DEFAULT)
		#self.abox.drag_source_set(Gdk.ModifierType.BUTTON1_MASK, [anEntry], 0)
		self.abox.enable_model_drag_dest([], Gdk.DragAction.DEFAULT)
		#self.abox.drag_dest_set(0, [], 0)
		self.abox.connect('drag_motion', self.drag_motion_cb)
		self.abox.connect('drag_drop', self.drop_cb)
		self.abox.connect('drag_data_received', self.got_data_cb)

		self.abox.connect("drag_data_get", self.drag_data_get_data)

		self.abox.connect('button_press_event', self.on_button_press)
		self.abox.connect('button_release_event', self.on_button_release)
		self.defer_select=False
		self.sw.add(self.abox)

	def drag_data_get_data(self, treeview, context, selection, target_id, etime):
		treeselection = treeview.get_selection()
        	model, paths = treeselection.get_selected_rows()
		Gtk.tree_set_row_drag_data(selection, treeview.get_model(), paths[0])		

	def drag_motion_cb(self, wid, context, x, y, time):
		Gdk.drag_status(context, Gdk.DragAction.COPY, time)
		return True

	def got_data_cb(self, windowid, context, x, y, data, info, time):
		treeselection = windowid.get_selection()
		model, paths = treeselection.get_selected_rows()
		destpath = windowid.get_dest_row_at_pos(x, y)
		if destpath:
			destpath, position = destpath
			destiter = model.get_iter(destpath)
		else:
			try: destiter = model.get_iter(len(model))
			except: destiter = False
		#handle internal drag/drops here, disabled atm
		sourceWidget = Gtk.drag_get_source_widget(context)
		if sourceWidget == windowid:	
			#print "internals"			
			if not destpath in paths:
				if (position == Gtk.TreeViewDropPosition.BEFORE or position == Gtk.TreeViewDropPosition.INTO_OR_BEFORE):
					for path in paths:
						model.move_before(model.get_iter(path), destiter)
				else:
					for path in reversed(paths):
						model.move_after(model.get_iter(path), destiter)
		else:
			##detach model improves performance but causes flicker
			windowid.set_model(None)
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
						#while Gtk.events_pending():
	    						#Gtk.main_iteration()
						for name in files:
							self.add_row(os.path.join(root, name), model, destiter)
				else:
					self.add_row(i, model, destiter)
			##reattach model
			windowid.set_model(model)
		context.finish(True, False, time)

	def drop_cb(self, windowid, context, x, y, time):
		# Some data was dropped, get the data
		windowid.drag_get_data(context, context.list_targets()[-1], time)
		return True

	def add_row(self, action, widget, destiter):
		getmesumdatabruv = TrackMetaData()
		x = getmesumdatabruv.getTrackType(action)
		if x != False:
			x.insert(0, None)
			if destiter == False:
				widget.append(x)
			else:
				widget.insert_before(destiter, x)

	def load_shelf(self, path):
		import cPickle as pickle
		model = self.return_model()
		self.abox.set_model(None)
		db = pickle.load(open(path, "rb"))
		for i in xrange(0, len(db), 8):
			templist = []
			for j in xrange(0, 8):
				templist.append(db[i+j])
			while Gtk.events_pending():
				Gtk.main_iteration()
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

	def on_button_press(self, widget, event):
		# Here we intercept mouse clicks on selected items so that we can
		# drag multiple items without the click selecting only one
		target = widget.get_path_at_pos(int(event.x), int(event.y))
		if (target 
		   and event.type == Gdk.EventType.BUTTON_PRESS
		   and not (event.get_state() & (Gdk.ModifierType.CONTROL_MASK|Gdk.ModifierType.SHIFT_MASK))
		   and widget.get_selection().path_is_selected(target[0])):
			   # disable selection
			   widget.get_selection().set_select_function(lambda *ignore: False, None)
			   self.defer_select = target[0]

	def on_button_release(self, widget, event):
		# re-enable selection
		widget.get_selection().set_select_function(lambda *ignore: True, None)

		target = widget.get_path_at_pos(int(event.x), int(event.y))	
		if (self.defer_select and target and self.defer_select == target[0] and not (event.x==0 and event.y==0)): # certain drag and drop
   				widget.set_cursor(target[0], target[1], False)

	def clear_playmark(self):
		for i in xrange(0, len(self.return_model())):
			self.return_model().set_value(self.return_model().get_iter(i), 0, '')

	def set_playmark(self, row):
		self.clear_playmark()		
		try: self.return_model().set_value(row, 0, 'media-playback-start')
		except: self.return_model().set_value(self.return_model().get_iter(row), 0, 'media-playback-start')

	def get_sw(self):
		return self.sw

	def return_model(self):
		return self.abox.get_model()

"""def on_exit(sw):
	sw.save_shelf(os.path.join(os.path.expanduser('~'), '.config/sopranoplayer/treedata.icono'))
	Gtk.main_quit()

def main():
	win = Gtk.Window()
	sw = IconoListView()
	sw.load_shelf(os.path.join(os.path.expanduser('~'), '.config/sopranoplayer/treedata.icono'))

	win.connect('destroy', lambda x: Gtk.main_quit())
	win.set_default_size(550, 400)	
	win.add(sw.get_sw())
	win.show_all()

	if __name__ == '__main__':
		Gtk.main()

main()"""
