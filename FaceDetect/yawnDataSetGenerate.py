'''
	Created on 28/2/2017.
	Objective: Read video --> detect Face --> detect eyes --> detect Mouth  -->save
	Created by : reh 
'''

import Paths
import globals
from globals import ClassifierFiles
import numpy as np
import cv2
import time
import dlib
import math
import eyeCoordinates
import mouthCoordinates
from globals import Threshold
from globals import yawnFolder
import os
import openface

#GLOBAL VARIABLES#
VIDEO_PATHS = []
yes = 0
no = 0
#GLOBAL VARIABLES#


def init():
	for video in range(globals.getVideoCount()):
		print(str(video) + "->" + VIDEO_PATHS[video])
		readVideo(VIDEO_PATHS[video])
	# # for video in range(2):
	# # 	readVideo(VIDEO_PATHS[3])
	# readVideo('v.avi')

		

def readVideo(video):
	global no,yes
	video_capture = cv2.VideoCapture(video)
	detector = dlib.get_frontal_face_detector() #Face detector
	predictor = dlib.shape_predictor(ClassifierFiles.shapePredicter) #Landmark identifier
	face_aligner = openface.AlignDlib(ClassifierFiles.shapePredicter)

	u = 0
	while True:
		ret, frame = video_capture.read()
		if frame != None:
			gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
			# clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
			# clahe_image = clahe.apply(gray)

			detections = detector(frame, 1) #Detect the faces in the image

			for k,d in enumerate(detections): #For each detected face
				shape = predictor(frame, d) #Get coordinates
				vec = np.empty([68, 2], dtype = int)
				coor = []
				for i in range(1,68): #There are 68 landmark points on each face
					#cv2.circle(frame, (shape.part(i).x, shape.part(i).y), 1, (0,0,255), thickness=1)
					coor.append([shape.part(i).x, shape.part(i).y])
					vec[i][0] = shape.part(i).x
					vec[i][1] = shape.part(i).y

				#RightEye and LeftEye coordinates
				rightEye = eyeCoordinates.distanceRightEye(coor)
				leftEye = eyeCoordinates.distanceLeftEye(coor)
				eyes = (rightEye + leftEye)/2

				#Mouth coordinates
				mouth = mouthCoordinates.distanceBetweenMouth(coor)

				print(eyes,mouth)

				alignedFace = face_aligner.align(400, frame, d, landmarkIndices=openface.AlignDlib.OUTER_EYES_AND_NOSE)

				if eyes <= Threshold.eye or mouth >= Threshold.mouth:
					cv2.imwrite(os.path.join(yawnFolder.yes, 'yawn_%d.jpg') % yes, alignedFace)
					yes = yes + 1
				else:
					cv2.imwrite(os.path.join(yawnFolder.no, 'yawnnot_%d.jpg') % no, alignedFace)
					no = no + 1

				#crop = frame[d.top():d.bottom(), d.left():d.right()]
				
			#cv2.imshow("image", crop) #Display the frame
		else:
			break

		if cv2.waitKey(1) & 0xFF == ord('q'):
			break



if __name__ == '__main__': 
	VIDEO_PATHS = Paths.videosPaths()
	init()
