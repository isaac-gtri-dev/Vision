import numpy as np
import cv2

face_cascade = cv2.CascadeClassifier('/home/pi/opencv/data/haarcascades/haarcascade_frontalface_alt2.xml')


cap = cv2.VideoCapture(0)
while(True):
	#disp frame
	ret, frame = cap.read()
	
	gray = cv2.cvtColor(frame , cv2.COLOR_BGR2GRAY)
	faces = face_cascade.detectMultiScale(gray, scaleFactor = 1.5, minNeighbors = 5)
	for (x , y, w, h) in faces:
		print(x, y, w, h)
		roi_gray = gray[y:y + h, x : x + w] 
		roi_color = frame[y:y + h, x : x + w]
		img_item = "my-image.png"
		
		cv2.imwrite(img_item, roi_gray)
		
		
		#draw rectangle #(BGR)
		color = (255, 0 ,0)
		stroke = 4
		end_cord_x = x + w
		end_cord_y = y + h
		cv2.rectangle(frame , (x , y), (end_cord_x, end_cord_y), color, stroke) #frame, start coords, end coords
		
		#face recognition
		
		
		
		
	#cap image
	cv2.imshow('frame' , frame)
	if cv2.waitKey(20) & 0xFF == ord('q'):
		break
		



cap.release()
cv2.destroyAllWindows()
