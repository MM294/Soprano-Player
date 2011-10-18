from gi.repository import Gtk, GObject, GdkPixbuf, Gdk

class IconoAudioCD():
	def __init__(self, device=None):
		self.trackpb = Gtk.IconTheme.get_default().load_icon('media-cdrom-audio', 16, Gtk.IconLookupFlags.FORCE_SIZE)
		self.device = device
		self.sw = Gtk.ScrolledWindow()	

		parents = {}
		treeview = Gtk.TreeView()
		treestore = Gtk.TreeStore(GdkPixbuf.Pixbuf, str, int, str)

		col = Gtk.TreeViewColumn()

		render_text = Gtk.CellRendererText()
		col.pack_end(render_text, True)
		col.add_attribute(render_text, 'text', 1)

		render_pb = Gtk.CellRendererPixbuf()
		col.pack_start(render_pb, False)
		col.add_attribute(render_pb, 'pixbuf', 0)

		treeview.append_column(col)
		treeview.set_headers_visible(False)
		treeview.show()
	
		self.sw.add(treeview)		

		treeview.set_model(treestore)
		treeview.get_selection().set_mode(Gtk.SelectionMode.MULTIPLE)
		treeview.drag_source_set(Gdk.ModifierType.BUTTON1_MASK, [], Gdk.DragAction.COPY)

		treeview.drag_source_add_text_targets()
		treeview.connect('button-press-event', self.on_right_click)
		treeview.connect("drag_data_get", self.drag_data_get_cb)
		treeview.connect("drag_begin", self.drag_begin_cb)
		GObject.idle_add(lambda: self.refreshDiscs(treeview, self.device))

	def on_right_click(self, widget, event):
		if event.button == 3:
			self.menu = Gtk.Menu()
			aMenuitem = Gtk.MenuItem()
			aMenuitem.set_label("Refresh")
			aMenuitem.connect("activate", lambda x: self.refreshDiscs(self.sw.get_child(),self.device))

			self.menu.append(aMenuitem)
			self.menu.show_all()
			self.menu.popup( None, None, None, None, event.button, event.time)
			return True

	def drag_data_get_cb(self, widget, drag_context, selection, info, time):
		data = []
		widget.get_selection().selected_foreach(self.afunc, data)
		strarray = []
		for item in data:
			strarray.append(item)
		astr = ''.join(strarray)
		selection.set_text(astr, -1)


	def afunc(self, model, path, iter, data):
		data.append(model.get_value(iter, 3) + '\n')

	def drag_begin_cb(self, widget, dragcontext):
		return True

	def refreshDiscs(self, treeview, path):
		treeview.get_model().clear()
		tracks = self.getCDTracks(self.device)
		for track in tracks:
			tempiter = treeview.get_model().append(None, track)

	def getCDTracks(self, device):
		import cdrom
		try: 
			if device:
				device = cdrom.open(device)
			else:
				device = cdrom.open()
			(first, last) = cdrom.toc_header(device)
			cdtracks = []
			for i in range(first, last+1):
				cdtracks.append([self.trackpb, "Track " + str(i), 3, 'cdda://' + str(i) ])
			return cdtracks
		except:
			return [[self.trackpb, "No CD Found", 3, '' ]]		

	def get_sw(self):
		return self.sw

#debug and testing stuff
"""treefile = IconoAudioCD('/dev/cdrom')
window = Gtk.Window()
window.add(treefile.get_sw())

window.set_size_request(200, 500)
window.connect("delete_event", Gtk.main_quit)
window.show_all()	
Gtk.main()"""
