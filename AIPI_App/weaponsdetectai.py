from ultralytics import YOLO
import os
import cv2
from os.path import join 
from ThemisAppAIPI.settings import BASE_DIR

def WeaponsDetectionFromImageAI(img_dir):
    model_weight_dir =  r'.' + r'\static\weaponsWeight\best.pt'
    print(model_weight_dir)
    model = YOLO(model_weight_dir)
    print(model)
    print(img_dir)
    results = model.predict(img_dir)  # predict on an image
    result = results[0]
    print(result)
    output = []
    for box in result.boxes:
        x1, y1, x2, y2 = [
            round(x) for x in box.xyxy[0].tolist()
        ]
        class_id = box.cls[0].item()
        prob = round(box.conf[0].item(), 2)
        output.append([
            x1, y1, x2, y2, result.names[class_id], prob
        ])
    return output


def WeaponsDetectedImgStore(img_dir, imgname):
    # img_dir = join(BASE_DIR, img_dir)
    img_dir = '.' + img_dir
    img = cv2.imread(img_dir)
    print(img.shape)
    outpath = r'.' + r'\static\weaponsDetect'
    # if not os.path.exists(outpath):
    #     os.mkdir(outpath)
    detect_output = WeaponsDetectionFromImageAI(img_dir)
    for i in range(0, len(detect_output)):
        x1, y1, x2, y2, classname,  conf =  detect_output[i]
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        new_image = cv2.putText(
        img = img,
        text = classname,
        org = (x1, y1-5),
        fontFace = cv2.FONT_HERSHEY_SIMPLEX,
        fontScale = 1.0,
        color = (125, 246, 55),
        thickness = 2
        )
        cv2.imwrite(join(outpath, imgname), new_image)



def WeaponsDetectedVideoFunc(videodir):
    outpath = r'.' + r'\static\weaponsDetect'
    # if not os.path.exists(outpath):
    #     os.mkdir(outpath)
    video_dir = '.' + videodir
    modelweight_dir = r'.' + r'\static\weaponsWeight\best.pt'
    model = YOLO(modelweight_dir) 
    results = model(video_dir, save=True, project= outpath)
    confirmation_result = "Successful"
    return confirmation_result
    
    

