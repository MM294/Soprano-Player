#Icon Combobox 
#Author: Mike Morley (mmorely19@gmail.com)
from gi.repository import Gtk, GdkPixbuf

class HeaderedComboBox:

    def __init__(self):

        self.name_store = Gtk.ListStore(int, str, GdkPixbuf.Pixbuf)
        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)

        name_combo = Gtk.ComboBox.new_with_model(self.name_store)
        name_combo.connect("changed", self.on_name_combo_changed)

	renderertext = Gtk.CellRendererText()
	name_combo.pack_end(renderertext, True)
	name_combo.add_attribute(renderertext, "markup", 1) # use renderertext with "text" from name_store model data at 1

	rendererpb = Gtk.CellRendererPixbuf()
	name_combo.pack_start(rendererpb, True)
	name_combo.add_attribute(rendererpb, "pixbuf", 2) # use rendererpb with a "pixbuf" from name_store model data at 2

        name_combo.set_entry_text_column(1)
        self.vbox.pack_start(name_combo, False, False, 0) 

    def on_name_combo_changed(self, combo):
        tree_iter = combo.get_active_iter()
        if tree_iter != None:
            model = combo.get_model()
            row_id, name = model[tree_iter][:2]
            #print "Selected: ID=%d, name=%s" % (row_id, name)
	    if row_id == 1:
		print "zomg its a header!"
		combo.set_active_iter(model.iter_next(tree_iter)) # if they try and select a header move to the real entry below instead
        else:
            entry = combo.get_child()
            print "Entered: %s" % entry.get_text()

    def add_entry(self, header, Name, pixbuf=None):
	self.name_store.append([header, Name, pixbuf])

    def get_ref(self):
	return self.vbox


"""#testing and debugging bits below
folderpb = Gtk.IconTheme.get_default().load_icon('folder', 16, Gtk.IconLookupFlags.FORCE_SIZE)
win = Gtk.Window()
cbbox = HeaderedComboBox()

cbbox.add_entry(1, "<b>Folders</b>", None)
cbbox.add_entry(0, "Home", folderpb)
cbbox.add_entry(0, "Media", folderpb)
cbbox.add_entry(1, "<b>Library</b>", None)
cbbox.add_entry(0, "Music", folderpb)

win.add(cbbox.get_ref())
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()"""
