import json
import trackpy as tp
import pandas as pd
import sys
# sys.path.append("../../detectors")
# from Yolo import Yolo

class TrackPyOT:
    def __init__(self, output_json='tracking_data.json'):
        """Initialize the tracker and output file."""
        self.output_json = output_json
        self.track_data = []
        self.track_id = 0

    def run(self, detections):
        total_frames = len(detections)
        tracking_data = []

        for frame_idx in range(total_frames):
            # Get detections for the current frame
            bboxes = detections[frame_idx]['detections'] if frame_idx < len(detections) else []

            if len(bboxes) == 0:
                tracking_data.append({
                    "frame": frame_idx,
                    "track_id": self.track_id,
                    "x": [],
                    "y": [],
                })
                continue

            # Create a temporary DataFrame for Trackpy
            temp_df = pd.DataFrame(bboxes, columns=['x1', 'y1', 'x2', 'y2', 'confidence'])
            temp_df['frame'] = frame_idx

            # Calculate object center
            temp_df['x'] = (temp_df['x1'] + temp_df['x2']) / 2
            temp_df['y'] = (temp_df['y1'] + temp_df['y2']) / 2

            # Link objects across frames using Trackpy
            if frame_idx == 0:
                # First frame: initialize tracks
                linked_df = temp_df
            else:
                linked_df = tp.link(temp_df, search_range=10)  # Adjust search range as needed

            # Save tracking information
            for _, track in linked_df.iterrows():
                self.track_id += 1
                tracking_data.append({
                    "frame": frame_idx,
                    "track_id": self.track_id,
                    "x": track['x'],
                    "y": track['y'],
                })

        self.track_data = tracking_data
        self.save_tracking_data()

    def save_tracking_data(self):
        """Save the tracking data to a JSON file."""
        with open(self.output_json, 'w') as json_file:
            json.dump(self.track_data, json_file, indent=4)
        print(f"Tracking data saved to {self.output_json}")



# Main function to run the pipeline
if __name__ == "__main__":
    video_path = 'received_video.mp4'
    model_path = 'yolov8m.pt'

    # Step 1: Run Detection
    print("Running detection...")
    detector = Yolo(model_path)
    detections = detector.detect(video_path)
    print(f"Detections completed. Total frames processed: {len(detections)}")

    # Step 2: Run Tracking
    print("Running tracking...")
    tracker = TrackPyOT(output_json='tracking_data.json')
    tracker.run(detections, len(detections))
    tracker.save_tracking_data()
    print("Tracking completed.")
