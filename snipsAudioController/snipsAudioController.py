import paho.mqtt.client as mqtt
import pulsectl
import subprocess
import time
from threading import Thread
from time import sleep
from sets import Set
from sink import Sink

HOST = '127.0.0.1'
PORT = 1883
SUBTOPIC = [('hermes/dialogueManager/sessionStarted', 0), ('hermes/dialogueManager/sessionEnded', 0)]
IS_WORKING = False
SINKS = Set()

def on_connect(client, userdata, flags, rc):
    print("Connected to {0} with result code {1}".format(HOST, rc))
    client.subscribe(SUBTOPIC)

def on_message(client, userdata, msg):
    if "hermes/dialogueManager/sessionStarted" == msg.topic:
		print("start detected")
		start = time.time()
		IS_WORKING = True;
		for sink in SINKS:
			print("before calc")
			print(sink.volume)
			print("new vol: " + str(int(sink.volume)/2))
			print("after calc")
			sink.volume = int(sink.volume)/2
			try:
				subprocess.Popen("sudo /home/respeaker/snipsAudio/./pulsemixer --id " + sink.id + " --set-volume " + str(sink.volume), stdout=subprocess.PIPE, shell=True)
			except:
				SINKS.remove(sink)
		print("detected")
		end = time.time()
		print(end - start)

		print("detected")
		end = time.time()
		print("Took: ")
		print(end - start)
    elif "hermes/dialogueManager/sessionEnded" == msg.topic:
		for sink in SINKS:
			sink.volume = int(sink.volume)*2
			subprocess.Popen("sudo /home/respeaker/snipsAudio/./pulsemixer --id " + sink.id + " --set-volume " + str(sink.volume), stdout=subprocess.PIPE, shell=True)
		print("ended")
		IS_WORKING = False;

def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

def find_between_r( s, first, last ):
    try:
        start = s.rindex( first ) + len( first )
        end = s.rindex( last, start )
        return s[start:end]
    except ValueError:
        return ""

def search_sinks():
	while True:
		if IS_WORKING == False:
			print("searching sinks...")
			p = subprocess.Popen("sudo /home/respeaker/snipsAudio/./pulsemixer --get-volume", stdout=subprocess.PIPE,shell=True)
			(output, err) = p.communicate()
			p_status = p.wait()
			p = subprocess.Popen("sudo /home/respeaker/snipsAudio/./pulsemixer --list", stdout=subprocess.PIPE, shell=True)
			(output, err) = p.communicate()
			p_status = p.wait()
			lines = output.splitlines()
			for line in lines:
				if line.startswith('Sink input:'):
					if line.find("snips") == -1:
						id = find_between(line,"ID: ", ",")
						SINKS.add(Sink(id, 0))
			for sink in SINKS:
				p = subprocess.Popen("sudo /home/respeaker/snipsAudio/./pulsemixer --id " + sink.id + " --get-volume", stdout=subprocess.PIPE, shell=True)
				(output, err) = p.communicate()
				p_status = p.wait()
				sink.volume = find_between(output, "", " ")
				print("Sink: " + sink.id + " has volume: " + sink.volume)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(HOST, PORT, 60)
t = Thread(target=search_sinks)
t.start()
client.loop_forever()


class Sink:
	def __init__(self, id, volume):
		self.id = id
		self.volume = volume

	def __hash__(self):
		return hash((self.id, self.volume))

	def __eq__(self, other):
		if not isinstance(other, type(self)): return NotImplemented
		return self.id == other.id