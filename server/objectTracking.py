import json
import io
from ultralytics import YOLO
import imageio
import numpy as np

class ObjectTracker:
    def __init__(self, model_path="yolov8m.pt"):
        # Load the YOLOv8 model during class initialization
        self.model = YOLO(model_path)

    def track_objects(self, video_stream):
        # Reset the stream pointer to the beginning
        video_stream.seek(0)

        # Use imageio to read the video from the in-memory stream
        try:
            reader = imageio.get_reader(video_stream, format='ffmpeg')
        except Exception as e:
            raise RuntimeError(f"Error reading video stream: {str(e)}")

        # Initialize a list to store each frame's data
        output_data = []
        frame_number = 0

        # Read frames from the video stream
        for frame in reader:
            # Convert the frame to a format suitable for YOLO (numpy array)
            frame_bgr = np.array(frame)[..., ::-1]  # Convert RGB to BGR for OpenCV

            # Run object tracking on the current frame
            results = self.model.track(source=frame_bgr, show=False, tracker="bytetrack.yaml")

            # Collect information from the current frame
            frame_data = {
                "frame": frame_number,
                "objects": []
            }

            if results[0].boxes is not None:  # If boxes are detected in the current frame
                for obj in results[0].boxes:
                    object_info = {
                        "class": results[0].names[int(obj.cls)],  # Convert class ID to class name
                        "confidence": obj.conf.item(),  # Convert tensor to float
                        "box": obj.xywh.tolist()  # Bounding box in format (center_x, center_y, width, height)
                    }
                    frame_data["objects"].append(object_info)

            # Add the frame's data to the output
            output_data.append(frame_data)

            # Increment the frame counter
            frame_number += 1

        # Convert the result data into JSON format
        json_output = json.dumps(output_data, indent=4)

        # Return the JSON output
        return json_output
