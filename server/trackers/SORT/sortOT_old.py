import cv2
import numpy as np
import json
# from trackers.SORT.sort.sort import Sort
from sort.sort import Sort

from ultralytics import YOLO

class SortOT_old:
    def __init__(self, model_path, output_json='tracking_data.json'):
        self.tracker = Sort()
        self.model = YOLO(model_path)
        self.output_json = output_json
        self.tracking_results = []

    def process_video(self, video_path):
        cap = cv2.VideoCapture(video_path)
        frame_count = 0

        if not cap.isOpened():
            print(f"Error: Cannot open video file {video_path}")
            return

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame_count += 1

            # Run YOLOv8m detection
            results = self.model.predict(frame)
            detections = results[0].boxes.data.cpu().numpy()  # [x1, y1, x2, y2, confidence, class]

            # Format detections for SORT
            dets = np.array([[d[0], d[1], d[2], d[3], d[4]] for d in detections if d[4] > 0.5])

            # Update SORT tracker
            tracks = self.tracker.update(dets)

            # Store tracking data and draw bounding boxes
            frame = self.draw_tracks(frame, tracks, frame_count)

            # Display the frame with bounding boxes
            # self.display_frame(frame)

        cap.release()
        # cv2.destroyAllWindows()

    def draw_tracks(self, frame, tracks, frame_count):
        for track in tracks:
            x1, y1, x2, y2, track_id = map(int, track)
            self.tracking_results.append({
                'frame': frame_count,
                'track_id': track_id,
                'bbox': [x1, y1, x2, y2]
            })

            # Draw bounding boxes and track IDs
            # cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            # cv2.putText(frame, f'ID: {track_id}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        return frame

    def display_frame(self, frame):
        cv2.imshow('Object Tracking with YOLOv8m + SORT', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            return

    def save_tracking_data(self):
        with open(self.output_json, 'w') as json_file:
            json.dump(self.tracking_results, json_file, indent=4)
        print(f"Tracking data saved to '{self.output_json}'")

    def run(self, video_path):
        self.process_video(video_path)
        self.save_tracking_data()


if __name__ == "__main__":
    tracker = SortOT(model_path='yolov8m.pt', output_json='tracking_data.json')
    video_path = 'received_video.mp4'  # You can change this to any video path dynamically
    tracker.run(video_path)
