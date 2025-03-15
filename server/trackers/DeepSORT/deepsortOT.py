import cv2
import json
import sys
import numpy as np
from trackers.DeepSORT.deep_sort.deep_sort import DeepSort
# from deep_sort.deep_sort import DeepSort
# # from ...detectors.Yolo import Yolo
# sys.path.append("../../")
# from detectors.Yolo import Yolo


class DeepSortOT:
    def __init__(self, output_json="tracking_data.json"):
        self.tracker = DeepSort(model_path="trackers/DeepSORT/deep_sort/deep/checkpoint/ckpt.t7", max_age=70)
        self.tracking_data = []
        self.output_json = output_json

    def run(self, detections, video_path):
        cap = cv2.VideoCapture(video_path)

        if not cap.isOpened():
            print(f"Error: Cannot open video file {video_path}")
            return []

        frame_idx = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Process only if detections exist for this frame
            frame_detections = next((d['detections'] for d in detections if d['frame'] == frame_idx + 1), [])
            if frame_detections:
                bbox = np.array([det[:4] for det in frame_detections], dtype=np.float32)
                conf = np.array([det[4] for det in frame_detections], dtype=np.float32)

                tracks = self.tracker.update(bbox, conf, frame)
                for track in self.tracker.tracker.tracks:
                    track_id = track.track_id
                    x1, y1, x2, y2 = track.to_tlbr()

                    self.tracking_data.append({
                        "track_id": track_id,
                        "bbox": [x1, y1, x2, y2],
                        "frame": frame_idx + 1
                    })

            frame_idx += 1

        cap.release()
        self.save_tracking_data()
        return self.tracking_data

    def save_tracking_data(self):
        with open(self.output_json, 'w') as json_file:
            json.dump(self.tracking_data, json_file, indent=4)
        print(f"Tracking data saved to {self.output_json}")


if __name__ == "__main__":
    video_path = "input_video.mp4"
    output_json = "tracking_results.json"
     # Assuming Yolo is in detection_tracking_classes.py
    detector = Yolo(model_path="yolov8m.pt")
    detections = detector.detect(video_path)

    tracker = Tracker(tracker_model_path="deep_sort/deep/checkpoint/ckpt.t7")
    tracking_data = tracker.track(detections, video_path)

    tracker.save_tracking_data(output_json)
