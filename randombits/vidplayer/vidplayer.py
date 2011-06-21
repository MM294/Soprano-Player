#!/usr/bin/env python

import sys, os
from gi.repository import Gtk, GObject, Gdk
import gst

class Gtkvid:	
	def __init__(self):
		window = Gtk.Window()
		window.set_title("Video-Player")
		window.set_default_size(500, 400)
		window.connect("destroy", Gtk.main_quit, "WM destroy")
		vbox = Gtk.VBox()
		window.add(vbox)
		hbox = Gtk.HBox()
		vbox.pack_start(hbox, False, 0, 0)
		self.entry = Gtk.Entry()
		hbox.add(self.entry)
		self.button = Gtk.Button("Start")
		hbox.pack_start(self.button, False, 0, 0)
		self.button.connect("clicked", self.start_stop)
		self.movie_window = Gtk.DrawingArea()
		vbox.add(self.movie_window)
		window.show_all()
		
		self.player = gst.element_factory_make("playbin2", "player")
		bus = self.player.get_bus()
		bus.add_signal_watch()
		bus.enable_sync_message_emission()
		bus.connect("message", self.on_message)
		bus.connect("sync-message::element", self.on_sync_message)
		
	def start_stop(self, w):
		if self.button.get_label() == "Start":
			filepath = self.entry.get_text()
			if os.path.isfile(filepath):
				self.button.set_label("Stop")
				self.player.set_property("uri", "file://" + filepath)
				self.player.set_state(gst.STATE_PLAYING)
		else:
			self.player.set_state(gst.STATE_NULL)
			self.button.set_label("Start")
						
	def on_message(self, bus, message):
		t = message.type
		if t == gst.MESSAGE_EOS:
			self.player.set_state(gst.STATE_NULL)
			self.button.set_label("Start")
		elif t == gst.MESSAGE_ERROR:
			self.player.set_state(gst.STATE_NULL)
			err, debug = message.parse_error()
			print "Error: %s" % err, debug
			self.button.set_label("Start")
	
	def on_sync_message(self, bus, message):
		if message.structure is None:
			return
		message_name = message.structure.get_name()
		if message_name == "prepare-xwindow-id":
			imagesink = message.src
			imagesink.set_property("force-aspect-ratio", True)
			Gdk.threads_enter()
			#print(Gdk.Window.xid(self.movie_window.get_parent_window()))
			#print(self.movie_window.get_parent_window().window_lookup())
			imagesink.set_xwindow_id(self.movie_window.window.xid)
			Gdk.threads_leave()
def main():		
	w = Gtkvid()
	#Gdk.threads_init()
	if __name__ == '__main__':
    		Gtk.main()

main()	
#/home/mike/Downloads/Cheerleader.Academy.2.XXX.720p.Bluray.x264-Jiggly/Sample/jiggly-cheeleaaca-720p-sample.mkv
