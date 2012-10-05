from gi.repository import Gtk, GObject, GdkPixbuf, Gdk
from settings import sopranoGlobals, settings

class IconoRadio():
	def __init__(self):
		self.sw = Gtk.ScrolledWindow()	
		self.editPref = settings.IconoPrefs(sopranoGlobals.RADIO_DATA)
		stations = self.editPref.get_radioStations()

		parents = {}
		self.treeview = Gtk.TreeView()
		treestore = Gtk.TreeStore(GdkPixbuf.Pixbuf, str, int, str)

		col = Gtk.TreeViewColumn()

		render_text = Gtk.CellRendererText()
		col.pack_end(render_text, True)
		col.add_attribute(render_text, 'text', 1)

		render_pb = Gtk.CellRendererPixbuf()
		col.pack_start(render_pb, False)
		col.add_attribute(render_pb, 'pixbuf', 0)

		self.treeview.append_column(col)
		self.treeview.set_headers_visible(False)		

		self.emptybtn = Gtk.Button(label="Add a Station")
		self.emptybtn.connect('clicked', self.addStationDialog)
		vbox = Gtk.VBox()
		vbox.pack_start(self.emptybtn, True, False, 0)
		vbox.add(self.treeview)
		if stations == []:
			self.treeview.set_no_show_all(True)
		else:
			self.emptybtn.set_no_show_all(True)
		self.sw.add_with_viewport(vbox)
		
		self.treeview.set_model(treestore)
		self.treeview.get_selection().set_mode(Gtk.SelectionMode.MULTIPLE)
		self.treeview.drag_source_set(Gdk.ModifierType.BUTTON1_MASK, [], Gdk.DragAction.COPY)

		self.treeview.drag_source_add_text_targets()
		self.treeview.connect('button-press-event', self.on_right_click)
		self.treeview.connect("drag_data_get", self.drag_data_get_cb)
		self.treeview.connect("drag_begin", self.drag_begin_cb)
		GObject.idle_add(self.setupStations, stations)

	def on_right_click(self, widget, event):
		if event.button == 3:
			self.menu = Gtk.Menu()
			aMenuitem = Gtk.MenuItem()
			aMenuitem.set_label("Add Station")
			aMenuitem.connect("activate", self.addStationDialog)
			self.menu.append(aMenuitem)

			aMenuitem = Gtk.MenuItem()
			aMenuitem.set_label("Remove Station")
			aMenuitem.connect("activate", self.delStation)
			self.menu.append(aMenuitem)
			
			self.menu.show_all()
			self.menu.popup( None, None, None, None, event.button, event.time)
			return True

	def drag_data_get_cb(self, widget, drag_context, selection, info, time):
		data = []
		widget.get_selection().selected_foreach(self.afunc, data)
		strarray = []
		#print(data)
		for item in data:
			strarray.append(item)
		astr = ''.join(strarray)
		selection.set_text(astr, -1)

	def afunc(self, model, path, iter, data):
		#data.append(model.get_value(iter, 1) + '\n')
		data.append(model.get_value(iter, 3) + '\n')
				

	def drag_begin_cb(self, widget, dragcontext):
		return True

	def setupStations(self, stations):
		self.treeview.get_model().clear()
		for key, value in stations.iteritems():
			self.addStation((key, value))

	def addStation(self, station):
		self.treeview.get_model().append(None, [sopranoGlobals.RADIOPB, station[0], 3, station[1] ])

	def delStation(self, widget):
		model, paths = self.treeview.get_selection().get_selected_rows()
		for i in paths:
			tempiter = model.get_iter(i)
			station = (model.get_value(tempiter, 1), model.get_value(tempiter, 3))
			model.remove(tempiter)
			self.editPref.delete_radio(station)
		if len(model) == 0:
			self.treeview.hide()
			self.emptybtn.show()

	def addStationDialog(self, widget=None):
		dialog = Gtk.Dialog(' ',
		                    None,
						    Gtk.DialogFlags.MODAL | 
		                    Gtk.DialogFlags.DESTROY_WITH_PARENT,
						    (Gtk.STOCK_OK, Gtk.ResponseType.OK,
		                     "Cancel", Gtk.ResponseType.CANCEL))

		content_area = dialog.get_content_area ()
		hbox = Gtk.HBox(spacing=8)
		hbox.set_border_width(8)

		label = Gtk.Label("Add Station")
		warnlabel = Gtk.Label("")

		vbox = Gtk.VBox(spacing=8)
		vbox.set_border_width(8)
		vbox.pack_start(label, False, False, 0)
		vbox.pack_start(warnlabel, False, False, 0)
		vbox.pack_start(hbox, False, False, 0)
		content_area.pack_start(vbox, False, False, 0)

		stock = Gtk.Image.new_from_pixbuf(sopranoGlobals.RADIOPBLARGE)

		hbox.pack_start(stock, False, False, 0)

		table = Gtk.Table(2, 2, False)
		table.set_row_spacings(4)
		table.set_col_spacings(4)
		hbox.pack_start(table, True, True, 0)
		label = Gtk.Label.new_with_mnemonic("_Name")
		table.attach_defaults(label, 0, 1, 0, 1);
		local_entry1 = Gtk.Entry();
		table.attach_defaults(local_entry1, 1, 2, 0, 1)
		label.set_mnemonic_widget(local_entry1)

		label = Gtk.Label.new_with_mnemonic("_Uri")
		table.attach_defaults (label, 0, 1, 1, 2)

		local_entry2 = Gtk.Entry()
		table.attach_defaults(local_entry2, 1, 2, 1, 2)
		label.set_mnemonic_widget(local_entry2);
	  
		vbox.show_all();
		
		while True:
			response = dialog.run()
			if response == Gtk.ResponseType.OK:
				station = (local_entry1.get_text(), local_entry2.get_text())
				if station[1][:7] != 'http://' and station[1][:6] != 'mms://':
					warnlabel.set_markup("<b>Not a Supported Uri</b>")
				elif station[0] in self.editPref.get_radioStations().keys():
					warnlabel.set_markup("<b>Radio name already exists</b>")
				else:
					self.addStation(station)
					self.editPref.add_radio(station)
					self.treeview.show()
					self.emptybtn.hide()
					dialog.destroy()
					break
			else:				
				dialog.destroy()
				break

	def get_sw(self):
		return self.sw

#debug and testing stuff
"""treefile = IconoRadio()
window = Gtk.Window()
window.add(treefile.get_sw())

window.set_size_request(200, 500)
window.connect("delete_event", Gtk.main_quit)
window.show_all()	
Gtk.main()"""
