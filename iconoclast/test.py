import gtk

def but_call(widget,data=None):
              #do what u want here
               win.show_all()   #this shows ur new window
     
win=gtk.Window()
win.connect("destroy",lambda wid:gtk.main_quit())
mywin=gtk.Window()
mywin.connect("destroy",lambda wid:gtk.main_quit())
mywin.set_default_size(500, 400)

#now show this window when somebody presses a button in ur main window... mywin
button=gtk.Button()
button.set_default_size(500, 400)
button.set_label("CLICK ME!")
button.connect("clicked",but_call)
mywin.add(button)
mywin.show_all()
gtk.main()
