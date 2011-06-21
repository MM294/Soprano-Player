from gi.repository import Gtk

def main(iconoclast=None):

	#ictheme = Gtk.IconTheme.get_default()
	aPixbuf = Gtk.IconTheme.get_default().load_icon('rhythmbox', 24, Gtk.IconLookupFlags.FORCE_SIZE)

	myStatusIcon = Gtk.StatusIcon()
	myStatusIcon.set_from_pixbuf(aPixbuf)

	if __name__ == '__main__':
		Gtk.main()

main()
