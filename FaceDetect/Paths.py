'''
	Created on 28/2/2017.
	Objective: Get All video paths
	Created by : reh 
'''
import os
import re
import cv2,time

video_path = []
def videosPaths():
	for root, dirs, files in os.walk("/home/rehan/Videos/YawDD dataset/"):
		for file in files:
			if file.endswith(".avi"):
				video_path.append(os.path.join(root, file))
	return video_path

def totalVideos():
	return len(video_path)

