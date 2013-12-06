from settings import sopranoGlobals
from music.musicdb import MusicDB

import os
from gi.repository import Gtk, GdkPixbuf, Gdk;
from settings import sopranoGlobals, settings

class IconoMediaLibrary():
	def __init__(self, database):
		self.database = database
		#self.path = path
		self.sw = Gtk.ScrolledWindow()	

		parents = {}
		self.treeview = Gtk.TreeView()
		treestore = Gtk.TreeStore(GdkPixbuf.Pixbuf, str, str, int, str)

		col = Gtk.TreeViewColumn()

		render_text = Gtk.CellRendererText()
		col.pack_start(render_text, True)
		col.add_attribute(render_text, 'text', 1)

		render_text = Gtk.CellRendererText()
		col.pack_end(render_text, True)
		col.add_attribute(render_text, 'text', 2)

		render_pb = Gtk.CellRendererPixbuf()
		col.pack_start(render_pb, False)
		col.add_attribute(render_pb, 'pixbuf', 0)

		self.treeview.append_column(col)
		self.treeview.set_headers_visible(False)
		self.treeview.show()
		self.treeview.connect("test-expand-row", self.on_expand)
		self.treeview.connect('row-activated', self.on_activate)
	
		self.sw.add(self.treeview)		

		self.treeview.set_model(treestore)
		self.treeview.get_selection().set_mode(Gtk.SelectionMode.MULTIPLE)
		self.treeview.drag_source_set(Gdk.ModifierType.BUTTON1_MASK, [], Gdk.DragAction.COPY)
		self.treeview.drag_source_add_uri_targets()
		self.treeview.drag_source_add_text_targets()

		self.treeview.connect('button_press_event', self.on_button_press)
		self.treeview.connect('button_release_event', self.on_button_release)
		self.treeview.connect("drag_data_get", self.drag_data_get_cb)
		self.treeview.connect("drag_begin", self.drag_begin_cb)
		self.setup_treestore(self.treeview, None)
		self.defer_select=False

	def drag_data_get_cb(self, widget, drag_context, selection, info, time):
		data = []
		widget.get_selection().selected_foreach(self.afunc, data)
		strarray = []
		for item in data:
			strarray.append(item)
		astr = ''.join(strarray)
		selection.set_text(astr, -1)


	def afunc(self, model, path, iter, data):
		if model.get_value(iter, 4) == "artist":
			self.database.cursor.execute("SELECT Url FROM Songs WHERE Artist='{}' ORDER BY Album, TrackNum".format(model.get_value(iter, 2).replace("'","''")))
			urls = self.database.cursor.fetchall()
			for item in urls:
				data.append(item[0] + '\n')
		elif model.get_value(iter, 4) == "album":
			self.database.cursor.execute("SELECT Url FROM Songs WHERE Album='{}' ORDER BY TrackNum".format(model.get_value(iter, 2).replace("'","''")))
			urls = self.database.cursor.fetchall()
			for item in urls:
				data.append(item[0] + '\n')
		else:
			data.append(model.get_value(iter, 4) + '\n')

		#data.append(model.get_value(iter, 4) + '\n')

	def drag_begin_cb(self, widget, dragcontext):
		return True

	def setup_treestore(self, treeview, path, iter=None):
		from time import time as systime
		systime1 = systime()

		model = treeview.get_model()
		try: print(model.get_value(iter, 4))
		except: pass

		if iter == None:
			self.database.cursor.execute("SELECT DISTINCT Artist FROM Songs")
			artists = self.database.cursor.fetchall()
			for artist in sorted(artists):
				artistiter = model.append(None, [sopranoGlobals.USERSPB, "", artist[0], 0, "artist"])
				treeview.get_model().append(artistiter, [sopranoGlobals.FOLDERPB, "", "artist", 3, artist[0]])
		elif model.get_value(iter, 4) == "artist":
			self.database.cursor.execute("SELECT DISTINCT Album FROM Songs WHERE Artist='{}'".format(model.get_value(iter, 2).replace("'","''")))
			albums = self.database.cursor.fetchall()
			for album in sorted(albums):
				albumiter = model.append(iter, [sopranoGlobals.TRACKPB, "", album[0], 3, "album"])
				treeview.get_model().append(albumiter, [sopranoGlobals.FOLDERPB,"", "album", 3, album[0]])
		elif model.get_value(iter, 4) == "album":
			artistiter = model.iter_parent(iter)
			artistname = model.get_value(artistiter, 2).replace("'","''")
			self.database.cursor.execute("SELECT TrackNum,Title,Url FROM Songs WHERE Album='{}' AND Artist='{}'".format(model.get_value(iter, 2).replace("'","''"),artistname))
			tracks = self.database.cursor.fetchall()
			for track in sorted(tracks):
				model.append(iter, [sopranoGlobals.FILEPB, str(track[0]), track[1], 1, track[2]])

		print("%s%f" % ("Operation took ",systime() - systime1))
			

	def on_activate(self, treeview, path, column):
		if treeview.row_expanded(path):
			treeview.collapse_row(path)
		else:
			treeview.expand_row(path, False)

	def on_expand(self, treeview, iter, path):
		tempiter = treeview.get_model().iter_children(iter)
		if treeview.get_model().get_value(tempiter, 2) == "artist" or treeview.get_model().get_value(tempiter, 2) == "album":
			treeview.get_model().remove(tempiter)
			self.setup_treestore(treeview, path, iter)

	def on_button_press(self, widget, event):
		# Here we intercept mouse clicks on selected items so that we can
		# drag multiple items without the click selecting only one
		target = widget.get_path_at_pos(int(event.x), int(event.y))
		if (target 
		   and event.type == Gdk.EventType.BUTTON_PRESS
		   and not (event.get_state() & (Gdk.ModifierType.CONTROL_MASK|Gdk.ModifierType.SHIFT_MASK))
		   and widget.get_selection().path_is_selected(target[0])) and event.button != 3:
			   # disable selection
			   widget.get_selection().set_select_function(lambda *ignore: False, None)
			   self.defer_select = target[0]
		elif event.button == 3:
			self.on_right_click(event.button, event.time)

	def on_button_release(self, widget, event):
		# re-enable selection
		widget.get_selection().set_select_function(lambda *ignore: True, None)

		target = widget.get_path_at_pos(int(event.x), int(event.y))	
		if (self.defer_select and target and self.defer_select == target[0] and not (event.x==0 and event.y==0)): # certain drag and drop
   				widget.set_cursor(target[0], target[1], False)

	def get_sw(self):
		return self.sw

	def on_right_click(self, button, time, widget=None):
		self.menu = Gtk.Menu()
		aMenuitem = Gtk.MenuItem()
		aMenuitem.set_label("Rescan Library")
		aMenuitem.connect("activate", self.rescanLibrary)
		self.menu.append(aMenuitem)

		self.menu.show_all()
		self.menu.popup( None, None, None, None, button, time)
		return True

	def rescanLibrary(self, widget=None):
		self.database.start()
		while self.database.is_alive():
			while Gtk.events_pending():
				Gtk.main_iteration()
		self.treeview.get_model().clear()
		self.setup_treestore(self.treeview, None)

