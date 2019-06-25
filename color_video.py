import numpy as np
import cv2
cap = cv2.VideoCapture(0)

while(True):
    ret, frame = cap.read()
    cv2.imshow('frame',frame)
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, miniNeighbors=5
    for(x, y, w, h) in faces:
        print(x,y)
    check, frame = cap.read()
    print(frame)
    
    if cv2.waitKey(20) & 0xff == ord('q'):
        break
        
cap.release()
cv2.destroyAllWindows()
