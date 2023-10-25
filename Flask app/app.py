from flask import Flask
from ultralytics import YOLO
from flask import Flask,render_template, request
from flask import jsonify
from flask_cors import CORS, cross_origin
# import base64
from convert import FrameCapture 
import time

import os
# import cloudinary
import cv2
# import cloudinary.uploader
# from dotenv import load_dotenv
import numpy as np
import json
 

# Define a flask app
app = Flask(__name__)
cors = CORS(app, resources={r"/YOURAPP/*": {"origins": "*"}})

# Load the model
model = YOLO("bestNew.pt")
print("Model Loaded")

def predictFinal(video):
    
    totalMaxCount = {}
    totalMinCount = {}
    totalCount = {}
    noOfFrames = {}
    avgCount = {}

    cap = cv2.VideoCapture(video)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    output_path = 'output.mp4'
    out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))


    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            og_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = og_frame.copy()
            results = model(frame, save=True,save_crop=True)
            names= [
            'Clownfish',
            'Blue Tang',
            'Trumpet Fish',
            'Moray Eel',
            'Manta Ray',
            'Giant Trevally',
            'Emperor Angelfish',
            'Green Chromis',
            'Humphead Wrasse',
            'Lion Fish',
            'Oriental Flying Gurnard',
            'Oriental Sweetlips',
            'Ribbon Eel',
            'Blue Shark',
            'Trigger Fish',
            'Parrot Fish',
            'Puffer Fish',
            'Mahi Mahi',
            'Pinnate Spadefish',
            'Mandarin Fish'
            ]

            #read image from path
            folder_path = 'runs/detect'
            sub_folders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]
            latest_sub_folder = max(sub_folders, key=lambda x: os.path.getctime(os.path.join(folder_path, x)))
            directory = folder_path + "/" + latest_sub_folder  
            path = directory + "/image0.jpg"
            img = cv2.imread(path) 

            out.write(img)         
            

            counter = {}
            for result in results:
                boxes = result.boxes  # Boxes object for bbox outputs
                probs = result.probs  # Class probabilities for classification outputs
                cls = boxes.cls.tolist()  # Convert tensor to list
                xyxy = boxes.xyxy
                conf = boxes.conf
                xywh = boxes.xywh  # box with xywh format, (N, 4)
                for class_index in cls:
                    class_name = names[int(class_index)]

                    if class_name in noOfFrames:
                        noOfFrames[class_name] += 1
                    else:
                        noOfFrames[class_name] = 1
                    # print("Class:", class_name)
                    if class_name in counter:
                        counter[class_name] += 1
                    else:
                        counter[class_name] = 1
                
                print(counter)
                for classes in counter:
                    if classes in totalMaxCount:
                        if counter[classes] > totalMaxCount[classes]:
                            totalMaxCount[classes] = counter[classes]
                    else:
                        totalMaxCount[classes] = counter[classes]
                
                for classes in counter:
                    if classes in totalMinCount:
                        if counter[classes] < totalMinCount[classes]:
                            totalMinCount[classes] = counter[classes]
                    else:
                        totalMinCount[classes] = counter[classes]
                
                for classes in counter:
                    if classes in totalCount:
                        totalCount[classes] += counter[classes]
                    else:
                        totalCount[classes] = counter[classes]

        else:
            break
    
    print("Total Max Count")
    print(totalMaxCount)
    print("Total Min Count")
    print(totalMinCount)

    for classes in totalCount:
        avgCount[classes] = totalCount[classes]/noOfFrames[classes]
    
    print("Average Count")
    print(avgCount)
    out.release()
    cap.release()


    return totalMaxCount, totalMinCount, avgCount, output_path
 

def predictVideo(video):
    """
    Predict the video
    """
    totalMaxCount,totalMinCount, avgCount, output_path = predictFinal(video)

    dn = os.path.dirname(__file__)
    dn = dn.replace('\\', '/')
    # print(dn)
    path = dn + "/"+ output_path
    newFileName = FrameCapture(path)
    # print(newFileName)
    newPath = dn +"/"+ newFileName

    return {"path": newPath, "filename": newFileName, "totalMaxCount": totalMaxCount, "totalMinCount": totalMinCount, "avgCount": avgCount}

