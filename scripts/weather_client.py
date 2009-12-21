#!/usr/bin/python

"""
This is a script which will fetch the current weather at the airport.

From the command line: python weather_client.py

WRITING YOUR OWN WEATHER CLIENT
Any environment which can make HTTP requests and parse XML can GET the weather data.
The URLs for the api endpoints are:
	http://<hostname>/api/weather/98113.api where 98113 could be any US zip code
	http://<hostname>/api/weather/airport/SJC.api where SJC could be any international airport code
The hostname is the one in the CLOUD_HOST variable in art_settings.py.
"""

import urllib
import pprint
import traceback
import datetime
import time

from art_settings import * # Look in art_settings.py for all of the runtime settings


class WeatherClient:
	"""A wrapper around the art cloud's weather API"""
	def __init__(self):
		self.weather_by_zip_url = "http://%s/api/weather/%s.xml"
		self.weather_by_airport_code_url = "http://%s/api/weather/airport/%s.xml"

	def fetch_weather_by_zip(self, zipcode=95113):
		"""Fetch the weather for any US zip code"""
		return self.fetch_xml(self.weather_by_zip_url % (CLOUD_HOST, zipcode))

	def fetch_weather_by_airport_code(self, airport_code='SJC'):
		"""Fetch the weather for any international airport code"""
		return self.fetch_xml(self.weather_by_airport_code_url % (CLOUD_HOST, airport_code))
		
	def fetch_xml(self, url):
		sock = urllib.urlopen(url)
		xml = sock.read()
		sock.close()
		return xml

if __name__ == "__main__":
	try:
		client = WeatherClient()
		print "FETCHING BY ZIPCODE"
		print client.fetch_weather_by_zip(95113)
		print "\n\nFETCHING BY AIRPORT CODE"
		print client.fetch_weather_by_airport_code('SJC')
	except:
		print "Could not fetch the weather: %s" % datetime.datetime.now()
		print pprint.pformat(traceback.format_exc())

# Copyright 2009 GORBET + BANERJEE (http://www.gorbetbanerjee.com/) Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
