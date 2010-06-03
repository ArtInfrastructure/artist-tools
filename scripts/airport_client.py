#!/usr/bin/python

"""
This is a script which will fetch information from the airport flight information API.

This script uses lxml so you'll need to add it to your python site-packages:
easy_install.py lxml

"""

import urllib
import pprint
import traceback
from datetime import datetime
import time
import sys
from lxml import etree

from art_settings import * # Look in art_settings.py for all of the runtime settings

TIMESTAMP_FORMAT = '%Y-%m-%d %H:%M:%S'

def fetch_resource(url):
	sock = urllib.urlopen(url)
	xml = sock.read()
	sock.close()
	return xml

class FlightDataClient:
	"""Provides methods to query flight data."""
	def __init__(self, host, port=80):
		self.host = host
		self.port = port
		if port == 80:
			port_string = ''
		else:
			port_string = ':%s' % self.port
		self.api_url = 'http://%s%s/api/aodb/' % (self.host, port_string)

	def fetch_snapshots(self):
		"""Returns an array of tuples for snapshots: (timestamp, id)"""
		list_data = fetch_resource(self.api_url)
		photo_elements = etree.fromstring(list_data).xpath('//snapshot')
		result = []
		for element in photo_elements:
			result.append((datetime.strptime(element.get('timestamp').split('.')[0], TIMESTAMP_FORMAT), element.get('url').split('/')[5]))
		return result
	
	def fetch_latest_snapshot(self): return fetch_resource('%slatest.xml' % self.api_url)
	
	def fetch_snapshot(self, id): return fetch_resource('%s%s/' % (self.api_url, id))

USAGE_MESSAGE = 'airport_client.py [list|fetch|fetch-latest] <snapshot id>'

if __name__ == "__main__":
	try:
		action = sys.argv[1]
		client = FlightDataClient('127.0.0.1', 8000)
		if action == 'list':
			print client.fetch_snapshots()
		elif action == 'fetch':
			snap_id = sys.argv[2]
			print client.fetch_snapshot(snap_id)
		elif action == 'fetch-latest':
			print client.fetch_latest_snapshot()
		else:
			print USAGE_MESSAGE
	except IndexError:
		print USAGE_MESSAGE
		
# Copyright 2009 GORBET + BANERJEE (http://www.gorbetbanerjee.com/) Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
