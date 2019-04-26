import paho.mqtt.client as mqtt
import pulsectl
import subprocess
import time
from threading import Thread
from time import sleep
from sets import Set

class Sink:
	def __init__(self, id, volume):
		self.id = id
		self.volume = volume

	def __hash__(self):
		return hash((self.id, self.volume))

	def __eq__(self, other):
		if not isinstance(other, type(self)): return NotImplemented
		return self.id == other.id