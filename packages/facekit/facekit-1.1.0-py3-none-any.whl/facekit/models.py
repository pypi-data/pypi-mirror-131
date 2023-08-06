import os
from pathlib import Path
import matplotlib.pyplot as plt
import glob
from PIL import Image
import numpy as np
from alive_progress import alive_bar
from colorama import Fore, Back, Style

# Suppress logging on mtcnn tf imports
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from mtcnn.mtcnn import MTCNN


class ImageFileLoader(object):
    @classmethod
    def get_image_path_list(cls, image_dir):
        return [Path(p) for p in glob.glob(f"{image_dir}/*.jpg")]

    @classmethod
    def get_image_pixels_from_file(cls, image_file):
        image_pixels = plt.imread(image_file)
        return image_pixels


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


class FaceDetector(object):
    input_path: str
    output_path: str
    accuracy_threshold: float
    detection_targets: list
    detection_results: list

    def __init__(self, input_path, output_path, accuracy_threshold, preload_images=True, resize=False,
                 resize_to=(224, 224)):
        self.input_path = input_path
        self.output_path = output_path
        self.accuracy_threshold = accuracy_threshold
        self.resize = resize
        self.resize_to = resize_to

        if not os.path.isdir(self.input_path):
            raise FileNotFoundError("Input path doesn't exist or is not a directory")
        if not os.path.isdir(self.output_path):
            raise FileNotFoundError("Output path doesn't exist or is not a directory")

        self.image_path_list = ImageFileLoader.get_image_path_list(input_path)
        self.detection_targets = []
        self.detection_results = []

        self._preloaded = preload_images
        if self._preloaded:
            self._preload_images()

    def _preload_images(self):
        with alive_bar(len(self.image_path_list), title=f"{Fore.CYAN}Preloading{Style.RESET_ALL}") as bar:
            for image_path in self.image_path_list:
                fd_target = FaceDetectionTarget(file_stem=image_path.stem,
                                                image_pixels=ImageFileLoader.get_image_pixels_from_file(image_path))

                self.detection_targets.append(fd_target)
                bar()


class MTCNNDetector(FaceDetector):
    def __init__(self, input_path, output_path, accuracy_threshold, preload):
        super().__init__(input_path, output_path, accuracy_threshold, preload)
        self.model = MTCNN()

    def _get_image_face_results(self, target: FaceDetectionTarget):
        results = self.model.detect_faces(target.image_pixels)
        return FaceDetectionResult(target=target, detections=results)

    def _filter_and_cut_results(self, fd_result: FaceDetectionResult):
        for result in fd_result.detections:
            if result['confidence'] >= self.accuracy_threshold:
                x1, y1, width, height = result['box']
                x2, y2 = x1 + width, y1 + height
                face = fd_result.target.image_pixels[y1:y2, x1:x2]
                image = Image.fromarray(face)
                image = image.resize((224, 224))  # Turn this to param
                face_array = np.asarray(image)
                fd_result.face_arrays.append(face_array)

        self.detection_results.append(fd_result)

    def extract_faces(self):
        title = f"{Fore.LIGHTYELLOW_EX}Extracting{Style.RESET_ALL}"
        if self._preloaded:
            with alive_bar(len(self.detection_targets), title=title) as bar:
                for fd_target in self.detection_targets:
                    fd_result = self._get_image_face_results(fd_target)
                    self._filter_and_cut_results(fd_result)
                    bar()
        else:
            with alive_bar(len(self.image_path_list), title=title) as bar:
                for image_path in self.image_path_list:
                    fd_target = FaceDetectionTarget(file_stem=image_path.stem,
                                                    image_pixels=ImageFileLoader.get_image_pixels_from_file(image_path))
                    fd_result = self._get_image_face_results(fd_target)
                    self._filter_and_cut_results(fd_result)
                    bar()

    def store_extracted_faces(self):
        with alive_bar(len(self.detection_results), title=f"{Fore.GREEN}Storing faces{Style.RESET_ALL}") as bar:
            for result in self.detection_results:
                ctr = 0
                for face in result.face_arrays:
                    im = Image.fromarray(face)
                    im.save(f"{self.output_path}/{result.target.file_stem}_{ctr}.jpg")
                    ctr += 1
                bar()