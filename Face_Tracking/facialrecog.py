import numpy as np
import cv2
import pickle
from pubnub.callbacks import SubscribeCallback 
from pubnub.enums import PNStatusCategory  
from pubnub.pnconfiguration import PNConfiguration  
from pubnub.pubnub import PubNub  
#pubnub configuration
pnconfig = PNConfiguration()
pnconfig.subscribe_key = "sub-c-bab9dc6c-912f-11e9-9769-e24cdeae5ee1"
pnconfig.publish_key = "pub-c-14a2c33b-ff74-4bb7-8139-ff46eed621cc"
pubnub = PubNub(pnconfig)
pubnub.EnableResumeOnreconnect = True
pubnub.subscribe().channels('awesomeChannel').execute()

def publish_callback(envelope, status):
	#error checks pb connection with voice module
	if not status.is_error():
		pass
	else:
		print("Connection error! Retrying")
		pass


face_cascade = cv2.CascadeClassifier('/home/pi/opencv-4.1.0/data/haarcascades/haarcascade_frontalface_alt2.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("trainer.yml")



labels = {}
with open("labels.pickle", "rb") as f:
	oldlabels = pickle.load(f)
	newlabels = {v:k for k,v in oldlabels.items()}
count = 0

cap = cv2.VideoCapture(0)
while(True):
	#disp frame
	ret, frame = cap.read()
	gray = cv2.cvtColor(frame , cv2.COLOR_BGR2GRAY)
	faces = face_cascade.detectMultiScale(gray, scaleFactor = 1.5, minNeighbors = 5)
	for (x , y, w, h) in faces:
		#print(x, y, w, h)
		roi_gray = gray[y:y + h, x : x + w] 
		roi_color = frame[y:y + h, x : x + w]
		
		#face recognition goes here
		id_, conf = recognizer.predict(roi_gray)
		if conf>=45: #and conf <= 85:
			#print(id_)
			#print(newlabels[id_])
			font = cv2.FONT_HERSHEY_SIMPLEX
			name = newlabels[id_] 
			#pubnub.publish().channel('awesomeChannel').message(name).pn_async(publish_callback)
			color = (255, 255, 255)
			stroke = 2
			cv2.putText(frame, name, (x,y), font, 1, color, stroke, cv2.LINE_AA)
			#publish
			
			#if id_ in newlabels == id_ :
			count += 1
			if count >= 5:
				pubnub.publish().channel('awesomeChannel').message(name).pn_async(publish_callback)
				count = 0
			
			
			
		img_item = "my-image.png"
		cv2.imwrite(img_item, roi_gray)
		
		
		#draw rectangle #(BGR) remove for final product
		color = (255, 0 ,0)
		stroke = 4
		end_cord_x = x + w
		end_cord_y = y + h
		#cv2.rectangle(frame , (x , y), (end_cord_x, end_cord_y), color, stroke) #frame, start coords, end coords
		
	
		
		
		
		
		
	#cap image
	cv2.imshow('frame' , frame)
	if cv2.waitKey(20) & 0xFF == ord('q'):
		break





cap.release()
cv2.destroyAllWindows()
