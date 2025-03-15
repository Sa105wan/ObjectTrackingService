import json
from ultralytics import YOLO
import os
import sys
import numpy as np
import subprocess
import torch
from detectors.Yolo import Yolo
from detectors.TorchVisionDetection import TorchVisionDetection
from detectors.TensorFlowDetection import TensorFlowDetection
from trackers.SORT.sortOT import SortOT
from trackers.DeepSORT.deepsortOT import DeepSortOT
from trackers.BotSORT.botsortOT import BotSortOT
from trackers.ByteTrack.bytetrackOT import ByteTrackOT
from trackers.TrackPy.trackpyOT import TrackPyOT
from trackers.StrongSORT.StrongSORTOT import StrongSORTOT
from trackers.NorFair.NorfairOT import NorfairOT


trackers_path = os.path.join(os.path.dirname(__file__), 'trackers')
sys.path.append(trackers_path)

class ObjectProcessor:
    def __init__(self):
        self.model = None  
        self.detector = None
        self.tracker = None

    def load_model(self, model):
        self.model = model
        name = model.split("_")
        self.detector = name[0]
        self.tracker = name[1]

    def detect_objects(self, video_path):

        if self.detector[:4]=="yolo":
            Model = Yolo(self.detector)
            detections = Model.detect(video_path)
            return detections
        
        if self.detector[:2] == "tf":
            print("model Name")
            print(self.detector[2:])
            detector = TensorFlowDetection(self.detector[2:], confidence_threshold=0.5)
            detections = detector.detect(video_path)
            return detections        


        if self.detector[:2] == "tv":
            print("model Name")
            print(self.detector[2:])
            detector = TorchVisionDetection(self.detector[2:], confidence_threshold=0.5)
            detections = detector.detect(video_path)
            return detections

    def track_objects(self, detections, video_path):
       device = self.get_device()

       if self.tracker=="sort":
            tracker = SortOT(output_json='output_data.json')
            tracker.track(detections)

       if self.tracker=="strongsort":
            tracker = StrongSORTOT(model_weights_path="osnet_x0_25_msmt17.pt", device=device, output_json='output_data.json')
            tracker.run(video_path,detections)

       if self.tracker=="norfair":
            tracker = NorfairOT(output_json='output_data.json')
            tracker.run(video_path,detections)

       if self.tracker =="deepsort":
            tracker = DeepSortOT(output_json='output_data.json')
            # print(detections)
            tracker.run(detections, video_path)

       if self.tracker == "trackpy":
           tracker = TrackPyOT(output_json='output_data.json')
           tracker.run(detections)

       if self.tracker == "ocsort":
            python38_path = os.path.join('trackers', 'OCSort', 'venv38', 'Scripts', 'python.exe')
            script_path = os.path.join('trackers', 'OCSort', 'OCSortOT.py')
            detections = np.array(detections, dtype=np.float32)
            detections_bytes = detections.tobytes()
            result = subprocess.run(
                [python38_path, script_path],
                input=detections_bytes, 
                capture_output=True
            )

            if result.returncode == 0:
                print("Script executed successfully!")
                print(result.stdout)  # Output from the script
            else:
                print(f"Error executing script: {result.stderr}")

    def trackInbuild(self, model_name):
        tracker_name = model_name.split("_")[1]
        detector_name = model_name.split("_")[0]
        print("detector")
        print(detector_name)
        print("tracker name")
        print(tracker_name)
        if tracker_name == "bytetrack":
           tracker = ByteTrackOT( detector_name, output_json='output_data.json')
           tracker.run('received_video.mp4')

        if tracker_name == "botsort":
           tracker = BotSortOT(detector_name, output_json='output_data.json')
           tracker.run('received_video.mp4')


    def get_device(self):
    # Check for any GPU backend
        if torch.cuda.is_available():  # NVIDIA GPUs
            return "cuda"
        elif torch.backends.mps.is_available():  # Apple Silicon GPUs
            return "mps"
        elif hasattr(torch.version, "hip") and torch.version.hip:  # AMD GPUs with ROCm
            return "rocm"
        else:
            return "cpu" 