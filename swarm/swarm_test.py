#!/usr/bin/python
"""
This is a development debug script and not an actual test suite.
"""
import sys, time, os
from threading import Thread
import swarm_master
import swarm_slave

class TestMasterThread(Thread):
	def __init__(self, master):
		self.master = master
		Thread.__init__(self)
		
	def run(self):
		while True:
			time.sleep(3.5)
			if not self.master.broadcast_message('master-action', 'I like the letter blue.'):
				print 'The master could not broadcast the message'
			if not self.master.narrowcast_message(1, 'narrow-action', 'I like the color L.'):
				print 'The master could not narrowcast a message'

class TestSlaveThread(Thread):
	def __init__(self, slave):
		self.slave = slave
		Thread.__init__(self)
		
	def run(self):
		while True:
			time.sleep(2.5)
			if not self.slave.send_message('test-action', 'I like traffic lights.'):
				print 'The slave could not send a message to the master'
			
def run_tests():
	master = swarm_master.SwarmMaster(slave_infos=[(1, "127.0.0.1")])
	master.start()
	slave = swarm_slave.SwarmSlave(1)
	slave.start()

	master_thread = TestMasterThread(master)
	master_thread.start()
	slave_thread = TestSlaveThread(slave)
	slave_thread.start()

if __name__ == "__main__":
	run_tests()
	try:
		while True: time.sleep(10000)
	except KeyboardInterrupt:
		sys.exit()
