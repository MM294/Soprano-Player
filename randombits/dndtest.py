from gi.repository import Gtk, GdkPixbuf, Gdk, Gio, GObject

def motion_cb(windowid, context, x, y, time):
    return True

def drop_cb(windowid, context, x, y, time):
    # Some data was dropped, get the data
    windowid.drag_get_data(context, context.list_targets()[-1], time)
    return True

def got_data_cb(windowid, context, x, y, data, info, time):
    # Got data.
    label.set_text(data.get_text())
    context.finish(True, False, time)

window = Gtk.Window()
window.set_size_request(200, 150)
window.connect('destroy', lambda window: Gtk.main_quit())
label = Gtk.Label()
window.add(label)
window.show_all()

window.drag_dest_set(0, [], 0)
window.connect('drag_motion', motion_cb)
window.connect('drag_drop', drop_cb)
window.connect('drag_data_received', got_data_cb)



Gtk.main()
