#!/usr/bin/python
"""
	This script runs a server which listens for status messages from the art server.
	To connect it to your system, edit the handle_status function.
	To run external scripts for each status level, uncomment the lines including "os.system(...)"
	and replace the dummy path with the path to your scripts.
	
	To run this script you must have Python 2.4 or later.
	From the command line: python status_listener.py
	Press crtl-c to abort the script.
"""
import string
import cgi
import os, sys
import time
import logging
import urlparse
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import urllib
from threading import Thread

from art_settings import *

STATUS_PARAMETER_NAME = 'status'
TEST_PARAMETER_NAME = 'test'

class StatusWebHandler(BaseHTTPRequestHandler):
	"""The http handler which reads the status parameter and hands it to the handle_status function."""
	def do_GET(self):
		try:
			self.send_response(200)
			self.send_header('Content-type', 'text/html')
			self.end_headers()
			self.wfile.write('This is the art status listener')
		except IOError:
			self.send_error(404,'File Not Found: %s' % self.path)

	def do_POST(self):
		try:
			ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
			length = int(self.headers.getheader('content-length'))
			if ctype == 'application/x-www-form-urlencoded':
				try:
					qs = self.rfile.read(length)
					body = cgi.parse_qs(qs, keep_blank_values=1)
					self.server.status_listener.handle_status(body[STATUS_PARAMETER_NAME][0])
				except (KeyError, IndexError):
					logging.exception('Received a POST with no status parameter: %s' % ctype)
			else:
				logging.error('Received a POST of unexpected type: %s' % ctype)
			self.send_response(200)
			self.end_headers()
			self.wfile.write("<HTML>POST OK.<BR><BR>");
		except:
			logging.exception("Error in POST")
			pass

class StatusListener:
	"""A wrapper around the status listener API on the on-site server.
	test_names must be an array of strings which contain no commas.
	test_names are communicated to the status infrastructure and may be triggered
	by the art technician, in which case the string will be POSTed to your status listener.
	In this status listener, they will be passed into handle_status.
	"""
	def __init__(self, port=STATUS_WEB_PORT, test_names=[]):
		self.port = port
		self.test_names = test_names
		self.server = HTTPServer(('', self.port), StatusWebHandler)
		self.server.status_listener = self
		self.status_thread = StatusListener.StatusThread()
		self.status_thread.status_listener = self
		
	def start(self):
		if not self.register_listener():
			print 'Could not register with %s' % ART_SERVER_HOST
			return False
		self.status_thread.start()

	def stop(self):
		if not self.unregister_listener(): print 'Could not unregister with %s' % ART_SERVER_HOST
		self.server.socket.close()
		self.server.server_close()

	class StatusThread(Thread):
		def run(self):
			self.status_listener.server.serve_forever()
			
	def register_listener(self):
		try:
			params = urllib.urlencode({ 'register':self.port, 'tests':','.join(self.test_names) })
			f = urllib.urlopen("http://%s/status/" % ART_SERVER_HOST, params)
			f.read()
			return True
		except:
			return False

	def unregister_listener(self):
		try:
			params = urllib.urlencode({ 'unregister':self.port })
			f = urllib.urlopen("http://%s/status/" % ART_SERVER_HOST, params)
			f.read()
			return True
		except:
			return False

	def handle_status(self, status):
		"""Override this with your status handling implementation.
		If you have defined test_names then handle_status may receive those as status values
		"""
		if status == 'explode':
			print 'Status is explode'
			# os.system('/full/path/to/script/reactToExplode.sh')
		elif status == 'freeze-dry':
			print 'Status is freeze'
			# os.system('/full/path/to/script/reactToFreeze.sh')
		# this is where you'd add hooks for your test names
		else:
			print 'Unknown status %s' % status

if __name__ == '__main__':
	try:
		sl = StatusListener(test_names=['explode', 'freeze-dry'])
		sl.start()
		while True: time.sleep(10000000)
	except KeyboardInterrupt:
		sl.stop()
		sys.exit()

# Copyright 2009 GORBET + BANERJEE (http://www.gorbetbanerjee.com/) Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
