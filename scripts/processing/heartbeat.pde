// Processing sample code for SJC heartbeat

/*----------*/

// multithreaded class for heartbeat generation


// Create the object with the run() method
Heartbeat hbeat;
Thread hbthread;


void setup()
{

  //----

  //----  OTHER SETUP STUFF...

  //----


  // set up the heartbeat - format: url, number of seconds btw heartbeats

  Heartbeat hbeat = new Heartbeat("http://174.129.3.149/heartbeat/?installation_id=[INSERT SJC ID NUMBER HERE]", 240); 

  // Create the thread supplying it with the runnable object
  Thread hbthread = new Thread(hbeat);

  // Start the heartbeat thread
  hbthread.start();

}

//----

//---- THE REST OF YOUR PROCESSING CODE

//----


class Heartbeat implements Runnable {
  String url;
  public String info;
  int sleeptime;

  Heartbeat(String address, int interval) {
    url = address;
    sleeptime = interval;
    info = "";
  }

  void setInfo(String i) {
    info = i;
  }

  // This method is called when the thread runs
  public void run() {
    while(true) {

      try {
        Thread.sleep(sleeptime*1000);
      } 
      catch(InterruptedException e) {
        e.printStackTrace();
      }
      info = "";
      if(minute() > 22 && minute() < 27 && (hour()== 6 || hour() ==13 || hour() == 21)) {
        info = "Some interesting info here, reported at intervals or under conditions defined just above...";
        loadStrings(url+"&info="+info);  // access the heartbeat page with info
      }
      else {
        loadStrings(url);  // just send a heartbeat without extra info.
      }

      // println("Updated heartbeat: "+ info);
    }
  }
}

// Copyright 2009 GORBET + BANERJEE (http://www.gorbetbanerjee.com/) Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
