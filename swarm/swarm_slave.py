#!/usr/bin/python

import time, sys, os
import logging
import urlparse
import httplib, cgi
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import urllib
from threading import Thread

import swarm_settings
		
class SlaveWebHandler(BaseHTTPRequestHandler):
	"""The http handler which accepts commands from the slave."""
	def do_GET(self):
		try:
			self.send_response(200)
			self.send_header('Content-type', 'text/plain')
			self.end_headers()
			self.wfile.write('This is the swarm slave server.')
		except IOError:
			self.send_error(404,'File Not Found: %s' % self.path)

	def do_POST(self):
		try:
			ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
			length = int(self.headers.getheader('content-length'))
			if ctype == 'application/x-www-form-urlencoded':
				qs = self.rfile.read(length)
				body = cgi.parse_qs(qs, keep_blank_values=1)
				self.server.slave_httpd.handle_post(body)
			else:
				logging.error('Received a POST of unexpected type: %s' % ctype)
			self.send_response(200)
			self.end_headers()
			self.wfile.write("<HTML>POST OK.<BR><BR>");
		except:
			logging.exception("Error in POST")
			pass

class SlaveHTTPD:
	"""The httpd wrapper which manages some of the message routing"""
	def __init__(self, swarm_slave, port=swarm_settings.SLAVE_WEB_PORT):
		self.port = port
		self.swarm_slave = swarm_slave
		self.server = HTTPServer(('', self.port), SlaveWebHandler)
		self.server.slave_httpd = self
		self.httpd_thread = SlaveHTTPD.HTTPDThread()
		self.httpd_thread.slave_httpd = self
		
	def start(self):
		self.httpd_thread.start()

	def stop(self):
		self.server.socket.close()
		self.server.server_close()

	class HTTPDThread(Thread):
		def run(self):
			self.slave_httpd.server.serve_forever()

	def handle_post(self, body):
		try:
			action = body[swarm_settings.ACTION_PARAMETER_NAME][0]
			message = body[swarm_settings.MESSAGE_PARAMETER_NAME][0]
			self.swarm_slave.receive_message(action, message)
		except (KeyError, IndexError):
			logging.exception('Received a POST with incorrect parameters: %s' % body)
		

class SwarmSlave:
	"""The class which manages the httpd and provides easy message passing functions"""
	def __init__(self, id):
		self.id = id
		self.slave_httpd = SlaveHTTPD(self)
		
	def start(self):
		self.slave_httpd.start()
	
	def stop(self):
		self.slave_httpd.stop()

	def receive_message(self, action, message):
		"""
		CHANGE ME:
		This is where you'd do your application specific work, like triggering a change in the slave hardware.
		"""
		print 'Slave received %s: "%s" from the master' % (action, message)

	def send_message(self, action, message):
		"""Send a message to the master"""
		params = urllib.urlencode({swarm_settings.ID_PARAMETER_NAME:self.id, swarm_settings.ACTION_PARAMETER_NAME:action, swarm_settings.MESSAGE_PARAMETER_NAME:message})
		headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
		try:
			conn = httplib.HTTPConnection('%s:%s' % (swarm_settings.MASTER_WEB_HOST, swarm_settings.MASTER_WEB_PORT))
			conn.request("POST", "/slave/message/", params, headers)
			response = conn.getresponse()
			response.read()
			conn.close()	
			return True
		except:
			return False

if __name__ == "__main__":
	usage_message = 'Usage: swarm_slave.py <slave id number>'
	if len(sys.argv) != 2:
		print usage_message
		sys.exit()
	try:
		id = int(sys.argv[1])
	except:
		print usage_message
		sys.exit()
		
	slave = SwarmSlave(id)
	slave.start()

	try:
		while True: time.sleep(10000)
	except KeyboardInterrupt:
		slave.stop()
		sys.exit()
		


		