@app.route('/')
def index():
    return "Hello World"


@app.route('/predict', methods=['POST'])
def predict():
    # video = "mygeneratedvideo_white_patch.mp4"
    data = request.get_json()
    info = {'path': data.get('path')}
    vid = info['path']
    print(vid)
    results = predictVideo(vid)
    print(results)


    return results

@app.route('/histeq', methods=['POST'])
def histeq():
    
    
    data = request.get_json()
    info = {'path': data.get('path')}
    video = info['path']
    vidObj = cv2.VideoCapture(video)
    count = 0
    success = 1
    width= int(vidObj.get(cv2.CAP_PROP_FRAME_WIDTH))
    height= int(vidObj.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = vidObj.get(cv2.CAP_PROP_FPS)
    print('frames per second =',fps)
    newFileName = "mygeneratedvideoHist.mp4"

    # try:
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(newFileName, fourcc , fps, (width, height))
    while success:

        success, frame = vidObj.read()
        
        if(frame is not None):
            img_yuv = cv2.cvtColor(frame,cv2.COLOR_BGR2YUV)
            img_yuv[:,:,0] = cv2.equalizeHist(img_yuv[:,:,0])
            if(img_yuv is not None):
                hist_eq = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)
                count += 1
                video.write(hist_eq)

    video.release()

    print(newFileName)

    finalFileName = FrameCapture(newFileName)
    results = predictVideo(finalFileName)
    return results



@app.route('/denoise' , methods=['POST'])
def denoise():

    data = request.get_json()
    info = {'path': data.get('path')}
    video = info['path']
    vidObj = cv2.VideoCapture(video)
    count = 0
    success = 1
    width= int(vidObj.get(cv2.CAP_PROP_FRAME_WIDTH))
    height= int(vidObj.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = vidObj.get(cv2.CAP_PROP_FPS)
    print('frames per second =',fps)
    newFileName = "mygeneratedvideoDenoise.mp4"

    # try:
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(newFileName, fourcc , fps, (width, height))
    while success:

        success, frame = vidObj.read()
        print("Frame reading")
        
        if(frame is not None):
            dst = cv2.fastNlMeansDenoisingColored(frame, None, 10, 10, 7, 15)
            if(dst is not None):
                count += 1
                video.write(dst)

    video.release()

    print(newFileName)
    finalFileName = FrameCapture(newFileName)
    results = predictVideo(finalFileName)
    return results


@app.route('/clahe', methods=['POST'])
def clahe():

    data = request.get_json()
    info = {'path': data.get('path')}
    video = info['path']
    vidObj = cv2.VideoCapture(video)
    count = 0
    success = 1
    width= int(vidObj.get(cv2.CAP_PROP_FRAME_WIDTH))
    height= int(vidObj.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = vidObj.get(cv2.CAP_PROP_FPS)
    print('frames per second =',fps)
    newFileName = "mygeneratedvideoClahe.mp4"

    # try:
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(newFileName, fourcc , fps, (width, height))
    while success:

        success, frame = vidObj.read()
        
        if(frame is not None):
            hsv_img = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            h, s, v = hsv_img[:,:,0], hsv_img[:,:,1], hsv_img[:,:,2]
            clahe = cv2.createCLAHE(clipLimit = 10.0, tileGridSize = (8,8))
            v = clahe.apply(v)
            hsv_img = np.dstack((h,s,v))
            if(hsv_img is not None):
                rgb = cv2.cvtColor(hsv_img, cv2.COLOR_HSV2RGB)
                count += 1
                video.write(rgb)

    video.release()

    print(newFileName)
    finalFileName = FrameCapture(newFileName)
    results = predictVideo(finalFileName)
    return results
    

if __name__ == '__main__':
    app.run(debug=True)