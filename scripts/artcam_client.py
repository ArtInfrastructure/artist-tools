#!/usr/bin/python

"""
This is a script which will fetch still images and stream information from art cameras.

This script uses lxml so you'll need to add it to your python site-packages:
easy_install.py lxml

"""

import urllib
import pprint
import traceback
import datetime
import time
from lxml import etree

from art_settings import * # Look in art_settings.py for all of the runtime settings

def fetch_xml(url):
	sock = urllib.urlopen(url)
	xml = sock.read()
	sock.close()
	return xml

class ArtcamManager:
	"""Provides methods to query for art cam information."""
	def __init__(self, art_server_host):
		self.art_server_host = art_server_host

	def fetch_artcams(self):
		"""Fetch the list of artcams from the art server and return them as an array of ArtcamClient objects"""
		list_data = fetch_xml('http://%s/api/artcam/' % self.art_server_host)
		artcam_elements = etree.fromstring(list_data).xpath('//artcam')
		return [ArtcamClient(self, element.get('id'), element.get('name'), element.get('ip'), element.get('port')) for element in artcam_elements]

class ArtcamClient:
	"""Provides methods to query art cams."""
	def __init__(self, manager, artcam_id, name, ip, port):
		self.manager = manager
		self.artcam_id = artcam_id
		self.name = name
		self.ip = ip
		self.port = port

	def fetch_photos(self):
		list_data = fetch_xml('http://%s/api/artcam/%s/photo/' % (self.manager.art_server_host, self.artcam_id))
		photo_elements = etree.fromstring(list_data).xpath('//artcamphoto')
		result = []
		for element in photo_elements:
			image_element = element.xpath('//image')[0]
			result.append(ArtcamPhoto(self.manager, self.artcam_id, element.get('id'), element.get('created'), image_element.get('name'), image_element.get('width'), image_element.get('height')))
		return result

	def __get_domain(self):
		if not self.port or self.port == 80: return str(self.ip)
		return '%s:%s' % (self.ip, self.port)
	def __set_domain(self, domain): pass
	domain = property(__get_domain, __set_domain)

class ArtcamPhoto:
	"""Wraps the information for an artcam photo"""
	def __init__(self, manager, artcam_id, photo_id, created, name, width, height):
		self.manager = manager
		self.artcam_id = artcam_id
		self.photo_id = photo_id
		self.created = created
		self.name = name
		self.width = width
		self.height = height
		
	def __get_photo_url(self):
		return 'http://%s/media/%s' % (self.manager.art_server_host, self.name)
	def __set_photo_url(self, url): pass
	photo_url = property(__get_photo_url, __set_photo_url)

if __name__ == "__main__":
	try:
		manager = ArtcamManager(ART_SERVER_HOST)
		clients = manager.fetch_artcams()
		for client in clients:
			print 'Artcam at', client.domain
			for photo in client.fetch_photos():
				print '\tphoto', photo.photo_id, 'created:', photo.created, 'name:', photo.name, 'width:', photo.width, 'height:', photo.height
				print '\t\tphoto url:', photo.photo_url
	except:
		print pprint.pformat(traceback.format_exc())

# Copyright 2009 GORBET + BANERJEE (http://www.gorbetbanerjee.com/) Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
