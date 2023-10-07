import cv2
import numpy as np
import os

def FrameCapture(path):

	vidObj = cv2.VideoCapture(path)
	count = 0
	success = 1
	width= int(vidObj.get(cv2.CAP_PROP_FRAME_WIDTH))
	height= int(vidObj.get(cv2.CAP_PROP_FRAME_HEIGHT))
	fps = vidObj.get(cv2.CAP_PROP_FPS)
	print('frames per second =',fps)
	video = cv2.VideoWriter('mygeneratedvideo.mp4', 0, fps, (width, height))
	while success:

		success, frame = vidObj.read()
		
		video.write(frame)
	return "mygeneratedvideo.mp4"
# Driver Code
if __name__ == '__main__':

	# Calling the function
	FrameCapture('Balistidae.avi')




