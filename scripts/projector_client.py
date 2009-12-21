#!/usr/bin/python

"""
This is a script to query and control projectors using the art server's projector API
From the command line: python projector_client.py
"""

import urllib
import pprint
import traceback
import datetime
import time
import sys

from art_settings import * # Look in art_settings.py for all of the runtime settings


class ProjectorClient:
	"""A wrapper around the art server's projector API"""
	def __init__(self):
		self.projector_list_url = "http://%s/api/projector/"
		self.projector_info_url = "http://%s/api/projector/%s/info/"

	def fetch_projector_list(self):
		"""Fetch a list of projectors"""
		return self.fetch_xml(self.projector_list_url % ART_SERVER_HOST)

	def fetch_projector_info(self, projector_id):
		"""Fetch live information about a projector"""
		return self.fetch_xml(self.projector_info_url % (ART_SERVER_HOST, projector_id))

	def power_on_projector(self, projector_id):
		"""Send the power on command to the projector"""
		return self.post_xml(self.projector_info_url % (ART_SERVER_HOST, projector_id), {'power':'1'})

	def power_off_projector(self, projector_id):
		"""Send the power on command to the projector"""
		return self.post_xml(self.projector_info_url % (ART_SERVER_HOST, projector_id), {'power':'0'})

	def post_xml(self, url, parameters):
		params = urllib.urlencode(parameters)
		sock = urllib.urlopen(url, params)
		xml = sock.read()
		sock.close()
		return xml
		
	def fetch_xml(self, url):
		sock = urllib.urlopen(url)
		xml = sock.read()
		sock.close()
		return xml


USAGE_MESSAGE = 'usage: projector_client.py ["list"|"info"|"power_on"|"power_off"] [<projector id>]'

def main():
	try:
		action = sys.argv[1]
	except IndexError:
		print USAGE_MESSAGE
		return
	client = ProjectorClient()
	if action == 'list':
		print client.fetch_projector_list()
	elif action == 'info':
		try:
			projector_id = sys.argv[2]
		except IndexError:
			print USAGE_MESSAGE
			return
		print client.fetch_projector_info(projector_id)
	elif action == 'power_on':
		try:
			projector_id = sys.argv[2]
		except IndexError:
			print USAGE_MESSAGE
			return
		print client.power_on_projector(projector_id)
	elif action == 'power_off':
		try:
			projector_id = sys.argv[2]
		except IndexError:
			print USAGE_MESSAGE
			return
		print client.power_off_projector(projector_id)
	else:
		print USAGE_MESSAGE
		return

if __name__ == '__main__':
	main()

# Copyright 2009 GORBET + BANERJEE (http://www.gorbetbanerjee.com/) Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
