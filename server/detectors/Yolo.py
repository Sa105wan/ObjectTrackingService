from ultralytics import YOLO

class Yolo:
    def __init__(self, model_path, confidence_threshold=0.5):
        self.model = YOLO(model_path)
        self.confidence_threshold = confidence_threshold

    def detect(self, video_path):
        results = self.model.predict(video_path, conf=self.confidence_threshold)
        detections = []

        for frame_idx, result in enumerate(results):
            filtered_dets = result.boxes.data.cpu().numpy()

            # Collect only relevant detections
            frame_detections = [
                [d[0], d[1], d[2], d[3], d[4]]  # [x1, y1, x2, y2, confidence]
                for d in filtered_dets if d[4] > self.confidence_threshold
            ]

            detections.append({
                'frame': frame_idx + 1,
                'detections': frame_detections
            })

        return detections
