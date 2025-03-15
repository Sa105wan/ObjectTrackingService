import torch
from torchvision import models, transforms
from PIL import Image
import cv2
from torchvision.models.detection import (
    FasterRCNN_ResNet50_FPN_Weights,
    FasterRCNN_MobileNet_V3_Large_FPN_Weights,
    FasterRCNN_MobileNet_V3_Large_320_FPN_Weights,
    FasterRCNN_ResNet50_FPN_V2_Weights,
    RetinaNet_ResNet50_FPN_Weights,
    RetinaNet_ResNet50_FPN_V2_Weights,
    SSD300_VGG16_Weights,
    SSDLite320_MobileNet_V3_Large_Weights,
    FCOS_ResNet50_FPN_Weights,
    KeypointRCNN_ResNet50_FPN_Weights,
    MaskRCNN_ResNet50_FPN_Weights,
    MaskRCNN_ResNet50_FPN_V2_Weights
    
)


class TorchVisionDetection:
    def __init__(self, model_name, confidence_threshold=0.5):
        self.model = self.load_model(model_name)
        self.model.eval()
        self.confidence_threshold = confidence_threshold
        self.transform = transforms.Compose([
            transforms.ToTensor()
        ])

    def load_model(self, model_name):
        if model_name == "fasterrcnn":
            model = models.detection.fasterrcnn_resnet50_fpn(weights=FasterRCNN_ResNet50_FPN_Weights.DEFAULT)
        elif model_name == "fasterrcnnmobilenet":
            # model = models.detection.fasterrcnn_mobilenet_v3_large_fpn(weights=FasterRCNN_MobileNet_V3_Large_FPN_Weights.DEFAULT)
            model = models.detection.fasterrcnn_mobilenet_v3_large_320_fpn(weights=FasterRCNN_MobileNet_V3_Large_320_FPN_Weights.DEFAULT)
        elif model_name == "fasterrcnnv2":
            model = models.detection.fasterrcnn_resnet50_fpn_v2(weights=FasterRCNN_ResNet50_FPN_V2_Weights.DEFAULT)
        elif model_name == "retinanet":
            # model = models.detection.retinanet_resnet50_fpn(weights=RetinaNet_ResNet50_FPN_Weights.DEFAULT)
            model = models.detection.retinanet_resnet50_fpn_v2(weights=True)
        elif model_name == "ssd":
            model = models.detection.ssd300_vgg16(weights=SSD300_VGG16_Weights.DEFAULT)
        elif model_name == "ssdlite":
            model = models.detection.ssdlite320_mobilenet_v3_large(weights=SSDLite320_MobileNet_V3_Large_Weights.DEFAULT)
        elif model_name == "fcosresnet50":
            model = models.detection.fcos_resnet50_fpn(weights=FCOS_ResNet50_FPN_Weights.DEFAULT)
        else:
            raise ValueError(f"Model {model_name} not supported!")
        
        return model

    def detect(self, video_path):
        cap = cv2.VideoCapture(video_path)
        detections = []
        frame_idx = 0

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Convert frame to PIL image and apply transformation
            pil_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            input_tensor = self.transform(pil_image).unsqueeze(0)

            # Perform detection
            with torch.no_grad():
                outputs = self.model(input_tensor)[0]

            frame_detections = []
            for box, score, label in zip(outputs['boxes'], outputs['scores'], outputs['labels']):
                if score > self.confidence_threshold:
                    x1, y1, x2, y2 = box.numpy()
                    # frame_detections.append([x1, y1, x2, y2, score.item(), int(label)])
                    frame_detections.append([x1, y1, x2, y2, score.item()])

            detections.append({
                'frame': frame_idx + 1,
                'detections': frame_detections
            })
            frame_idx += 1

        cap.release()
        return detections

if __name__ == "__main__":
    video_path = "received_video.mp4"
    detector = TorchVisionDetection("retinanet",confidence_threshold=0.5)
    detections = detector.detect(video_path)
    print(len(detections))
    print(detections[:3])
    # for frame_data in result:
    #     print(f"Frame {frame_data['frame']}:")
    #     for det in frame_data['detections']:
    #         print(f"  Box: {det[:4]} | Confidence: {det[4]:.2f} | Label: {det[5]}")
