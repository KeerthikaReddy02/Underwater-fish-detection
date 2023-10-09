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

def predictVideo(video):
    """
    Predict the video
    """
    # results = model(video, save=True, save_dir="predictions")
    # model(video, project="C:/Users/WELCOME/Documents/Keerthi_documents/VIT related/VIT others/Research Paper- Underwater/Flask app/", name="xxx")
    results = model.predict(video, save=True)
    flag = 0
    for result in results:
        path = result.path
        flag = 1
        break
    if flag == 0:
        return "Oops faced with an error!"
    
    folder_path = 'runs/detect'
    sub_folders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]
    latest_sub_folder = max(sub_folders, key=lambda x: os.path.getctime(os.path.join(folder_path, x)))
    directory = folder_path + "/" + latest_sub_folder
    print(directory) 
    files = os.listdir(directory)
    latest_file = files[0]
    print(latest_file)
    dn = os.path.dirname(__file__)
    dn = dn.replace('\\', '/')
    # print(dn)
    path = directory + "/"+ latest_file
    newFileName = FrameCapture(path)
    print(newFileName)
    # newPath = directory +"/"+ newFileName
    # print(newPath)
    print(dn+"/"+newFileName)

    # cloudinary.config(cloud_name = os.getenv('CLOUD_NAME'), api_key=os.getenv('API_KEY'), 
    # api_secret=os.getenv('API_SECRET'))
    # upload_result = cloudinary.uploader.upload(path)
    # app.logger.info(upload_result)
    # return jsonify(upload_result)
    return {"path": dn+"/"+newFileName, "filename": newFileName}

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
    # return results
    # print(vid)
    # print(vid['video'].response)
    # print(vid['video'].filename)

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

    print("going to sleep")
    time.sleep(5)
    print(newFileName)
    results = predictVideo(newFileName)
    return results
    
    # except:
    #     print("Error")
    #     print("Going to sleep")
    #     time.sleep(20)
    
    # finally:  
    #     print("Woke up")
    #     results = predictVideo(newFileName)
    #     return results



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

    print("going to sleep")
    time.sleep(5)
    print(newFileName)
    results = predictVideo(newFileName)
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

    print("going to sleep")
    time.sleep(5)
    print(newFileName)
    results = predictVideo(newFileName)
    return results
    
    # data = request.get_json()
    # info = {'path': data.get('path')}
    # video = info['path']
    # vidObj = cv2.VideoCapture(video)
    # count = 0
    # success = 1
    # width= int(vidObj.get(cv2.CAP_PROP_FRAME_WIDTH))
    # height= int(vidObj.get(cv2.CAP_PROP_FRAME_HEIGHT))
    # fps = vidObj.get(cv2.CAP_PROP_FPS)
    # print('frames per second =',fps)
    # newFileName = "mygeneratedvideoClahe.mp4"
    # video = cv2.VideoWriter(newFileName, 0, fps, (width, height))
    # while success:

    #     success, frame = vidObj.read()
    #     hsv_img = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    #     h, s, v = hsv_img[:,:,0], hsv_img[:,:,1], hsv_img[:,:,2]
    #     clahe = cv2.createCLAHE(clipLimit = 10.0, tileGridSize = (8,8))
    #     v = clahe.apply(v)
    #     hsv_img = np.dstack((h,s,v))
    #     rgb = cv2.cvtColor(hsv_img, cv2.COLOR_HSV2RGB)

    #     count += 1
    #     video.write(rgb)

    
    # dn = os.path.dirname(__file__)
    # dn = dn.replace('\\', '/')
    # return {"path": dn+"/"+newFileName, "filename": newFileName}



@app.route('/sharpen')
def sharpen():
    video = "Ephippidae.mp4"
    vidObj = cv2.VideoCapture(video)
    count = 0
    success = 1
    width= int(vidObj.get(cv2.CAP_PROP_FRAME_WIDTH))
    height= int(vidObj.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = vidObj.get(cv2.CAP_PROP_FPS)
    print('frames per second =',fps)
    video = cv2.VideoWriter('mygeneratedvideoSharpen.mp4', 0, fps, (width, height))
    while success:

        success, frame = vidObj.read()
        # Create the sharpening kernel
        kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
        
        # Sharpen the image
        sharpened_image = cv2.filter2D(frame,-1,kernel)

        count += 1
        video.write(sharpened_image)





if __name__ == '__main__':
    app.run(debug=True)