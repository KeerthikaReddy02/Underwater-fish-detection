from flask import Flask
from ultralytics import YOLO
from flask import Flask,render_template, request
from flask import jsonify
from flask_cors import CORS, cross_origin
import os
# import cloudinary
import cv2
# import cloudinary.uploader
# from dotenv import load_dotenv


# Define a flask app
app = Flask(__name__)

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
    return totalMaxCount, totalMinCount, avgCount, output_path
    

def predictVideo(video):
    """
    Predict the video
    """
    # results = model(video, save=True, save_dir="predictions")
    # model(video, project="C:/Users/WELCOME/Documents/Keerthi_documents/VIT related/VIT others/Research Paper- Underwater/Flask app/", name="xxx")
    totalMaxCount,totalMinCount, avgCount, output_path = predictFinal(video)
    # results = model.predict(video, save=True,save_crop=True)
    # flag = 0
    # for result in results:
    #     print(result.__len__())
    #     path = result.path
    #     flag = 1
    #     break
    # if flag == 0:
    #     return "Oops faced with an error!"
    
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
    video = "Balistidae.mp4"
    results = predictVideo(video)
    return results


if __name__ == '__main__':
    app.run(debug=True)