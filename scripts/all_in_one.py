#!/usr/bin/python
"""

"""

import time, sys, os
from heartbeat_client import HeartbeatClient
from status_listener import StatusListener

class ExampleStatusListener(StatusListener):
	def handle_status(self, status):
		print 'The ExampleStatusListener received status: %s' % status

class ArtInfrastructureClient:
	def __init__(self):
		self.heartbeat_client = HeartbeatClient()
		self.status_listener = ExampleStatusListener()
	
	def start(self):
		self.heartbeat_client.start()
		self.status_listener.start()
	
	def stop(self):
		self.heartbeat_client.stop()
		self.status_listener.stop()

if __name__ == "__main__":
	ai_client = ArtInfrastructureClient()
	ai_client.start()
	try:
		while True: time.sleep(10000)
	except KeyboardInterrupt:
		ai_client.stop()
		sys.exit()