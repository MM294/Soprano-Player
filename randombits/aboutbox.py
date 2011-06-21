# -*- coding: utf-8 -*-
#
# Author: Ingelrest François (Francois.Ingelrest@gmail.com)
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Library General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301 USA

import os.path, webbrowser
from gi.repository import Gtk, GdkPixbuf;

def show():
    """ Show an about dialog box """
    dlg = Gtk.AboutDialog()
    #dlg.set_transient_for(parent)

    # Set credit information
    dlg.set_name("Iconoclast Media Player")
    dlg.set_comments('...And Music For All')
    dlg.set_version('0.02')
    dlg.set_website('http://github.com/HairyPalms/IconoClast')
    dlg.set_website_label('Iconoclast Homepage')
    dlg.set_translator_credits('translator-credits')
    dlg.set_artists([('Iconoclast Icon:'),
        '    Mike Morley <sebastien.durel@gmail.com>'])

    dlg.set_authors([
        _('Developer:'),
        '    Mike Morley <Francois.Ingelrest@gmail.com>',
        '',])

    # Set logo
    dlg.set_logo(GdkPixbuf.Pixbuf.new_from_file(consts.fileImgIcon128))

    # Load the licence from the disk if possible
    if os.path.isfile(consts.fileLicense) :
        dlg.set_license(open(consts.fileLicense).read())
        dlg.set_wrap_license(True)

    dlg.run()
    dlg.destroy()

show()
