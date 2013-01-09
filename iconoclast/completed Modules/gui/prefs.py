from gi.repository import Gtk, GdkPixbuf
from gui import PrefWin
from settings import settings
from settings import sopranoGlobals
import os.path

class SopranoPrefWin:
	def __init__(self, showtray):
		self.audioFolderlist = settings.IconoPrefs(sopranoGlobals.EXPLORER_DATA)
		
		page1, traycheckbox = self.create_page1(showtray)

		self.win = PrefWin.PrefWin()
		self.win.traycheckbox = traycheckbox
		self.win.change = 0
		self.win.create_category("Desktop", "folder", page1)

	def create_page1(self, showtray):
		#Page 1
		vbox = Gtk.VBox()
		#Line 1
		categorys = Gtk.ListStore(str, GdkPixbuf.Pixbuf, str)
		column = Gtk.TreeViewColumn()
		title = Gtk.CellRendererText()
		piccy = Gtk.CellRendererPixbuf()
		namecol = Gtk.CellRendererText()
		column.pack_start(namecol, True)
		column.pack_start(piccy, True)
		column.pack_start(title, True)
		column.add_attribute(namecol, "text", 0)
		column.add_attribute(piccy, "pixbuf", 1)
		column.add_attribute(title, "text", 2)

		self.tree = Gtk.TreeView(categorys)
		self.tree.set_headers_visible(False)
		self.tree.append_column(column)

		for key, value in self.audioFolderlist.get_radioStations().items():
			categorys.append([key, sopranoGlobals.FOLDERPB, value])	
		#Line 2
		line3HBox = Gtk.HBox()
		line3Button1 = Gtk.Button()
		line3Button1.set_label("Add Folder")
		line3Button1.connect('clicked', self.addFolderDialog)
		line3Button2 = Gtk.Button()
		line3Button2.set_label("Remove Folder")
		line3Button2.connect('clicked',self.removeFolder)
		line3HBox.pack_start(line3Button1, True, True, 4)
		line3HBox.pack_start(line3Button2, True, True, 4)
		#Seperator
		separator1 = Gtk.Separator()
		#Line 3
		hbox = Gtk.HBox()
		alabel = Gtk.Label("Show Tray Icon")
		traycheckbox = Gtk.Switch()
		traycheckbox.set_active(showtray)
		hbox.pack_start(alabel, True, False, 0)
		hbox.pack_end(traycheckbox, True, False, 0)
		#Packing
		vbox.pack_start(self.tree, True, True, 0)
		vbox.pack_start(line3HBox, False, True, 5)
		vbox.pack_start(separator1, False, True, 5)
		vbox.pack_start(hbox, False, True, 0)
		return vbox, traycheckbox

	def get_change_value(self):
		return self.win.change

	def addFolderDialog(self, widget=None):
		dialog = Gtk.Dialog(' ',
		                    None,
						    Gtk.DialogFlags.MODAL | 
		                    Gtk.DialogFlags.DESTROY_WITH_PARENT,
						    (Gtk.STOCK_OK, Gtk.ResponseType.OK,
		                     "Cancel", Gtk.ResponseType.CANCEL))

		content_area = dialog.get_content_area ()
		hbox = Gtk.HBox(spacing=8)
		hbox.set_border_width(8)

		label = Gtk.Label("Add Location")
		warnlabel = Gtk.Label("Enter or select a location to add to the main window")

		vbox = Gtk.VBox(spacing=8)
		vbox.set_border_width(8)
		vbox.pack_start(label, False, False, 0)
		vbox.pack_start(warnlabel, False, False, 0)
		vbox.pack_start(hbox, False, False, 0)
		content_area.pack_start(vbox, False, False, 0)

		stock = Gtk.Image.new_from_pixbuf(sopranoGlobals.FOLDERPBLARGE)

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
				if not os.path.isdir(station[1]):# != 'file://':
					warnlabel.set_markup("<b>Not a Supported Uri</b>")
				elif station[0] in self.audioFolderlist.get_radioStations().keys():
					warnlabel.set_markup("<b>Folder with that name already exists</b>")
				else:
					self.tree.get_model().append([station[0],sopranoGlobals.FOLDERPB,station[1]])
					self.audioFolderlist.add_radio(station)
					dialog.destroy()
					self.win.change = self.win.change + 1
					print(self.win.change)
					break
			else:				
				dialog.destroy()
				break
	def removeFolder(self, widget=None):
		model, selected = self.tree.get_selection().get_selected()
		if selected:
			self.audioFolderlist.delete_radio([model.get_value(selected, 0)])
			model.remove(selected)
			self.win.change = self.win.change - 1
			print(self.win.change)

"""def main():
	win = SopranoPrefWin(True)
	win.win.connect("delete_event", Gtk.main_quit)
	if __name__ == '__main__':
		Gtk.main()
main()"""
