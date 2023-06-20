import cv2
import pickle
import face_recognition
from django.urls import reverse
from django.http import HttpResponseRedirect
import supervision as sv
from ultralytics import YOLO
import uuid
from os.path import join


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def predict(rgb_frame, knn_clf=None, model_path=None, distance_threshold=0.5):
    if knn_clf is None and model_path is None:
        raise Exception("Must supply knn classifier either thourgh knn_clf or model_path")

    # Load a trained KNN model (if one was passed in)
    if knn_clf is None:
        with open(model_path, 'rb') as f:
            knn_clf = pickle.load(f)
    X_face_locations = face_recognition.face_locations(rgb_frame, number_of_times_to_upsample=2)
    if len(X_face_locations) == 0:
        return []
    faces_encodings = face_recognition.face_encodings(rgb_frame, known_face_locations=X_face_locations)
    closest_distances = knn_clf.kneighbors(faces_encodings, n_neighbors=1)
    are_matches = [closest_distances[0][i][0] <= distance_threshold for i in range(len(X_face_locations))]
    return [(pred, loc) if rec else ("unknown", loc) for pred, loc, rec in zip(knn_clf.predict(faces_encodings), X_face_locations, are_matches)]



# if __name__ == "__main__":
def stream():
    video_capture = cv2.VideoCapture(0)

    process_this_frame = True

    while True:
        # Grab a single frame of video
        ret, frame = video_capture.read()

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_frame = small_frame[:, :, ::-1]

        if process_this_frame:
            predictions = predict(rgb_frame, model_path="AIPI_App/Model/trained_model.clf")
            # print(predictions)

        process_this_frame = not process_this_frame

        for name, (top, right, bottom, left) in predictions:

            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)


        # Display the resulting image
        cv2.imshow('Video', frame)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()



def weaponsStream():
    # to save the video
    outpath = join(r'.' + r'\static\weaponsDetect' ,  uuid.uuid1().hex +'mp4' )
    writer= cv2.VideoWriter(outpath,
                            cv2.VideoWriter_fourcc(*'DIVX'), 
                            7, 
                            (1280, 720))
    
    # define resolution
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    # specify the model
    modelweight_dir = r'.' + r'\static\weaponsWeight\best.pt'
    model = YOLO(modelweight_dir)

    # customize the bounding box
    box_annotator = sv.BoxAnnotator(
        thickness=2,
        text_thickness=2,
        text_scale=1
    )

    while True:
        # Grab a single frame of video
        ret, frame = cap.read()
        result = model(frame, agnostic_nms=True)[0]
        
        detections = sv.Detections.from_yolov8(result)
        labels = [
            f"{model.model.names[class_id]} {confidence:0.2f}"
            for _, confidence, class_id, _
            in detections
        ]
        frame = box_annotator.annotate(
            scene=frame, 
            detections=detections, 
            labels=labels
        ) 
        # Display the resulting image
        cv2.imshow('Video', frame)

        writer.write(frame)
        
        cv2.imshow("yolov8", frame)

        if (cv2.waitKey(30) == 27): # break with escape key
            break

    cap.release()
    writer.release()
    cv2.destroyAllWindows()