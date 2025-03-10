import numpy as np
import cv2
import tensorflow as tf

from keras.models import load_model
from keras.preprocessing.image import img_to_array
from keras.preprocessing import image

face_classifier = cv2.CascadeClassifier(r'C:\\Users\\binor\\Desktop\\All project\\Emotion detection\\haarcascade_frontalface_default (2).xml')
classifier = load_model(r'C:\\Users\\binor\\Desktop\\All project\\Emotion detection\\EmotionDetectionModel.h5')

emotion_labels = ['Angry','Disgust','Fear','Happy','Neutral','Sad','Surprise']

cap = cv2.VideoCapture(0)

while True:
	_, frame = cap.read()
	labels = []
	if cap is None:
		print("Error")
	else:
		gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
		faces = face_classifier.detectMultiScale(gray)

	for(x,y,w,h)in faces:
		cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,255),2)
		roi_gray = gray[y:y+h,x:x+w]
		roi_gray = cv2.resize(roi_gray,(48,48),interpolation=cv2.INTER_AREA)
		if np.sum([roi_gray])!=0:
			roi =roi_gray.astype("float")/255.0
			roi = img_to_array(roi)
			roi = np.expand_dims(roi, axis=0)
			prediction = classifier.predict(roi)[0]
			label = emotion_labels[np.argmax(prediction)]
			label_position= (x,y)
			cv2.putText(frame,label,label_position,cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
		else:
			cv2.putText(frame,"no Faces",(30,80),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
	cv2.imshow("Emotion Detected",frame)
	if cv2.waitKey(1) == ord("q"):
		break

cap.release()
cv2.destroyAllWindows()

			
