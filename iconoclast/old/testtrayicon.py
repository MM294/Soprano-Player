from gi.repository import Gtk
APPIND_SUPPORT = 1
try: from gi.repository import AppIndicator3
except: APPIND_SUPPORT = 0

class BuilderApp:
	def __init__(self):
		self.window = Gtk.Window(title="Trayicon Example")

	def toggle_window(self, trayicon):
		if self.window.get_property("visible"):
			self.window.hide()
		else:
			self.window.show()

	def make_tray_menu(self):
		self.menu = Gtk.Menu()

		show = Gtk.MenuItem()
		show.set_label("Show")
		separator1 = Gtk.SeparatorMenuItem()
		play = Gtk.MenuItem()
		play.set_label("Play")
		prev = Gtk.MenuItem()
		prev.set_label("Previous")
		next = Gtk.MenuItem()
		next.set_label("Next")
		separator2 = Gtk.SeparatorMenuItem()
		quit = Gtk.MenuItem()
		quit.set_label("Quit")

		show.connect("activate", self.toggle_window)
		## makes these do whatever you need them to
		#play.connect("activate", self.play_pause)
		#prev.connect("activate", self.play_prev)
		#next.connect("activate", self.play_next)
		quit.connect("activate", lambda x: Gtk.main_quit())
		
		self.menu.append(show)
		self.menu.append(separator1)
		self.menu.append(play)
		self.menu.append(prev)
		self.menu.append(next)
		self.menu.append(separator2)
		self.menu.append(quit)
		
		self.menu.show_all()

		return self.menu		

	def right_click_event_statusicon(self, icon, button, time):
		if not self.menu:
			self.make_tray_menu()

		def pos(menu, ignore, aicon):
			return (Gtk.StatusIcon.position_menu(menu, aicon))

		self.menu.popup(None, None, pos, icon, button, time)

def main(iconoclast=None):
	app = BuilderApp()

	if APPIND_SUPPORT == 1:
		ind = AppIndicator3.Indicator.new("iconoclast-indicator-applet", "rhythmbox", AppIndicator3.IndicatorCategory.APPLICATION_STATUS)
		ind.set_status (AppIndicator3.IndicatorStatus.ACTIVE)

		ind.set_menu(app.make_tray_menu())
	else:
		myStatusIcon = Gtk.StatusIcon()
		myStatusIcon.set_from_file('decibel-tray.png')
		myStatusIcon.connect('activate', app.toggle_window)
		myStatusIcon.connect('popup-menu', app.right_click_event_statusicon)

	if __name__ == '__main__':
		Gtk.main()

main()
