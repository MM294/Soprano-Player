import os.path
from settings import sopranoGlobals
from gi.repository import Gtk;

def aboutBoxShow(widget, parent, parameter=None):
    """ Show an about dialog box """
    aboutBox = Gtk.AboutDialog(program_name='Soprano Media Player')

    aboutBox.set_name("Soprano Media Player")
    aboutBox.set_comments('...One Goal, Be Epic')
    aboutBox.set_version('0.02')
    aboutBox.set_copyright('(C) 2010 Mike Morley')
    aboutBox.set_website('http://github.com/HairyPalms/IconoClast')
    aboutBox.set_website_label('Soprano Homepage')
    aboutBox.set_translator_credits('translator-credits')
    aboutBox.set_artists([('Soprano Icon:'), 'Mike Morley <mmorely19@gmail.com>'])
    aboutBox.set_authors([('Developer:'),'Mike Morley <mmorely19@gmail.com>'])
    aboutBox.set_logo(sopranoGlobals.PLACEHOLDER)

    # Load the licence from the disk if possible
    if os.path.isfile(os.path.join('data', 'gpl2.txt')) :
        aboutBox.set_license(open(os.path.join('data', 'gpl2.txt')).read())
        aboutBox.set_wrap_license(True)

    aboutBox.set_transient_for(parent)
    aboutBox.run()
    aboutBox.destroy()

#just for testing remove when used
#aboutBoxShow(None)
