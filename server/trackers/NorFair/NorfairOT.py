from norfair import Detection, Tracker, draw_tracked_objects
from ultralytics import YOLO  # Assuming YOLOv8
import cv2
import numpy as np
import json

import sys
sys.path.append("../../")
from detectors.Yolo import Yolo


class NorfairOT:
    def __init__(self,device="cuda",output_json="tracking_data_norfair.json"):
        self.tracker = Tracker(distance_function=lambda d, t: np.linalg.norm(d.points - t.estimate), distance_threshold=20)
        self.model=YOLO("yolov8m.pt")
        self.tracking_data = []
        self.output_json_path=output_json


    def run(self, video_path, detections):
        video = cv2.VideoCapture(video_path)
        frame_id = 0

        while video.isOpened():
            ret, frame = video.read()
            if not ret:
                break

            frame_detections = detections[frame_id]['detections'] if frame_id < len(detections) else []
            # Convert detections to Norfair format
            norfair_detections = []
            for detection in frame_detections:
                try:
                    # x1, y1, x2, y2, cnf = map(float, detection)
                    x1, y1, x2, y2, cnf = detection
                    center_x = (x1 + x2) / 2
                    center_y = (y1 + y2) / 2
                    norfair_detections.append(Detection(points=np.array([center_x, center_y])))
                except (ValueError, TypeError) as e:
                    print(f"Skipping invalid detection: {detection} - Error: {e}")

            tracked_objects = self.tracker.update(norfair_detections)

            self.save_tracked_objects(tracked_objects, frame_id)

            frame_id += 1

        video.release()
        self.save_to_json(self.output_json_path)
        
        
    def save_tracked_objects(self, tracked_objects, frame_id):
        for obj in tracked_objects:
            bbox = obj.estimate.flatten().tolist()
            self.tracking_data.append({
                "frame_id": frame_id,
                "track_id": obj.id,
                "bbox": bbox,
            })

    def save_to_json(self, output_json_path):
        """Saves all tracking data to a JSON file."""
        with open(output_json_path, "w") as json_file:
            json.dump(self.tracking_data, json_file, indent=4)


if __name__ == "__main__":
    
    detector = Yolo(model_path="yolov8m.pt")
    detections = detector.detect("input_video.mp4")

    # # print(detections)

    tracker = NorfairOT()
    tracker.run("input_video.mp4",detections)