#debug and testing stuff
#SopranoDB.cursor.execute("SELECT * FROM Songs;")
#rows = SopranoDB.cursor.fetchall()
#print(rows[0])

"""SopranoDB = MusicDB(os.path.join(sopranoGlobals.CONFIGDIR, 'sopranoDB.db'))
SopranoDB.add_folder("file:///media/Media/Music")

treefile = IconoMediaLibrary(SopranoDB)

window = Gtk.Window()
nb = Gtk.Notebook()
nb.add(treefile.get_sw())
window.add(nb)

window.set_size_request(200, 500)
window.connect("delete_event", Gtk.main_quit)
window.show_all()	
Gtk.main()"""

"""#Example code
print(os.path.join(sopranoGlobals.CONFIGDIR, 'sopranoDB.db'))
SopranoDB = MusicDB(os.path.join(sopranoGlobals.CONFIGDIR, 'sopranoDB.db'))

SopranoDB.rebuild_database("file:///media/Media/Music")

#SopranoDB.cursor.execute("SELECT * FROM Songs ORDER BY RANDOM() LIMIT 1")
#SopranoDB.cursor.execute("SELECT count(*) FROM Songs WHERE Artist='Foo Fighters'")
SopranoDB.cursor.execute("SELECT DISTINCT Artist FROM Songs")
rows = SopranoDB.cursor.fetchall()
print("Artists", len(rows))

SopranoDB.cursor.execute("SELECT DISTINCT Album FROM Songs")
rows = SopranoDB.cursor.fetchall()
print("Albums", len(rows))

SopranoDB.cursor.execute("SELECT count(*) FROM Songs;")
rows = SopranoDB.cursor.fetchall()
print("Songs", rows[0][0])"""
