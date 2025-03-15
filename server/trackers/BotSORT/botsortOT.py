import os
import json
import cv2
from ultralytics import YOLO  # Ensure ultralytics library is installed

class BotSortOT:
    def __init__(self, model_path: str, output_json='track_results_botsort.json'):

        # if not os.path.exists(model_path):
        #     raise FileNotFoundError(f"YOLO model file not found: {model_path}")
        self.model = YOLO(model_path)  # Load YOLO model
        self.output_json = output_json
        self.tracking_results = []

    def run(self, video_path: str):

        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found: {video_path}")

        # Open the video file
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise ValueError(f"Cannot open video: {video_path}")

          # To store tracking data

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break  # End of video

            # Run YOLO inference with built-in BoT-SORT
            results = self.model.track(frame, tracker="botsort.yaml", persist=True)

            # Extract tracked objects and add to results
            for track in results[0].boxes.data.cpu().numpy():
                obj = {
                    "frame_id": int(results[0].orig_shape[0]),  # Frame index
                    "id": int(track[4]),  # Object ID
                    "class": int(track[5]),  # Object class
                    "bbox": {
                        "x": float(track[0]),  # Bounding box X
                        "y": float(track[1]),  # Bounding box Y
                        "width": float(track[2] - track[0]),  # Bounding box width
                        "height": float(track[3] - track[1])  # Bounding box height
                    },
                    "confidence": float(track[6])  # Confidence score
                }
                self.tracking_results.append(obj)

        cap.release()

        self.save_results(self.output_json)


    def save_results(self, output_json):
        # Save results to a JSON file
        with open(output_json, "w") as f:
            json.dump(self.tracking_results, f, indent=4)
        print(f"Tracking results saved to: {output_json}")



