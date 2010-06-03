package org.sanjoseartcloud.flightxml;

import com.flightaware.flightxml.*; //these classes are generated in the build phase of the ant build.xml using WSDL
import javax.xml.rpc.ServiceException;
import java.rmi.RemoteException;

/**
This example uses dynamically generated classes in order to talk with the SOAP service for FlightXML.

The FlightXMLExample.print_enroute and FlightXMLExample.matar methods are examples of wrapping the dynamically generated classes with a handy method.

Once you've run the build target in the ant build.xml, look in the "generate" directory to see all of the classes and methods which are available in the API.

*/

class FlightXMLExample {
	
	String username = null;
	String apiKey = null;

	DirectFlightLocator locator = new DirectFlightLocator();
	DirectFlightSoap df = locator.getDirectFlightSoap();
	DirectFlightSoapStub stub = (DirectFlightSoapStub)df;
	
	public FlightXMLExample(String username, String apiKey) throws ServiceException, RemoteException {
		this.username = username;
		this.apiKey = apiKey;
		stub.setUsername(this.username);
		stub.setPassword(this.apiKey);
	}

	public void print_enroute(String airportCode) throws ServiceException, RemoteException {
		EnrouteStruct r = df.enroute(airportCode, 10, "", 0);
		for (EnrouteFlightStruct e: r.getEnroute()) {
			System.out.println(e.getIdent());
		}
	}

	public String metar(String airportCode) throws ServiceException, RemoteException {
	 	return df.METAR(airportCode);
	}

	public static String USAGE_MESSAGE = "FlightXMLExample <username> <api-key> enroute";
	
    public static void main(String[] args) {
		if(args.length < 3){
			System.err.println(USAGE_MESSAGE);
			return;
		}
		try {
			FlightXMLExample fx = new FlightXMLExample(args[0], args[1]);
			if("enroute".equals(args[2])){
				fx.print_enroute("KSJC");
			} else if("metar".equals(args[2])) {
				System.out.println(fx.metar("KSJC"));
			} else {
				System.err.println(USAGE_MESSAGE);
				return;
			}
		} catch (Exception e){
			e.printStackTrace();
		}
    }
}