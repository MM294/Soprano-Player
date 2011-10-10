import os
from gi.repository import Gtk, GObject, GdkPixbuf, Gdk;


try: filepb = Gtk.IconTheme.get_default().load_icon('audio-x-generic', 16, Gtk.IconLookupFlags.FORCE_SIZE)
except:  filepb = Gtk.IconTheme.get_default().load_icon('empty', 16, Gtk.IconLookupFlags.FORCE_SIZE)



class IconoTreeFile():
	def __init__(self, root, fileFormats):
		self.folderpb = Gtk.IconTheme.get_default().load_icon('folder', 16, Gtk.IconLookupFlags.FORCE_SIZE)
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
		col.pack_start(render_pb, True)
		col.add_attribute(render_pb, 'pixbuf', 0)

		treeview.append_column(col)
		treeview.set_headers_visible(False)
		treeview.show()
		treeview.connect("test-expand-row", self.on_expand)
	
		self.sw.add(treeview)
		

		treeview.set_model(treestore)
		treeview.get_selection().set_mode(Gtk.SelectionMode.MULTIPLE)
		treeview.drag_source_set(Gdk.ModifierType.BUTTON1_MASK, [], Gdk.DragAction.COPY)
		treeview.drag_source_add_uri_targets()
		treeview.drag_source_add_text_targets()

		treeview.connect("drag_data_get", self.drag_data_get_cb)
		treeview.connect("drag_begin", self.drag_begin_cb)
		self.setup_treestore(treeview, self.root)

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
				treeview.get_model().append(tempiter, [self.folderpb,"iconoph", 3, ""])
		for filez in mediaFiles:
			treeview.get_model().append(iter, filez)

	def on_expand(self, treeview, iter, path):
		tempiter = treeview.get_model().iter_children(iter)#.get_value(iter, 3) treeview.iter_children(iter)
		if treeview.get_model().get_value(tempiter, 1) == "iconoph":
			treeview.get_model().remove(tempiter)
		self.setup_treestore(treeview, path, iter)

	def getDirContents(self, directory):
		""" Return a tuple of sorted rows (directories, playlists, mediaFiles) for the given directory """
		mediaFiles  = []
		directories = []

		for (file, path) in self.listDir(directory, False):
		    if os.path.isdir(path):
		        directories.append((self.folderpb, file, 1, path))
		    elif os.path.isfile(path):
			if os.path.splitext(file.lower())[1] in self.fileFormats:
		            mediaFiles.append((filepb, file, 0, path))                

		mediaFiles.sort()
		directories.sort()

		return (directories, mediaFiles)

	#__dirCache = {}

	def listDir(self, directory, listHiddenFiles=False):
	    """
		Return a list of tuples (filename, path) with the given directory content
		The dircache module sorts the list of files, and either it's not needed or it's not sorted the way we want
	    """
	    #if directory in __dirCache: cachedMTime, list = __dirCache[directory]
	    #else:                       cachedMTime, list = None, None

	    #if os.path.exists(directory): mTime = os.stat(directory).st_mtime
	    #else:                         mTime = 0

	    #if mTime != cachedMTime:
		# Make sure it's readable
	    if os.access(directory, os.R_OK | os.X_OK): list = os.listdir(directory)
	    else:                                       list = []

		#__dirCache[directory] = (mTime, list)

	    return [(filename, os.path.join(directory, filename)) for filename in list if listHiddenFiles or filename[0] != '.']

	def get_sw(self):
		return self.sw

"""#debug and testing stuff
treefile = IconoTreeFile('/media/Media/Music', {'.mp3','.ogg','.oga','.wma','.flac','.m4a','.mp4'})
window = Gtk.Window()
window.add(treefile.get_sw())

window.set_size_request(200, 500)
window.connect("delete_event", Gtk.main_quit)
window.show_all()	
Gtk.main()"""
