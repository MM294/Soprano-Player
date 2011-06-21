import os.path
from gi.repository import Gtk, GdkPixbuf, Gio;

def aboutBoxShow(parent):
    """ Show an about dialog box """
    aboutBox = Gtk.AboutDialog(program_name='Iconoclast Media Player')

    aboutBox.set_name("Iconoclast Media Player")
    aboutBox.set_comments('...And Music For All')
    aboutBox.set_version('0.02')
    aboutBox.set_copyright('(C) 2010 Mike Morley')
    aboutBox.set_website('http://github.com/HairyPalms/IconoClast')
    aboutBox.set_website_label('Iconoclast Homepage')
    aboutBox.set_translator_credits('translator-credits')
    aboutBox.set_artists([('Iconoclast Icon:'), 'Mike Morley <mmorely19@gmail.com>'])
    aboutBox.set_authors([('Developer:'),'Mike Morley <mmorely19@gmail.com>'])
    aboutBox.set_logo_icon_name('rhythmbox')

    # Load the licence from the disk if possible
    if os.path.isfile(os.path.join('', 'gpl2.txt')) :
        aboutBox.set_license(open(os.path.join('', 'gpl2.txt')).read())
        aboutBox.set_wrap_license(True)

    aboutBox.set_transient_for(parent)
    aboutBox.run()
    aboutBox.destroy()

#just for testing remove when used
#show(None)
