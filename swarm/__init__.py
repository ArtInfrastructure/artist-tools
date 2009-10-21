"""
These scripts demonstrate how to set up a swarm of machines in a single art piece which,
together, interact correctly with the art infrastructure.

There is a single master machine which runs swarm_master.py
All of the other machines run swarm_slave.py <id number>

All communication between the machines is over HTTP.  The slaves can communicate with
the master and the master can broadcast messages to the slaves.

Setup:

Assuming that you have the entire artist-tools directory (specifically, the scripts and swarm directories) 
on both the master and slave maches, you should first edit the scripts/art_settings.py to set 
your INSTALLATION_ID to the integer which the art technician should have provided for you.

On each machine (master and slaves) open swarm/swarm_settings.py and set the following:

MASTER_WEB_HOST = "127.0.0.1" # the IP number of the master machine
MASTER_WEB_PORT = 8199 # it's ok to leave this unless there is a conflict

SLAVE_INFOS = [(1, "127.0.0.1")] # this should be an array of tuples, one for each slave: (<id number>, <slave IP#>)
SLAVE_WEB_PORT = 8299 # it's ok to leave this unless there is a conflict

To run the master, cd in the artist-tools directory and run the following:
export PYTHONPATH=.
swarm/swarm_master.py

To run the slave, cd into the artist-tools directory and run the following:
export PYTHONPATH=.
./swarm/swarm_slave.py <id number>  # replacing <id number> with the integer, of course

Now that you have a running master and slave you can edit the scripts to implement your
application specific functions.  Search in swarm_master.py and swarm_slave.py for CHANGE ME
to see the points in the code where you'll want to start.


"""