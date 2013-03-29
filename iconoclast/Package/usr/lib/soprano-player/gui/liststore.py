#got_data_cb needs to be rewritten aswell as improve internal drag-drop performance, possibly do manipulation in a structure before updating the treeview
#init function needs rewrite too
#(C) 2011 Mike Morley

from gi.repository import Gtk, GdkPixbuf, Gdk, GObject
import os.path
try: import cPickle as pickle
except: import pickle
from music.tagreading import TrackMetaData

class IconoListView():
	def __init__(self):
		self.sw = Gtk.ScrolledWindow()
		self.trackparser = TrackMetaData()

		builder = Gtk.Builder()
		filename = os.path.join('data', 'treeview.ui')
		builder.add_from_file(filename)
		self.abox = builder.get_object('treeview1')
		self.abox.set_fixed_height_mode(False)

		self.abox.set_search_column(1)
		self.abox.get_selection().set_mode(Gtk.SelectionMode.MULTIPLE)
		trackCol = builder.get_object('trackCol')
		titleCol = builder.get_object('titleCol')
		artistCol = builder.get_object('artistCol')
		albumCol = builder.get_object('albumCol')
		lengthCol = builder.get_object('lengthCol')
		genreCol = builder.get_object('genreCol')
		pathCol = builder.get_object('pathCol')

		#need to figure a working sorting function
		#self.abox.get_model().set_sort_func(1, self.tracknumsortfunc, None)

		trackCol.set_sort_column_id(1)
		titleCol.set_sort_column_id(2)
		artistCol.set_sort_column_id(3)
		albumCol.set_sort_column_id(4)
		lengthCol.set_sort_column_id(5)
		genreCol.set_sort_column_id(6)

		#anEntry = Gtk.TargetEntry.new("abox",Gtk.TargetFlags.SAME_WIDGET, 10)
		self.abox.enable_model_drag_source(Gdk.ModifierType.BUTTON1_MASK, [('TREE_MODEL_ROW', Gtk.TargetFlags.SAME_WIDGET, 0),], Gdk.DragAction.COPY|Gdk.DragAction.MOVE)
		#self.abox.drag_source_set(Gdk.ModifierType.BUTTON1_MASK, [anEntry], 0)
		self.abox.enable_model_drag_dest([], Gdk.DragAction.COPY|Gdk.DragAction.DEFAULT)
		#self.abox.drag_dest_set(0, [], 0)
		self.abox.connect('drag_motion', self.drag_motion_cb)
		self.abox.connect('drag_drop', self.drop_cb)
		self.abox.connect('drag_data_received', self.got_data_cb)

		self.abox.connect("drag_data_get", self.drag_data_get_data)

		self.abox.connect('button_press_event', self.on_button_press)
		self.abox.connect('button_release_event', self.on_button_release)
		self.defer_select=False
		self.sw.add(self.abox)

	def tracknumsortfunc(self,model, row1, row2, user_data):
		if (model.get_value(row1, 3) == model.get_value(row2, 3)) and (model.get_value(row1, 4) == model.get_value(row2, 4)):
			#print("Same Band! and Same Album!")
			#print(model.get_value(row1, 3), model.get_value(row1, 4))
			#print cmp(model[row1][3], model[row2][3])
			if (model.get_value(row1, 1) <= model.get_value(row2, 1)):
				print("0")
				return 0
				#print(model.get_value(row1, 1))
				#model.swap(row1, row2)
			else:
				print("-1")
				return -1
				#model.swap(row2, row1)
		#else:
			#print cmp(model[row1][3], model[row2][3])

	def drag_data_get_data(self, treeview, context, selection, target_id, etime):
		treeselection = treeview.get_selection()
		model, paths = treeselection.get_selected_rows()
		Gtk.tree_set_row_drag_data(selection, treeview.get_model(), paths[0])		

	def drag_motion_cb(self, senderID, context, x, y, time):
		Gdk.drag_status(context, Gdk.DragAction.COPY, time)
		if self.abox.get_dest_row_at_pos(x, y) == None:
			return True
		path, pos = self.abox.get_dest_row_at_pos(x, y)
		self.abox.set_drag_dest_row(path, pos)
		return True

	def got_data_cb(self, windowid, context, x, y, data, info, time):
		treeselection = windowid.get_selection()
		model, paths = treeselection.get_selected_rows()
		refs = []
		for path in paths:
    			refs.append(Gtk.TreeRowReference.new(model, path))
		#refs = [path.append(Gtk.TreeRowReference.new(model, path)) for path in paths# different way of wording the above
		destpath = windowid.get_dest_row_at_pos(x, y)
		if destpath:
			destpath, position = destpath
			destiter = model.get_iter(destpath)
		else:
			#print "outside the rows"
			try: destiter = model.get_iter(len(model))
			except: destiter = False
		#handle internal drag/drops here
		sourceWidget = Gtk.drag_get_source_widget(context)		
		if sourceWidget == windowid:
			#print "internals"			
			if not destpath in paths:
				if (position == Gtk.TreeViewDropPosition.BEFORE):# or position == Gtk.TreeViewDropPosition.INTO_OR_BEFORE):
					print "into or before"
					for currentref in refs:
						model.move_before(model.get_iter(currentref.get_path()), destiter)
				else:
					print "else"
					for currentref in reversed(refs):
						model.move_after(model.get_iter(currentref.get_path()), destiter)
		else:

			##detach model improves performance but causes flicker # MAKES MIKE A SAD PANDA
			windowid.set_model(None)
			#fuckin file managers handling differently :( nautilus sends plaintext, but pcman sends uris
			tempArray = []
			if data.get_text():
				for i in data.get_text().splitlines():
					tempArray.append(i)
			else:
				for i in data.get_uris():
					tempArray.append(i)
			from time import time as systime
			systime1 = systime()
			#got the data now split it up
			for i in tempArray:
				i = i.replace('file://','').replace('%20',' ') #simple but is way too slow
				if os.path.isdir(i):
					for root, dirs, files in os.walk(i):
						while Gtk.events_pending():
	    						Gtk.main_iteration()
						for name in files:
							#print(name)
							self.add_row(os.path.join(root, name), model, destiter)
				else:
					self.add_row(i, model, destiter)
			##reattach model
			print("%s%f%s%i" % ("Add Operation took ",systime() - systime1," Items:", len(model)))
			del(systime)
			windowid.set_model(model)

		context.finish(True, False, time)

	def drop_cb(self, windowid, context, x, y, time):
		# Some data was dropped, get the data
		windowid.drag_get_data(context, context.list_targets()[-1], time)
		return True

	def add_row(self, action, widget, destiter):
		x = self.trackparser.getTrackType(action)
		#x = [None, 1,"Title","Artist","Album","400","Genre","/aidscake"]
		#x.insert(0, None)
		if destiter == False and x != False:
			widget.append(x)
		elif x != False:
			widget.insert_after(destiter, x)

	def load_shelf(self, path):
		model = self.return_model()
		self.abox.set_model(None)
		db = pickle.load(open(path, "rb"))
		for i in range(0, len(db), 8):
			templist = []
			for j in range(0, 8):
				templist.append(db[i+j])
			while Gtk.events_pending():
				Gtk.main_iteration()
			model.append(templist)
		self.abox.set_model(model)

	def save_shelf(self, path):
		count = 0
		settings = []
		def writeouttree(model, path, iter, data):
			for i in range(0, 8):
				settings.append(model.get_value(iter, i))

		self.return_model().foreach(writeouttree, None)
		db = pickle.dump(settings, open(path, "wb" ),2)

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
		if event.button == 3:
			self.menu = Gtk.Menu()
			aMenuitem = Gtk.MenuItem()
			aMenuitem.set_label("Remove")
			aMenuitem.connect("activate", self.remove_rows, widget)

			self.menu.append(aMenuitem)
			self.menu.show_all()
			self.menu.popup( None, None, None, None, event.button, event.time)
			return True

	def on_button_release(self, widget, event):
		# re-enable selection
		widget.get_selection().set_select_function(lambda *ignore: True, None)

		target = widget.get_path_at_pos(int(event.x), int(event.y))	
		if (self.defer_select and target and self.defer_select == target[0] and not (event.x==0 and event.y==0)): # certain drag and drop
   				widget.set_cursor(target[0], target[1], False)

	def clear_playmark(self):
		for i in range(0, len(self.return_model())):
			self.return_model().set_value(self.return_model().get_iter(i), 0, '')

	def set_playmark(self, row):
		self.clear_playmark()		
		try: self.return_model().set_value(row, 0, 'media-playback-start')
		except: self.return_model().set_value(self.return_model().get_iter(row), 0, 'media-playback-start')

	def get_playmark(self):
		for i in range(0, len(self.return_model())):
			tempiter = self.return_model().get_iter(i)
			if self.return_model().get_value(tempiter, 0) == 'media-playback-start':
				return i
				break
		return None

	def get_sw(self):
		return self.sw

	def return_model(self):
		return self.abox.get_model()

	def remove_rows(self, widget, treeview):
		model, selected = self.abox.get_selection().get_selected_rows()
		treeview.set_model(None)
		for i in reversed(selected):
			tempiter = model.get_iter(i)
			"""if model.get_value(tempiter, 0) == 'media-playback-start':
				GObject.idle_add(self.stop_play)"""
			model.remove(tempiter)
		treeview.set_model(model)

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
