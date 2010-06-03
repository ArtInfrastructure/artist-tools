import sys
from suds.client import Client
# You will need suds in your python path: https://fedorahosted.org/suds/

"""
The FlightXML SOAP service provides a WSDL file which describes all of the methods the service provides.

Current information about the service is available on the San Jose Art Cloud wiki: http://sanjoseartcloud.org/wiki/FlightAware/

In the example code below you will see that the soap_client is initialized using the WSDL url, username, and API key.
Then in the enroute method the service is queried using the automatically generated Enroute method.

Here are all of the methods on the soap_client object at the moment:
AircraftType(xs:string type, )
AirportInfo(xs:string airportCode, )
AllAirports()
Arrived(xs:string airport, xs:int howMany, xs:string filter, xs:int offset, )
Departed(xs:string airport, xs:int howMany, xs:string filter, xs:int offset, )
Enroute(xs:string airport, xs:int howMany, xs:string filter, xs:int offset, )
FleetArrived(xs:string fleet, xs:int howMany, xs:int offset, )
FlightInfo(xs:string ident, xs:int howMany, )
GetLastTrack(xs:string ident, )
InFlightInfo(xs:string ident, )
LatLongsToDistance(xs:float lat1, xs:float lon1, xs:float lat2, xs:float lon2, )
LatLongsToHeading(xs:float lat1, xs:float lon1, xs:float lat2, xs:float lon2, )
METAR(xs:string airport, )
MapFlight_Beta(xs:string ident, xs:int mapHeight, xs:int mapWidth, )
NTAF(xs:string airport, )
RoutesBetweenAirports(xs:string origin, xs:string destination, )
Scheduled(xs:string airport, xs:int howMany, xs:string filter, xs:int offset, )
Search(xs:string query, xs:int howMany, xs:int offset, )
SearchCount(xs:string query, )
TAF(xs:string airport, )
TailOwner(xs:string ident, )
ZipcodeInfo(xs:string zipcode, )
blockIdentCheck(xs:string ident, )
countAirportOperations(xs:string airport, )

Using the enroute method as an example, you should be able to wrap any of the above service calls in a handy method on the FlightXMLClient.

"""

class FlightXMLClient:
	"""An example class which wraps the FlightXML API using a SOAP client which is generated at runtime via WSDL"""
	def __init__(self, username, api_key, wsdl_url='http://flightaware.com/commercial/flightxml/data/wsdl1.xml'):
		self.username = username
		self.api_key = api_key
		self.wsdl_url = wsdl_url
		self.soap_client = Client(wsdl_url, username=self.username, password=self.api_key)

	def enroute(self, airport_code='KSJC', index=0, page_size=10):
		"""An example of wrapping one of the methods on the SOAP client for easy use within your code.
		See the wsdl_info command for a way to print all the available methods."""
		return self.soap_client.service.Enroute(airport_code, page_size, '', index)

USAGE_MESSAGE = """flight_aware.py <username> <api_key> enroute # provides information about current flights
flight_aware.py <username> <api_key> wsdl_info # lists the methods available from the FlightXML service."""

def simple_example(username, api_key, wsdl_url='http://flightaware.com/commercial/flightxml/data/wsdl1.xml'):
	soap_client = Client(wsdl_url, username=username, password=api_key)

def main():
	if len(sys.argv) < 4:
		print USAGE_MESSAGE
		return

	username = sys.argv[1]
	api_key = sys.argv[2]
	client = FlightXMLClient(sys.argv[1], sys.argv[2])

	action = sys.argv[3]
	if action == 'enroute':
		print client.enroute()
		return
	if action == 'wsdl_info':
		print client.soap_client
		return
	else:
		print USAGE_MESSAGE
		return

if __name__ == '__main__': main()

# Copyright 2010 GORBET + BANERJEE (http://www.gorbetbanerjee.com/) Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.


