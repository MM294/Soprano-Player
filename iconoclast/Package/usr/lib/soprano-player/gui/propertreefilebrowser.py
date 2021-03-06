import os
from gi.repository import Gtk, GdkPixbuf, Gdk;
from settings import sopranoGlobals, settings

class IconoTreeFile():
	def __init__(self, root, fileFormats):
		self.root = root
		self.sw = Gtk.ScrolledWindow()	
		self.fileFormats = fileFormats

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
		treeview.connect("test-expand-row", self.on_expand)
		treeview.connect('row-activated', self.on_activate)
	
		self.sw.add(treeview)		

		treeview.set_model(treestore)
		treeview.get_selection().set_mode(Gtk.SelectionMode.MULTIPLE)
		treeview.drag_source_set(Gdk.ModifierType.BUTTON1_MASK, [], Gdk.DragAction.COPY)
		treeview.drag_source_add_uri_targets()
		treeview.drag_source_add_text_targets()

		treeview.connect('button_press_event', self.on_button_press)
		treeview.connect('button_release_event', self.on_button_release)
		treeview.connect("drag_data_get", self.drag_data_get_cb)
		treeview.connect("drag_begin", self.drag_begin_cb)
		self.setup_treestore(treeview, self.root)
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
		data.append(model.get_value(iter, 3) + '\n')

	def drag_begin_cb(self, widget, dragcontext):
		return True

	def setup_treestore(self, treeview, path, iter=None):
		if iter == None:
			directories, mediaFiles = self.getDirContents(self.root)
		else:
			directories, mediaFiles = self.getDirContents(treeview.get_model().get_value(iter, 3))

		for subdir in directories:
			tempiter = treeview.get_model().append(iter, subdir)
			if iter == None:
				directories2, mediaFiles2 = self.getDirContents(os.path.join(self.root, subdir[1]))
			else:
				directories2, mediaFiles2 = self.getDirContents(os.path.join(treeview.get_model().get_value(iter, 3), subdir[1]))
			if not directories2 == [] or not mediaFiles2 == []:
				treeview.get_model().append(tempiter, [sopranoGlobals.FOLDERPB,"iconoph", 3, ""])
		for filez in mediaFiles:
			treeview.get_model().append(iter, filez)

	def on_activate(self, treeview, path, column):
		if treeview.row_expanded(path):
			treeview.collapse_row(path)
		else:
			treeview.expand_row(path, False)

	def on_expand(self, treeview, iter, path):
		tempiter = treeview.get_model().iter_children(iter)
		if treeview.get_model().get_value(tempiter, 1) == "iconoph":
			treeview.get_model().remove(tempiter)
			self.setup_treestore(treeview, path, iter)

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

	#2 more methods inspired by decibel#
	def getDirContents(self, directory):
		""" Return a tuple of sorted rows (directories, playlists, mediaFiles) for the given directory """
		mediaFiles  = []
		directories = []

		for (file, path) in self.listDir(directory, False):
			if os.path.isdir(path):
				directories.append((sopranoGlobals.FOLDERPB, file, 1, path))
			elif os.path.isfile(path):
				if os.path.splitext(file.lower())[1] in self.fileFormats:
					mediaFiles.append((sopranoGlobals.FILEPB, file, 0, path))                

		mediaFiles.sort()
		directories.sort()

		return (directories, mediaFiles)

	def listDir(self, directory, listHiddenFiles=False):

		if os.access(directory, os.R_OK | os.X_OK): list = os.listdir(directory)
		else:                                       list = []

		return [(filename, os.path.join(directory, filename)) for filename in list if listHiddenFiles or filename[0] != '.']

	def get_sw(self):
		return self.sw

#debug and testing stuff
"""treefile = IconoTreeFile('/media/Media/Music', {'.mp3','.ogg','.oga','.wma','.flac','.m4a','.mp4'})
treefile2 = IconoTreeFile('/', {'.mp3','.ogg','.oga','.wma','.flac','.m4a','.mp4'})
treefile3 = IconoTreeFile('/home/mike', {'.mp3','.ogg','.oga','.wma','.flac','.m4a','.mp4'})
window = Gtk.Window()
nb = Gtk.Notebook()
nb.add(treefile.get_sw())
nb.add(treefile2.get_sw())
nb.add(treefile3.get_sw())
window.add(nb)

window.set_size_request(200, 500)
window.connect("delete_event", Gtk.main_quit)
window.show_all()	
Gtk.main()"""
