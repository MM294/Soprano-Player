"""import gtk
rect = gtk.gdk.Rectangle(0, 0, 12, 10)
aWindow = gtk.Window()
aWindow.set_size_request(rect.width / 3, -1)
aWindow.show_all()

gtk.main()

from gi.repository import Gtk, Gdk
rect = Gdk.Rectangle() # takes 0 arguments error output, wut wut in the butt?
rect.width = 24
aWindow = Gtk.Window()
aWindow.set_size_request(rect.width * 3, -1)
aWindow.show_all()

Gtk.main()"""

from gi.repository import Gtk

class aStatusIcon:
    def __init__(self):
        self.statusicon = Gtk.StatusIcon()
        self.statusicon.set_from_stock(Gtk.STOCK_HOME) 
        self.statusicon.connect("popup-menu", self.right_click_event)
        
        window = Gtk.Window()
        window.connect("destroy", lambda w: Gtk.main_quit())
        window.show_all()
		
    def right_click_event(self, icon, button, time):
        self.menu = Gtk.Menu()

        about = Gtk.MenuItem()
	about.set_label("About")
        quit = Gtk.MenuItem()
	quit.set_label("Quit")
        
        about.connect("activate", self.show_about_dialog)
        quit.connect("activate", Gtk.main_quit)
        
        self.menu.append(about)
        self.menu.append(quit)
        
        self.menu.show_all()

	def pos(menu, ignore, icon):
		return (Gtk.StatusIcon.position_menu(menu, icon))

        self.menu.popup(None, None, pos, self.statusicon, button, time)	
        
    def show_about_dialog(self, widget):
        about_dialog = Gtk.AboutDialog()

        about_dialog.set_destroy_with_parent(True)
        about_dialog.set_name("StatusIcon Example")
        about_dialog.set_version("1.0")
        about_dialog.set_authors(["Andrew Steele"])
        		
        about_dialog.run()
        about_dialog.destroy()

aStatusIcon()
Gtk.main()
