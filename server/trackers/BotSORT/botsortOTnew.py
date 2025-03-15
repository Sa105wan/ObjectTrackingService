import sys
sys.path.append("/BoT-SORT")

from botsort import BoTSORT
import json


class BotSortOTnew:
    def __init__(self, det_thresh=0.3, iou_thresh=0.5, max_age=30, min_hits=3,output_data="output_data.json"):
        self.tracker = BoTSORT(
            det_thresh=det_thresh,
            iou_thresh=iou_thresh,
            max_age=max_age,
            min_hits=min_hits
        )
        self.output_data = output_data

    def track_frame(self, detections):
        """
        Perform tracking on a single frame.
        Expects `detections` in the format [[x1, y1, x2, y2, confidence]].
        Returns active tracks for the frame: [[x1, y1, x2, y2, track_id]].
        """
        # Add dummy class IDs (e.g., class_id = 1 for all detections)
        formatted_detections = [
            [det[0], det[1], det[2], det[3], det[4], 1] for det in detections
        ]
        tracks = self.tracker.update(formatted_detections)
        return tracks

    def run(self, detections_per_frame):
        """
        Perform tracking across video detections.
        Saves the tracking results to a JSON file.
        """
        tracking_results = []

        for frame_data in detections_per_frame:
            frame_id = frame_data['frame']
            detections = frame_data['detections']

            # Track objects in the current frame
            tracks = self.track_frame(detections)

            # Prepare tracking results for the current frame
            frame_tracks = []
            for track in tracks:
                track_id = int(track[4])  # Track ID
                x_min, y_min, x_max, y_max = map(float, track[:4])  # Bounding box
                frame_tracks.append({
                    'track_id': track_id,
                    'bbox': [x_min, y_min, x_max, y_max]
                })

            tracking_results.append({
                'frame': frame_id,
                'tracks': frame_tracks
            })

        # Save tracking results to a JSON file
        with open(self.output_data, 'w') as f:
            json.dump(tracking_results, f, indent=4)

        print(f"Tracking results saved to {self.output_data}")
