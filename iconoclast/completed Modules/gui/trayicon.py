from gi.repository import Gtk

class IconoTray:
	def __init__(self, iconname):
		self.menu = Gtk.Menu()

		APPIND_SUPPORT = 1
		try: from gi.repository import AppIndicator3
		except: APPIND_SUPPORT = 0

		if APPIND_SUPPORT == 1:
			self.ind = AppIndicator3.Indicator.new("Soprano2", iconname, AppIndicator3.IndicatorCategory.APPLICATION_STATUS)
			self.ind.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
			self.ind.set_menu(self.menu)
		else:
			self.myStatusIcon = Gtk.StatusIcon()
			self.myStatusIcon.set_from_icon_name(iconname)
			self.myStatusIcon.connect('popup-menu', self.right_click_event_statusicon)
	
	def add_menu_item(self, command, title):
		aMenuitem = Gtk.MenuItem()
		aMenuitem.set_label(title)
		aMenuitem.connect("activate", command)

		self.menu.append(aMenuitem)
		self.menu.show_all()

	def add_seperator(self):
		aMenuitem = Gtk.SeparatorMenuItem()
		self.menu.append(aMenuitem)
		self.menu.show_all()

	def get_tray_menu(self):
		return self.menu		

	def right_click_event_statusicon(self, icon, button, time):
		self.get_tray_menu()

		def pos(menu, aicon):
			return (Gtk.StatusIcon.position_menu(menu, aicon))

		self.menu.popup(None, None, pos, icon, button, time)

#test/debug stuff below here
"""import time
def killthingy(app):
	print("killthingy run")
	app = None
	time.sleep(4)
	app = IconoTray("rhythmbox")
	app.add_menu_item(lambda x: Gtk.main_quit(), "Quit")

def main(iconoclast=None):
	app = IconoTray("rhythmbox")
	app.add_menu_item(lambda x: Gtk.main_quit(), "Quit")
	app.add_seperator()
	app.add_menu_item(lambda x: killthingy(app), "Play")

	if __name__ == '__main__':
		Gtk.main()

main()"""
