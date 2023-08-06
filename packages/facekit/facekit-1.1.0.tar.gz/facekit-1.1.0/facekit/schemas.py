import os
# Suppress logging on mtcnn tf imports
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


class FaceDetectionTarget(object):
    image_pixels: list
    file_stem: str

    def __init__(self, image_pixels, file_stem):
        self.image_pixels = image_pixels
        self.file_stem = file_stem


class FaceDetectionResult(object):
    target: FaceDetectionTarget
    detections: list

    def __init__(self, target: FaceDetectionTarget, detections: list):
        self.target = target
        self.detections = detections
        self.face_arrays = []

