#!/usr/bin/python
from gi.repository import TotemPlParser

def pl_entry(parser, uri, htable):
  print uri

def parse_uri(uri):
  parser = TotemPlParser.Parser.new()
  parser.connect('entry-parsed', pl_entry)
  result = parser.parse(uri, False)

parse_uri('file:///home/mike/Desktop/Python/IconoClast/Sample Files/playlists/Play Queue (7).pls')
