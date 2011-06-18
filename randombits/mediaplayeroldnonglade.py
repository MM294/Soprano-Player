from gi.repository import Gio, Gtk, GLib, GdkPixbuf;
#Gtk.MessageDialog(None, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.CLOSE, "Hello World").run()

#!/usr/bin/env python

def widget_destroy(widget, button):
    widget.destroy()

def quit_hello_world(window):
    Gtk.main_quit()

def print_hello_world(button):
    print("Hello World")

def show_about(widget):
	about = Gtk.AboutDialog(program_name='Iconoclast Media Player',
	version='0.1',
	copyright='(C) 2010 Mike Morley',
	license='GPLv3',
	website='http://live.gnome.org/iconoclast',
	comments='Program to demonstrate PyGI functions.',
	authors=['Mike Morley',],
	title='About Iconoclast Media Player')
	about.connect('response', widget_destroy)
	about.show()

def create_help_menu():
	menu = Gtk.Menu()

	gicon = Gio.ThemedIcon.new_with_default_fallbacks('help-about')
        image = Gtk.Image.new_from_gicon(gicon, Gtk.IconSize.MENU)

	menuitem = Gtk.ImageMenuItem(label='About')
	menuitem.connect("activate", show_about)
	menuitem.set_image(image) 

        menu.append(menuitem)

        return menu

def create_file_menu():
	menu = Gtk.Menu()

	gicon = Gio.ThemedIcon.new_with_default_fallbacks('application-exit')
        image = Gtk.Image.new_from_gicon(gicon, Gtk.IconSize.MENU)
	
        menuitem = Gtk.ImageMenuItem(label='Quit')
	menuitem.connect("activate", quit_hello_world)
	menuitem.set_image(image)

        menu.append(menuitem)

        return menu

def create_edit_menu():
	menu = Gtk.Menu()

	gicon = Gio.ThemedIcon.new_with_default_fallbacks('preferences-desktop')
        image = Gtk.Image.new_from_gicon(gicon, Gtk.IconSize.MENU)

        menuitem = Gtk.ImageMenuItem(label='Preferences')
	menuitem.connect("activate", print_hello_world)
	menuitem.set_image(image)

        menu.append(menuitem)

        return menu

def create_view_menu():
        menu = Gtk.Menu()
	
        menuitem = Gtk.RadioMenuItem(label='Full')
	menu.append(menuitem)
	menuitem = Gtk.RadioMenuItem(label='Playlist')
	menu.append(menuitem)
	menuitem = Gtk.RadioMenuItem(label='Mini')
	menu.append(menuitem)        

        return menu

def make_main_window():
	window = Gtk.Window()
	window.set_title("Iconoclast Media Player")
	window.set_default_size(300, 300)
	window.connect("destroy", quit_hello_world)

	vbox = Gtk.VBox(spacing=8)
	window.add(vbox)

	##START MENUS##
	menubar = Gtk.MenuBar()	
	
	filemenuitem = Gtk.MenuItem(label='File')
	filemenuitem.set_submenu(create_file_menu())
	menubar.append(filemenuitem)

	editmenuitem = Gtk.MenuItem(label='Edit')
	editmenuitem.set_submenu(create_edit_menu())
	menubar.append(editmenuitem)

	viewmenuitem = Gtk.MenuItem(label='View')
	viewmenuitem.set_submenu(create_view_menu())
	menubar.append(viewmenuitem)

	helpmenuitem = Gtk.MenuItem(label='Help')		
	helpmenuitem.set_submenu(create_help_menu())
	menubar.append(helpmenuitem)
	
	vbox.pack_start(menubar, 0, 0, 0)
	##END MENUS##

	hbox = Gtk.HBox(spacing=8)
	label = Gtk.Label("lolcakes")
	hbox.add(label)
	
	label = Gtk.Label("failsauce")
	hbox.add(label)

	vbox.add(hbox)	

	window.show_all()

	if __name__ == "__main__":
	    Gtk.main()

make_main_window()
