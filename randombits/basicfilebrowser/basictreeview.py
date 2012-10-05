#!/usr/bin/env python

# example basictreeview.py

from gi.repository import Gtk
import os
import filelister

class BasicTreeViewExample:

    # close the window and quit
    def delete_event(self, widget, event, data=None):
        Gtk.main_quit()
        return False

    def get_icon(self, name):
        theme = Gtk.IconTheme.get_default()
        return theme.load_icon(name, 48, 0)

    def __init__(self):
        # Create a new window
        self.window = Gtk.Window()

        self.window.set_title("Basic TreeView Example")

        self.window.set_size_request(300, 600)

        self.window.connect("delete_event", self.delete_event)

        # create a TreeStore with one string column to use as the model
        self.treestore = Gtk.TreeStore(str)

        # create the TreeView using treestore
        self.treeview = Gtk.TreeView()
	self.treeview.set_headers_visible(False)
	self.treeview.set_model(self.treestore)
        # create the TreeViewColumn to display the data
        self.tvcolumn = Gtk.TreeViewColumn('Column 0')

        # add tvcolumn to treeview
        self.treeview.append_column(self.tvcolumn)

        # create a CellRendererText to render the data
        self.cell = Gtk.CellRendererText()

        # add the cell to the tvcolumn and allow it to expand
        self.tvcolumn.pack_start(self.cell, True)

        # set the cell "text" attribute to column 0 - retrieve text
        # from that column in treestore
        self.tvcolumn.add_attribute(self.cell, 'text', 0)
        self.tvcolumn.add_attribute(self.cell, 'text', 0)

	#My Shit Starts here

	self.treeview.connect('row-expanded', self.populate)

	self.sw = Gtk.ScrolledWindow()

	self.sw.add(self.treeview)

	#My Shit Stops here

        self.window.add(self.sw)

        self.window.show_all()

	self.root = os.path.expanduser('~')

	for (filename, path) in filelister.listDir(self.root): 
		titer = self.treestore.append(None, [filename])       
		directories, mediaFiles = filelister.getDirContents(path)
		#for f2 in directories:
		if directories != None:
			self.treestore.append(titer, [""])
		#for f2 in mediaFiles:
			#self.treestore.append(titer, [f2])

    def populate(self, treeview, treeIter, path):
	for (filename, path) in filelister.listDir(self.root): 
		self.treestore.append(treeIter, [filename])       
		directories, mediaFiles = filelister.getDirContents(path)
	
    """def populate(self, treeview, treeIter, path):
	self.x = (treeview.get_model().get_value(treeIter, 0))
	self.y = (os.path.join(self.root + '/' + self.x)) #parent directory value
	for (filename, filepath) in filelister.listDir(self.y):        
	    if not filename[0] == '.':
		self.treestore.append(treeIter, [filename])
		directories, mediaFiles = filelister.getDirContents(filepath)
		#print(directories)
		newIter = (self.treestore.iter_children(treeIter))
		print(len(directories))
		for f2 in directories:						
			self.treestore.append(newIter, [f2])
			#print("count me!")
			#print(self.y + '/' + f2)
			newIter = self.treestore.iter_next(newIter)
		#print("count me again!")
		self.treestore.append(newIter, ["WTFBLAD"])

			#print(f2[1])
		#for f2 in mediaFiles:
			#print(f2[1])
			#self.treestore.append(treeIter, [f2[0]])		
		if os.path.isdir(filepath):
			print((filepath))
			if directories != None:
				self.treestore.append(treeIter, [filename])
				newIter = self.treestore.iter_children(treeIter)
				self.treestore.append(newIter, [filename])
		else:
			print("this is a file")	"""

def main():
    Gtk.main()

if __name__ == "__main__":
    tvexample = BasicTreeViewExample()
    main()
