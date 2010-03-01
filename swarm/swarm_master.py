#!/usr/bin/python

import time, sys, os
from scripts.heartbeat_client import HeartbeatClient
from scripts.status_listener import StatusListener
import logging
import urlparse
import httplib, cgi
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import urllib
from threading import Thread

import swarm_settings

class MasterWebHandler(BaseHTTPRequestHandler):
	"""The http handler which accepts messages from the slaves."""
	def do_GET(self):
		try:
			self.send_response(200)
			self.send_header('Content-type', 'text/plain')
			self.end_headers()
			self.wfile.write('This is the swarm master server.')
		except IOError:
			self.send_error(404,'File Not Found: %s' % self.path)

	def do_POST(self):
		try:
			ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
			length = int(self.headers.getheader('content-length'))
			if ctype == 'application/x-www-form-urlencoded':
				qs = self.rfile.read(length)
				body = cgi.parse_qs(qs, keep_blank_values=1)
				self.server.master_httpd.handle_post(body)
			else:
				logging.error('Received a POST of unexpected type: %s' % ctype)
			self.send_response(200)
			self.end_headers()
			self.wfile.write("<HTML>POST OK.<BR><BR>");
		except:
			logging.exception("Error in POST")
			pass

class MasterHTTPD:
	"""The httpd wrapper for handling messages from the slaves"""
	def __init__(self, swarm_master, port=swarm_settings.MASTER_WEB_PORT):
		self.port = port
		self.swarm_master = swarm_master
		self.server = HTTPServer(('', self.port), MasterWebHandler)
		self.server.master_httpd = self
		self.httpd_thread = MasterHTTPD.HTTPDThread()
		self.httpd_thread.master_httpd = self
		
	def start(self):
		self.httpd_thread.start()

	def stop(self):
		self.server.socket.close()
		self.server.server_close()

	class HTTPDThread(Thread):
		def run(self):
			self.master_httpd.server.serve_forever()

	def handle_post(self, body):
		try:
			action = body[swarm_settings.ACTION_PARAMETER_NAME][0]
			message = body[swarm_settings.MESSAGE_PARAMETER_NAME][0]
			slave_id = body[swarm_settings.ID_PARAMETER_NAME][0]
			self.swarm_master.receive_message(slave_id, action, message)
		except (KeyError, IndexError):
			logging.exception('Received a POST with incorrect parameters: %s' % body)

class SwarmMaster:
	"""The class which manages all of the master's roles: heartbeat generator, status listener, and httpd"""
	def __init__(self, slave_infos=swarm_settings.SLAVE_INFOS):
		self.slave_infos = slave_infos
		self.heartbeat_client = HeartbeatClient()
		self.status_listener = SwarmMaster.SwarmStatusListener(self)
		self.master_httpd = MasterHTTPD(self)
		
	class SwarmStatusListener(StatusListener):
		def __init__(self, swarm_master):
			self.swarm_master = swarm_master
			StatusListener.__init__(self)
		def handle_status(self, status):
			"""
			CHANGE ME: This is where you'd implement your application's reaction
			to any tests you've defined.
			"""
			print 'The SwarmStatusListener received status: %s' % status
	
	def start(self):
		self.heartbeat_client.start()
		self.status_listener.start()
		self.master_httpd.start()
	
	def stop(self):
		self.heartbeat_client.stop()
		self.status_listener.stop()
		self.master_httpd.stop()

	def receive_message(self, slave_id, action, message):
		"""
		CHANGE ME: This is where you'd implement your application specific functions.
		You could triggering a change in the master hardware or use self.send_message(...)
		to trigger actions by the slaves.
		"""
		print 'Master received %s: "%s" from slave %s' % (action, message, slave_id)

	def send_message(self, slave_host, action, message):
		"""Send a message to a host"""
		params = urllib.urlencode({swarm_settings.ACTION_PARAMETER_NAME:action, swarm_settings.MESSAGE_PARAMETER_NAME:message})
		headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
		try:
			conn = httplib.HTTPConnection('%s:%s' % (slave_host, swarm_settings.SLAVE_WEB_PORT))
			conn.request("POST", "/master/message/", params, headers)
			response = conn.getresponse()
			response.read()
			conn.close()	
			return True
		except:
			return False

	def narrowcast_message(self, slave_id, action, message):
		"""Send a message to a single slave"""
		for slave_info in self.slave_infos:
			if slave_info[0] == slave_id:
				return self.send_message(slave_info[1], action, message)
		return false
		
	def broadcast_message(self, action, message):
		"""Send a message to all of the slaves"""
		for slave_info in self.slave_infos: 
			if not self.send_message(slave_info[1], action, message):
				print 'Error'

if __name__ == "__main__":
	master = SwarmMaster()
	master.start()
	
	try:
		while True: time.sleep(10000)
	except KeyboardInterrupt:
		master.stop()
		sys.exit()
		
# Copyright 2009 GORBET + BANERJEE (http://www.gorbetbanerjee.com/) Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

		