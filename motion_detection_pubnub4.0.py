from pubnub.callbacks import SubscribeCallback 
from pubnub.enums import PNStatusCategory  
from pubnub.pnconfiguration import PNConfiguration  
from pubnub.pubnub import PubNub  
import threading 
import time  
from time import sleep 
from pubnub.pubnub import PubNub, SubscribeListener  
import cv2
import numpy as np
import queue
pnconfig = PNConfiguration() 
pnconfig.subscribe_key = "sub-c-bab9dc6c-912f-11e9-9769-e24cdeae5ee1" 
pnconfig.publish_key = "pub-c-14a2c33b-ff74-4bb7-8139-ff46eed621cc" 
q = queue.Queue()
 
pubnub = PubNub(pnconfig)
my_listener = SubscribeListener()


pubnub.add_listener(my_listener)
 
pubnub.subscribe().channels('awesomeChannel').execute()

def publish_callback(envelope, status):
    # Check whether request successfully completed or not
    if not status.is_error():
        pass  # Message successfully published to specified channel.
    else:
        pass  # Handle message publish error. Check 'category' property to find out possible issue
        # because of which request did fail.
        # Request can be resent using: [status retry];

def SendMessage( threadName, delay):
	keep_going = True
	while keep_going:
		msg = q.get()
		pubnub.publish().channel('awesomeChannel').message(msg).pn_async(publish_callback)
		sleep(8)
		q.queue.clear()
		
			
	print("Disconnected")
def ListenMessage( threadName, delay):
	my_listener = SubscribeListener()

	pubnub.add_listener(my_listener)
 
	pubnub.subscribe().channels('awesomeChannel').execute()
	my_listener.wait_for_connect()
	print('connected')
	print ("starting to listen")
	result = my_listener.wait_for_message_on('awesomeChannel')
	keep_goin = True
	while keep_goin:
	
		print(result.message)
		result = my_listener.wait_for_message_on('awesomeChannel')
		if result.message == "bye":
			keep_goin = False
			
def motiondetection( threadName, delay):
	capture = cv2.VideoCapture(0)

	fgbg = cv2.createBackgroundSubtractorMOG2(8, 6, True)

	frameCount = 0

	while(1): 

		ret, frame = capture.read()

		if not ret:
			break

		frameCount += 1
	
		resizedFrame = cv2.resize(frame, (0, 0), fx=0.1, fy=0.1)

		fgmask = fgbg.apply(resizedFrame)

		count = np.count_nonzero(fgmask)

	
		if (frameCount > 1 and count > 100):
			
			q.put("Motion Detected")
					
			
		cv2.imshow('Frame', resizedFrame)
	
		if cv2.waitKey(3)==ord('q'):
			break

	capture.release()
	cv2.destroyAllWindows()

# Create two threads as follows
try:
	x2 = threading.Thread(target=SendMessage, args=("two", 2))
	x2.start()
	
	#x1 = threading.Thread(target=ListenMessage, args=("one", 1))
	#x1.start()
	
	x3 = threading.Thread(target=motiondetection, args=("three", 3))
	x3.start()
	
except:
   print ("Error: unable to start thread")

while 1:
   pass
