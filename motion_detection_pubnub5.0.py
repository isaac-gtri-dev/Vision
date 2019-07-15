#THIS IS THE FINAL PRODUCT 
#imports for pubnub
#keep in mind pubnub is an indpendent server and has a limited amount you can send
from pubnub.callbacks import SubscribeCallback 
from pubnub.enums import PNStatusCategory  
from pubnub.pnconfiguration import PNConfiguration  
from pubnub.pubnub import PubNub 
from pubnub.pubnub import PubNub, SubscribeListener 
#imports for threading, time keeping/waiting, open cv(camera library), numpy, and for queues respectfully  
import threading 
import time  
from time import sleep   
import cv2
import numpy as np
import queue

pnconfig = PNConfiguration()
#keys needed to send and receive messages 
pnconfig.subscribe_key = "sub-c-bab9dc6c-912f-11e9-9769-e24cdeae5ee1" 
pnconfig.publish_key = "pub-c-14a2c33b-ff74-4bb7-8139-ff46eed621cc" 

#queue of "Motion Detected"s
q = queue.Queue()
 
pubnub = PubNub(pnconfig)
my_listener = SubscribeListener()


pubnub.add_listener(my_listener)
 
pubnub.subscribe().channels('awesomeChannel').execute()
q.queue.clear()



def publish_callback(envelope, status):
    # Check whether request successfully completed or not
    if not status.is_error():
        pass  # Message successfully published to specified channel.
    else:
        pass  # Handle message publish error. Check 'category' property to find out possible issue
        # because of which request did fail.
        # Request can be resent using: [status retry];
#Thread that sends messages
def SendMessage( threadName, delay):
	keep_going = True
	while keep_going:
		msg = q.get()
		pubnub.publish().channel('awesomeChannel').message(msg).pn_async(publish_callback)
		#wait 8 seconds
		sleep(8)
		q.queue.clear()
		
			
	print("Disconnected")
#Thread that listens for messages
def ListenMessage( threadName, delay):
	my_listener = SubscribeListener()

	pubnub.add_listener(my_listener)
	#Tells code what channel to connect to and to connect
	pubnub.subscribe().channels('awesomeChannel').execute()
	my_listener.wait_for_connect()
	print('connected')
	print ("starting to listen")
	result = my_listener.wait_for_message_on('awesomeChannel')
	keep_goin = True
	while keep_goin:
	#command to print what is sent
		print(result.message)
		result = my_listener.wait_for_message_on('awesomeChannel')
		if result.message == "bye":
			keep_goin = False
#Thread that detects motion			
def motiondetection( threadName, delay):
	capture = cv2.VideoCapture(0)
	iffirsttime = True
	fgbg = cv2.createBackgroundSubtractorMOG2(8, 6, True)
	#frame starts at zero
	frameCount = 0
	
	while(1): 

		ret, frame = capture.read()

		if not ret:
			break

		frameCount += 1
												#These vales used for changing frame size
		resizedFrame = cv2.resize(frame, (0, 0), fx=0.1, fy=0.1)

		fgmask = fgbg.apply(resizedFrame)

		count = np.count_nonzero(fgmask)

#If frame count is above number you want and pixel count change is above the other number 
		if (frameCount > 10 and count > 100): 
				
			q.put("Motion Detected")
				
		cv2.imshow('Frame', resizedFrame)
		#break ONLY frame with 'q'
		if cv2.waitKey(3)==ord('q'):
			break

	capture.release()
	cv2.destroyAllWindows()

# The list of threads in the script in order by how they show up in the script
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
