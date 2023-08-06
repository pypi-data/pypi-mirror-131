import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name="facekit",
    version="1.1.0",
    description="Library to ease data collection for face detection/recognition/analysis",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/jarviscodes/facekit",
    author="Jarvis Codes",
    author_email="jarvis@jayradz.com",
    license="MIT",
    classifiers=["Programming Language :: Python :: 3.8"],
    packages=["facekit"],
    include_package_data=True,
    install_requires=["click", "colorama", "alive-progress", "mtcnn"],
    entry_points={"console_scripts": ["facekit=facekit.__main__:main"]},
)
