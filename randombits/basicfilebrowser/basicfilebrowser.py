#!/usr/bin/python

# ZetCode PyGTK tutorial 
#
# This example demonstrates the IconView widget.
# It shows the contents of the currently selected
# directory on the disk.
#
# author: jan bodnar
# website: zetcode.com 
# last edited: February 2009

#Updated June 2011 by Mike Morley for PyGobject and Gtk3#

from gi.repository import Gtk, GdkPixbuf
import os

COL_PATH = 0
COL_PIXBUF = 1
COL_IS_DIRECTORY = 2


class PyApp(Gtk.Window): 
    def __init__(self):
        super(PyApp, self).__init__()
        
        self.set_size_request(150, 600)
        self.set_position(Gtk.WindowPosition.CENTER)
        
        self.connect("destroy", Gtk.main_quit)
        self.set_title("IconView")
        
        self.current_directory = os.path.realpath(os.path.expanduser('~')) #'/'

        vbox = Gtk.VBox();
       
        toolbar = Gtk.Toolbar()
        vbox.pack_start(toolbar, False, False, 0)

        self.upButton = Gtk.ToolButton()#Gtk.STOCK_GO_UP);
	self.upButton.set_stock_id(Gtk.STOCK_GO_UP)
        self.upButton.set_is_important(True)
        self.upButton.set_sensitive(False)
        toolbar.insert(self.upButton, -1)

        homeButton = Gtk.ToolButton()#Gtk.STOCK_HOME)
	homeButton.set_stock_id(Gtk.STOCK_HOME)
        homeButton.set_is_important(True)
        toolbar.insert(homeButton, -1)

        self.fileIcon = self.get_icon(Gtk.STOCK_FILE)
        self.dirIcon = self.get_icon(Gtk.STOCK_DIRECTORY)

        sw = Gtk.ScrolledWindow()
        sw.set_shadow_type(Gtk.ShadowType.ETCHED_IN)
        sw.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        vbox.pack_start(sw, True, True, 0)

        self.store = self.create_store()
        self.fill_store()

        iconView = Gtk.IconView()
	iconView.set_model(self.store)
        iconView.set_selection_mode(Gtk.SelectionMode.MULTIPLE)

        self.upButton.connect("clicked", self.on_up_clicked)
        homeButton.connect("clicked", self.on_home_clicked)

        iconView.set_text_column(COL_PATH)
        iconView.set_pixbuf_column(COL_PIXBUF)

        iconView.connect("item-activated", self.on_item_activated)
        sw.add(iconView)
        iconView.grab_focus()

        self.add(vbox)
        self.show_all()

    def get_icon(self, name):
        theme = Gtk.IconTheme.get_default()
        return theme.load_icon(name, 48, 0)
    

    def create_store(self):
        store = Gtk.ListStore(str, GdkPixbuf.Pixbuf, bool)
        store.set_sort_column_id(COL_PATH, Gtk.SortType.ASCENDING)
        return store
            
    
    def fill_store(self):
        self.store.clear()

        if self.current_directory == None:
            return

        for fl in os.listdir(self.current_directory):
        
            if not fl[0] == '.': 
                if os.path.isdir(os.path.join(self.current_directory, fl)):
                    self.store.append([fl, self.dirIcon, True])
                else:
                    self.store.append([fl, self.fileIcon, False])             
        
    

    def on_home_clicked(self, widget):
        self.current_directory = os.path.realpath(os.path.expanduser('~'))
        self.fill_store()
        self.upButton.set_sensitive(True)
        
    
    def on_item_activated(self, widget, item):

        model = widget.get_model()
        path = model[item][COL_PATH]
        isDir = model[item][COL_IS_DIRECTORY]

        if not isDir:
            return
            
        self.current_directory = self.current_directory + os.path.sep + path
        self.fill_store()
        self.upButton.set_sensitive(True)
    

    def on_up_clicked(self, widget):
        self.current_directory = os.path.dirname(self.current_directory)
        self.fill_store()
        sensitive = True
        if self.current_directory == "/": sensitive = False
        self.upButton.set_sensitive(sensitive)
    
def main():
	app = PyApp()
	if __name__ == '__main__':
    		Gtk.main()

main()
