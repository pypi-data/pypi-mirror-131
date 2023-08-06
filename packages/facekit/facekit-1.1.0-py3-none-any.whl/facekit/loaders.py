from pathlib import Path
import matplotlib.pyplot as plt
import glob


class ImageFileLoader(object):
    @classmethod
    def get_image_path_list(cls, image_dir):
        return [Path(p) for p in glob.glob(f"{image_dir}/*.jpg")]

    @classmethod
    def get_image_pixels_from_file(cls, image_file):
        image_pixels = plt.imread(image_file)
        return image_pixels
