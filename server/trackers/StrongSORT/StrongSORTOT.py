import cv2
import torch
from ultralytics import YOLO
from strongsort import StrongSORT
from pathlib import Path
import json
import numpy as np

import sys
sys.path.append("../../")
from detectors.TorchVisionDetection import TorchVisionDetection


class StrongSORTOT:
    """Tracking class using StrongSORT."""
    def __init__(self, model_weights_path="osnet_x0_25_msmt17.pt", device="cuda", max_age=70, fp16=False,output_json="tracking_data.json"):

        self.tracker = StrongSORT(model_weights=Path(model_weights_path), device=device, max_age=max_age, fp16=fp16)
        self.device = device
        self.tracking_data = []
        self.output_json_path=output_json

    def run(self, video_path, detections_per_frame):

        cap = cv2.VideoCapture(video_path)
        frame_id = 0

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Get detections for the current frame
            frame_detections = next(
                (d["detections"] for d in detections_per_frame if d["frame"] == frame_id + 1), []
            )

            if not frame_detections:
                frame_id += 1
                continue

            # Prepare detections for tracking
            det_boxes = [
                [x1, y1, x2, y2, conf, -1] for x1, y1, x2, y2, conf in frame_detections
            ]

            # Perform tracking
            tracked_objects = self.update_tracking(det_boxes, frame, frame_id)
            self.save_tracking_data(tracked_objects, frame_id)

            frame_id += 1

        cap.release()

        # Write tracking data to JSON
        self.save_to_json(self.output_json_path)

    def update_tracking(self, detections, frame, frame_id):
        """Updates the tracker with detections for the current frame."""
        detections_tensor = torch.tensor(detections, dtype=torch.float32).to(self.device)
        tracked_objects = self.tracker.update(detections_tensor, frame)
        return tracked_objects

    def save_tracking_data(self, tracked_objects, frame_id):
        """Saves tracking data for the current frame."""
        for obj in tracked_objects:
            x1, y1, x2, y2, track_id = map(int, obj[:5])
            self.tracking_data.append({
                "frame_id": frame_id,
                "track_id": track_id,
                "bbox": [x1, y1, x2, y2],
            })

    def save_to_json(self, output_json_path):
        """Saves all tracking data to a JSON file."""
        with open(output_json_path, "w") as json_file:
            json.dump(self.tracking_data, json_file, indent=4)


# Main Logic
if __name__ == "__main__":
    device = "cuda" if torch.cuda.is_available() else "cpu"

    # Initialize Detector and Tracker
    video_path = "input_video.mp4"
    detector = TorchVisionDetection("ssdlite", confidence_threshold=0.5)
    detections = detector.detect(video_path)
    print(detections)
    tracker = StrongSORTOT(device=device)

    # Process video and save tracking results to JSON
    tracker.run(video_path="input_video.mp4", detections_per_frame=detections)

    # tracker.process_video(video_path="input_video.mp4", detections, output_json_path)

