from setuptools import setup, find_packages
import codecs
import os

readme = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(readme, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '1.2.3.20'
DESCRIPTION = 'Simple interface that allows injection of image faults into robot cameras.'
LONG_DESCRIPTION = 'This tool is a simple interface that allows injection of image faults into robot cameras. Thanks to this interface, \
    you can create new image libraries by injecting the fault types you have determined, both real-time\
    to TOF and RGB type ROS cameras, and to the image libraries previously\
    recorded by these cameras. NOTE: For using Reatime FI features, please install ROS Noetic, cv-bridge and vision-opencv'

# Setting up
setup(
    name="camfitool",
    version=VERSION,
    licence="Apache Software License",
    author="Alim Kerem Erdogmus (Inovasyon Muhendislik)",
    author_email="<kerem.erdogmus@inovasyonmuhendislik.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['opencv-python', "PyQt5", "Pillow"],
    keywords=['python3', 'ros noetic', 'fault injection', 'image database', 'image faults', 'robot cameras'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: Microsoft :: Windows",
    ],
    project_urls={
        'Inovasyon Muhendislik': 'https://www.inorobotics.com/',
        'Github Wiki': 'https://github.com/inomuh/camfitool/wiki',
        'ROS Wiki': 'http://wiki.ros.org/camfitool/',
        'Download': 'https://github.com/inomuh/camfitool/releases',
        'Github Repository': 'https://github.com/inomuh/camfitool',    
    }
)

