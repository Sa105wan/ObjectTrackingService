import cv2
import numpy as np
import json
import sys
from trackers.SORT.sort.sort import Sort
# for running through main function
# from sort.sort import Sort
# sys.path.append("../../detectors")
# from Yolo import Yolo


class SortOT:
    def __init__(self, output_json='tracking_data.json'):
        self.tracker = Sort()
        self.output_json = output_json
        self.tracking_results = []

    def track(self, detections):
        for frame_data in detections:
            frame = frame_data['frame']
            # frame_detections = detections[frame]['detections'] if frame < len(detections) else []
            # dets = np.array(frame_detections)
            dets = np.array(frame_data['detections'])  # Convert to NumPy array

            if dets.size == 0:
                self.tracking_results.append({
                    'frame': frame,
                    'track_id': None,
                    'bbox': []
                })
                continue

            # Update SORT tracker with detections
            tracks = self.tracker.update(dets)

            # Save tracking results
            for track in tracks:
                x1, y1, x2, y2, track_id = map(int, track)
                self.tracking_results.append({
                    'frame': frame,
                    'track_id': track_id,
                    'bbox': [x1, y1, x2, y2]
                })
        print("Tracking completed!")
        self.save_tracking_data()

    def save_tracking_data(self):
        with open(self.output_json, 'w') as json_file:
            json.dump(self.tracking_results, json_file, indent=4)
        print(f"Tracking data saved to '{self.output_json}'")


if __name__ == "__main__":
    video_path = 'received_video.mp4'
    model_path = 'yolov8m.pt'

    # Step 1: Run Detection
    print("Running detection...")
    detector = Yolo(model_path="yolov8m.pt")
    detections = detector.detect(video_path)
    print(f"Detections completed. Total frames processed: {len(detections)}")

    # Step 2: Run Tracking
    print("Running tracking...")
    tracker = SortOT(output_json='tracking_data.json')
    tracker.track(detections)
    tracker.save_tracking_data()
    print("Tracking completed.")
