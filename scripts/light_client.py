#!/usr/bin/python

"""
This is a script to query and control bacnet lights using the art server's lighting API
From the command line: python bacnet_client.py
"""

import urllib
import pprint
import traceback
import datetime
import time
import sys

from art_settings import * # Look in art_settings.py for all of the runtime settings


class LightClient:
	"""A wrapper around the art server's bacnet light API"""
	def __init__(self):
		self.list_url = "http://%s/api/bnlight/"
		self.info_url = "http://%s/api/bnlight/%s/"
		self.value_url = "http://%s/api/bnlight/%s/value/"

	def fetch_list(self):
		"""Fetch a list of lights"""
		return self.fetch(self.list_url % ART_SERVER_HOST)

	def fetch_info(self, device_id):
		"""Fetch live information about a light"""
		return self.fetch(self.info_url % (ART_SERVER_HOST, device_id))

	def fetch_value(self, device_id):
		"""Fetch current level value of a light"""
		return self.fetch(self.value_url % (ART_SERVER_HOST, device_id))

	def set_level(self, device_id, new_level):
		"""Set the level of a light"""
		return self.post(self.value_url % (ART_SERVER_HOST, device_id), {'value':new_level })

	def post(self, url, parameters):
		params = urllib.urlencode(parameters)
		sock = urllib.urlopen(url, params)
		result = sock.read()
		sock.close()
		return result
		
	def fetch(self, url):
		sock = urllib.urlopen(url)
		result = sock.read()
		if sock.getcode() != 200:
			print "Error fetching %s: status code %s" % (url, sock.getcode())
			result = None
		sock.close()
		return result


USAGE_MESSAGE = 'usage: bacnet_client.py ["list"|"info"|"value"|"set"] <projector id> <new value>'

def main():
	try:
		action = sys.argv[1]
	except IndexError:
		print USAGE_MESSAGE
		return
	client = LightClient()
	if action == 'list':
		print client.fetch_list()
	elif action == 'info':
		try:
			device_id = sys.argv[2]
		except IndexError:
			print USAGE_MESSAGE
			return
		print client.fetch_info(device_id)
	elif action == 'value':
		try:
			device_id = sys.argv[2]
		except IndexError:
			print USAGE_MESSAGE
			return
		print client.fetch_value(device_id)
	elif action == 'set':
		try:
			device_id = sys.argv[2]
			new_value = sys.argv[3]
		except IndexError:
			print USAGE_MESSAGE
			return
		print client.set_level(device_id, new_value)
	else:
		print USAGE_MESSAGE
		return

if __name__ == '__main__':
	main()

# Copyright 2009 GORBET + BANERJEE (http://www.gorbetbanerjee.com/) Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

# Copyright 2009 GORBET + BANERJEE (http://www.gorbetbanerjee.com/) Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
