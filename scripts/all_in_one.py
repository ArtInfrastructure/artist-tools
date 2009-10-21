#!/usr/bin/python
"""
This demonstrates how to run both the heartbeat and status listener clients in order
to satisfy the requirements of art pieces using the art infrastructure.
"""

import time, sys, os
from heartbeat_client import HeartbeatClient
from status_listener import StatusListener

class ExampleStatusListener(StatusListener):
	def __init__(self):
		StatusListener.__init__(self, test_names=['Test One', 'Test Two'])
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

# Copyright 2009 GORBET + BANERJEE (http://www.gorbetbanerjee.com/) Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
