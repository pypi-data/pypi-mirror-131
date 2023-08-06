# -*- coding: utf-8 -*-
#############################################
# File Name: setup.py
# Author: bbnclyx
# Mail: 20185414@stu.neu.edu.cn
# Created Time:  2021-12-11
#############################################
from setuptools import setup, find_packages


# with open("README.rst") as f:
#     readme = f.read()
#
# with open("LICENSE") as f:
#     license = f.read()

# with open("requirements.txt", "r") as f:
#     required = f.read().splitlines()

setup(
    name="deepcad",
    version="0.0.4",
    description=("implemenent deepcad to denoise data by "
                 "removing independent noise"),
    author="bbnclyx and bbnclyx",
    author_email="20185414@stu.neu.edu.cn",
    url="https://github.com/cabooster/DeepCAD-RT",
    license="MIT Licence",
    packages=find_packages(),
    install_requires=['matplotlib','pyyaml','tifffile','scikit-image','opencv-python','csbdeep','gdown'],
)
