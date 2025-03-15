import cv2
import json
from trackers.DeepSORT.deep_sort.deep_sort import DeepSort
from ultralytics import YOLO


class DeepSortOT:
    def __init__(self, model_path, output_json='tracking_results.json'):
        self.model = YOLO(model_path)
        self.tracker = DeepSort(model_path="trackers/DeepSort/deep_sort/deep/checkpoint/ckpt.t7", max_age=70)
        self.video_path = None
        self.output_json = output_json
        self.tracking_data = []

    def set_video_path(self, video_path):
        """Set the video path dynamically."""
        self.video_path = video_path

    def process_video(self):
        if not self.video_path:
            raise ValueError("Video path is not set. Please use 'set_video_path()' to set it before running.")

        cap = cv2.VideoCapture(self.video_path)

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Preprocess frame and run detection
            og_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.model(og_frame, device='cpu', conf=0.5)

            for result in results:
                boxes = result.boxes
                cls = boxes.cls.tolist()
                conf = boxes.conf.detach().cpu().numpy()
                xywh = boxes.xywh.cpu().numpy()

                # Update tracker with bounding boxes
                tracks = self.tracker.update(xywh, conf, og_frame)

                for track in self.tracker.tracker.tracks:
                    track_id = track.track_id
                    x1, y1, x2, y2 = track.to_tlbr()
                    class_name = cls[int(track.track_id) % len(cls)] if cls else "unknown"

                    # Append tracking data (no display code here)
                    self.tracking_data.append({
                        "track_id": track_id,
                        "bbox": [x1, y1, x2, y2],
                        "class": class_name,
                    })

            # self.display_frame(frame)
            # self.draw_bbox(frame, track_id, x1, y1, x2, y2, class_name)

            # Press 'q' to exit the video display (commented out since we are not displaying)
            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     break

        cap.release()
        cv2.destroyAllWindows()

    def draw_bbox(self, frame, track_id, x1, y1, x2, y2, class_name):
        """Draw bounding boxes and track information on the frame."""
        cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (255, 0, 0), 2)  # Blue box
        cv2.putText(frame, f'ID: {track_id} {class_name}', (int(x1), int(y1) - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)  # Blue text

    def display_frame(self, frame):
        """Display the frame with tracking."""
        cv2.imshow('Tracking', frame)

    def save_tracking_data(self):
        """Save the tracking data to a JSON file."""
        with open(self.output_json, 'w') as json_file:
            json.dump(self.tracking_data, json_file, indent=4)
        print(f"Tracking data saved to {self.output_json}")

    def run(self, video_path=None):
        """Run the video tracker."""
        if video_path:
            self.set_video_path(video_path)
        self.process_video()
        self.save_tracking_data()

if __name__ == "__main__":
    # Initialize tracker with paths
    tracker = DeepSortOT(
        model_path="yolov8m.pt",
        tracker_weights="deep_sort/deep/checkpoint/ckpt.t7",
        video_path="input_video.mp4",
        output_json="tracking_results.json"
    )
    tracker.run()