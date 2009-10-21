#!/usr/bin/python

"""
This is a script which will generate a heartbeat call to the art infrastructure.
If your piece does not send heartbeats the art technicial will be notified.


From the command line: python heartbeat_client.py
The script will periodically send the heartbeat to the art infrastructure and won't quit unless you stop the script.

TROUBLESHOOTING
If you run this script and get an error like "/usr/bin/python: bad interpreter: No such file or directory":
Find the python interpreter and set the first line in this file to reflect it's full path.
For example, if the python program is at /bin/python make the first line "#!/bin/python"

If you run this script get an error like "ImportError: No module named urllib":
Make certain that you have a full modern python (Python 2.5.1 at the time of writing) by running "python --version".
If you have a python older than 2.4, you will need to upgrade to a newer version.

If the script waits for a while and then spits out a bunch of errors that end with "Operation timed out":
Double check that your system can connect to the web server defined by the CLOUD_HOST variable below.

WRITING YOUR OWN HEARTBEAT CLIENT
Any environment which can make HTTP requests can generate heartbeats by periodically making a GET request.
The URL for the heartbeat receiver is: http://<hostname>/heartbeat/?installation_id=<id>
The hostname is the CLOUD_HOST variable in art_settings.py.
The installation id should be provided by the art technician.
Have your program GET that URL once a minute and the art infrastructure will handle the rest.

OPTIONALLY, you can add an info parameter which will be included in the database for easy access
via the art cloud web UI
For example: http://<hostname>/heartbeat/?installation_id=101&info=my%20art%20is%20faboo

Alternatively, you could load the heartbeat URL in your browser and manually hit reload every minute or so. ;-)
"""

import urllib
import pprint
import traceback
import datetime
import time, sys
from threading import Thread

from art_settings import *

INSTALLATION_ID_PARAMETER = 'installation_id'
INFO_PARAMETER = "info"

# The timeout after which the heartbeat system will signal failure if it hasn't heard from your piece
HEARTBEAT_TIMEOUT = 80 # in seconds
HEARTBEAT_PERIOD = HEARTBEAT_TIMEOUT / 2

class HeartbeatClient:
	def __init__(self, installation_id=INSTALLATION_ID):
		self.installation_id = installation_id
		self.heartbeat_url = "http://%s/heartbeat/?%s=%s"
		self.heartbeat_thread = HeartbeatClient.HeartbeatThread(self)

	def send_heartbeat(self, info=None):
		url = self.heartbeat_url % (CLOUD_HOST, INSTALLATION_ID_PARAMETER, INSTALLATION_ID)
		if info != None:
			url = '%s&%s=%s' % (url, INFO_PARAMETER, urllib.quote(info))
		sock = urllib.urlopen(url)
		sock.read()
		sock.close()

	class HeartbeatThread(Thread):
		def __init__(self, heartbeat_client):
			self.heartbeat_client = heartbeat_client
			self.should_run = True
			Thread.__init__(self)

		def run(self):
			while self.should_run:
				try:
					self.heartbeat_client.send_heartbeat()
				except:
					print "Could not send heartbeat: %s" % datetime.datetime.now()
					#print pprint.pformat(traceback.format_exc())
				time.sleep(HEARTBEAT_PERIOD)
			print 'thread finish'

	def start(self):
		self.heartbeat_thread.start()
	
	def stop(self):
		self.heartbeat_thread.should_run = False
		
if __name__ == "__main__":
	if INSTALLATION_ID == None:
		print "You must set the INSTALLATION_ID value in art_settings.py to the value given to you by the art technician."
	else:
		try:
			client = HeartbeatClient()
			client.start()
			while True: time.sleep(100000)
		except KeyboardInterrupt:
			client.stop()
			sys.exit()

# Copyright 2009 GORBET + BANERJEE (http://www.gorbetbanerjee.com/) Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
