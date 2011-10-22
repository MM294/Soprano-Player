from gi.repository import Gtk, GdkPixbuf
import os

CONFIGDIR = os.path.join(os.path.expanduser('~'), '.config/sopranoplayer')
if not os.path.exists(CONFIGDIR):
	os.mkdir(CONFIGDIR)

CACHEFILE = os.path.join(CONFIGDIR, '.iconocache.jpg')
TREE_DATA = os.path.join(CONFIGDIR, 'treedata.icono')
SETTINGS_DATA = os.path.join(CONFIGDIR, 'settings.icono')
RADIO_DATA = os.path.join(CONFIGDIR, 'netradio.icono')
EXPLORER_DATA = os.path.join(CONFIGDIR, 'folders.icono')

DATADIR = '/home/mike/Desktop/Python/IconoClast/iconoclast/completed Modules/data'
PLACEHOLDER =  GdkPixbuf.Pixbuf().new_from_file(os.path.join(DATADIR ,'crashbit-soprano.png'))

currentGtkIconTheme = Gtk.IconTheme.get_default()

try: FILEPB = currentGtkIconTheme.load_icon('audio-x-generic', 16, Gtk.IconLookupFlags.FORCE_SIZE)
except: FILEPB = GdkPixbuf.Pixbuf().new_from_file(os.path.join(DATADIR, 'musicfile.png'))

try: FOLDERPB = currentGtkIconTheme.load_icon('folder', 16, Gtk.IconLookupFlags.FORCE_SIZE)
except: FOLDERPB = GdkPixbuf.Pixbuf().new_from_file(os.path.join(DATADIR, 'foldericon.png'))

try: TRACKPB = currentGtkIconTheme.load_icon('media-cdrom-audio', 16, Gtk.IconLookupFlags.FORCE_SIZE)
except: TRACKPB = GdkPixbuf.Pixbuf().new_from_file(os.path.join(DATADIR, 'cd.png'))

try: RADIOPB = currentGtkIconTheme.load_icon('folder-remote', 16, Gtk.IconLookupFlags.FORCE_SIZE)
except: RADIOPB = GdkPixbuf.Pixbuf().new_from_file(os.path.join(DATADIR, 'folderinternet.png'))

try: RADIOPBLARGE = currentGtkIconTheme.load_icon('folder-remote', 48, Gtk.IconLookupFlags.FORCE_SIZE)
except: RADIOPBLARGE = GdkPixbuf.Pixbuf().new_from_file(os.path.join(DATADIR, 'folderinternetlarge.png'))


