import cv2
import json
import trackpy as tp
import numpy as np
import pandas as pd
from ultralytics import YOLO
import matplotlib.pyplot as plt

class TrackPyOTold:
    def __init__(self, model_path, output_json='tracking_data_trackpy.json'):

        self.model = YOLO(model_path)
        self.video_path = ''
        self.output_json = output_json
        self.frames = []
        self.track_data = []
        self.track_id = 0
        self.object_tracks = []

        # Load video frames
       

    def load_video(self):
        """Load frames from the video."""
        video = cv2.VideoCapture(self.video_path)
        while True:
            ret, frame = video.read()
            if not ret:
                break
            self.frames.append(frame)
        video.release()

    def detect_objects(self, frame):
        """Detect objects in the given frame using YOLOv8."""
        results = self.model(frame)
        bboxes = []
        
        # Extract bounding boxes from the results
        for result in results[0].boxes:
            x1, y1, x2, y2 = result.xyxy[0].tolist()
            bboxes.append([x1, y1, x2, y2])
        return bboxes

    def track_objects(self):
        """Track objects across frames using Trackpy."""
        for frame_idx, frame in enumerate(self.frames):
            # Detect objects in the frame using YOLOv8
            bboxes = self.detect_objects(frame)

            # Create a temporary DataFrame for Trackpy
            temp_df = pd.DataFrame(bboxes, columns=['x1', 'y1', 'x2', 'y2'])
            temp_df['frame'] = frame_idx

            # Calculate object center
            temp_df['x'] = (temp_df['x1'] + temp_df['x2']) / 2
            temp_df['y'] = (temp_df['y1'] + temp_df['y2']) / 2

            # Link objects across frames (Trackpy will link based on proximity)
            if frame_idx == 0:
                # First frame: start new tracks
                self.object_tracks = temp_df
            else:
                self.object_tracks = tp.link(temp_df, search_range=10)  # Link based on proximity (adjust the range if needed)

            # Save the tracking information
            for _, track in self.object_tracks.iterrows():
                self.track_id += 1
                track_info = {
                    "frame": frame_idx,
                    "track_id": self.track_id,
                    "x": track['x'],
                    "y": track['y'],
                }
                self.track_data.append(track_info)

    def save_tracking_data(self):
        """Save the tracking data to a JSON file."""
        with open(self.output_json, 'w') as json_file:
            json.dump(self.track_data, json_file, indent=4)
        print(f"Tracking data saved to {self.output_json}")

    def run(self, video_path):
        """Run the object tracking pipeline."""
        self.video_path=video_path
        self.load_video()
        self.track_objects()
        self.save_tracking_data()

    def plot_trajectories(self):
        """Plot the object trajectories using Trackpy."""
        track_df = pd.DataFrame(self.track_data)
        track_df['particle'] = track_df['track_id']  # Use track_id as the particle identifier
        tp.plot_traj(track_df)
        plt.show()


# Main function to run the tracker independently
if __name__ == "__main__":
    tracker = TrackPyOT(
        model_path='yolov8m.pt',
        output_json='tracking_data.json'
    )
    tracker.run('received_video.mp4')
    tracker.plot_trajectories()  # Optional: Plot the trajectories after tracking
