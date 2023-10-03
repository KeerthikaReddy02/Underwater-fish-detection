from flask import Flask
from ultralytics import YOLO
from flask import Flask,render_template, request
from flask import jsonify
from flask_cors import CORS, cross_origin
import os
import cloudinary
import cv2
import cloudinary.uploader
from dotenv import load_dotenv


# Define a flask app
app = Flask(__name__)

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

    path = directory + "/"+ latest_file

    # cloudinary.config(cloud_name = os.getenv('CLOUD_NAME'), api_key=os.getenv('API_KEY'), 
    # api_secret=os.getenv('API_SECRET'))
    # upload_result = cloudinary.uploader.upload(path)
    # app.logger.info(upload_result)
    # return jsonify(upload_result)
    return "Success"

@app.route('/')
def index():
    return "Hello World"


@app.route('/predict')
def predict():
    video = "mygeneratedvideo_white_patch.mp4"
    results = predictVideo(video)
    return results


if __name__ == '__main__':
    app.run(debug=True)