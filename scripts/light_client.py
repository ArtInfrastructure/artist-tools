#!/usr/bin/python

"""
This is a script to query and control lights using the art server's API
"""

import urllib
import pprint
import traceback
import datetime
import time
import sys

from art_settings import * # Look in art_settings.py for all of the runtime settings


class LightClient:
	"""A wrapper around the art server's projector API"""
	def __init__(self):
		self.light_url = "http://%s/api/bnlight/%s/value/"

	def fetch_light_value(self, light_id):
		url = self.light_url % (ART_SERVER_HOST, light_id)
		return urllib.urlopen(url).read()

	def set_light_value(self, light_id, new_value):
		url = self.light_url % (ART_SERVER_HOST, light_id)
		return urllib.urlopen(url, urllib.urlencode({'value':new_value})).read()

USAGE_MESSAGE = 'usage: light_client.py <light_id> [<new value>]'

def main():
	client = LightClient()
	if len(sys.argv) == 2:
		print client.fetch_light_value(sys.argv[1])
	elif len(sys.argv) == 3:
		print client.set_light_value(sys.argv[1], sys.argv[2])
	else:
		print USAGE_MESSAGE
		return

if __name__ == '__main__':
	main()

# Copyright 2009 GORBET + BANERJEE (http://www.gorbetbanerjee.com/) Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
