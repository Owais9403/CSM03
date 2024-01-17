# -*- coding: utf-8 -*-
"""project.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1cUQvOLgl1YLVQuPTqUiL3ACMn2XeyBOa
"""

!pip install torch
!pip install torch --extra-index-url https://download.pytorch.org/whl/cu116

pip install ultralytics

pip install --upgrade pip

!pip install split-folders

pip install clearml

!pip install colorama

! python -m venv env

# prompt: apt install python3.10-venv

!apt install python3.10-venv

!python -m venv env

!pip install colorama

import os
import shutil
import splitfolders
import pandas as pd
import numpy as np
from tqdm import tqdm
from colorama import Fore

IMAGE_PATH = "/content/drive/MyDrive/Colab Notebooks/drone-dataset/ds0/img" # The path to the folder with images.
TARGET_PATH ="/content/drive/MyDrive/Colab Notebooks/drone-dataset/ds0/ann"

def create_dataset(data_path,target_path) :
    assert isinstance(data_path, str)
    assert isinstance(target_path, str)

    dict_paths = {
        "image": [],
        "annotation": []
    }

    for dir_name, _, filenames in os.walk(data_path):
        for filename in tqdm(filenames):
            name = filename.split('.')[0]
            dict_paths["image"].append(f"{data_path}/{name}.jpg")
            dict_paths["annotation"].append(f"{target_path}/{name}.txt")


    dataframe = pd.DataFrame(
        data=dict_paths,
        index=np.arange(0, len(dict_paths["image"]))
    )

    return dataframe

def prepare_dirs(dataset_path: str,
                 annotation_path: str,
                 images_path: str) -> None:
    if not os.path.exists(dataset_path):
        os.mkdir(path=dataset_path)
        os.mkdir(path=annotation_path)
        os.mkdir(path=images_path)

def copy_dirs(dataframe, data_path: str,target_path: str) :

    assert isinstance(dataframe, pd.DataFrame)
    assert isinstance(data_path, str)
    assert isinstance(target_path, str)

    for i in tqdm(range(len(dataframe))):
        image_path, annotation_path = dataframe.iloc[i]
        shutil.copy(image_path, data_path)
        shutil.copy(annotation_path, target_path)

def finalizing_preparation(dataset_path: str, ladd_path: str):
    assert os.path.exists(f"{dataset_path}")

    example_structure = [
        "dataset",
        "train", "labels", "images",
        "test","labels", "images",
        "val", "labels", "images"
    ]

    dir_bone = (
        dirname.split("/")[-1]
        for dirname, _, filenames in os.walk('/content/drive/MyDrive/Colab Notebooks/drone-dataset/working/dataset')
        if dirname.split("/")[-1] in example_structure
    )

    try:
        print("\n~ Lacmus Dataset Structure ~\n")
        print(
        f"""
      ├── {next(dir_bone)}
      │   │
      │   ├── {next(dir_bone)}
      │   │   └── {next(dir_bone)}
      │   │   └── {next(dir_bone)}
      │   │
      │   ├── {next(dir_bone)}
      │   │   └── {next(dir_bone)}
      │   │   └── {next(dir_bone)}
      │   │
      │   ├── {next(dir_bone)}
      │   │   └── {next(dir_bone)}
      │   │   └── {next(dir_bone)}
        """
        )
    except StopIteration as e:
        print(e)
    else:
        print( "-> Success")
    finally:
        os.system(f"rm -rf {ladd_path}")

import os

df = create_dataset(
    data_path=IMAGE_PATH,
    target_path=TARGET_PATH
)

dataset_path = "/content/drive/MyDrive/Colab Notebooks/drone-dataset/working/dataset"
ladd_path = "/content/drive/MyDrive/Colab Notebooks/drone-dataset/working/ladd"
annotation_path = "/content/drive/MyDrive/Colab Notebooks/drone-dataset/working/ladd/labels"
image_path = "/content/drive/MyDrive/Colab Notebooks/drone-dataset/working/ladd/images"

prepare_dirs(
    dataset_path=ladd_path,
    annotation_path=annotation_path,
    images_path=image_path
)

copy_dirs(
    dataframe=df,
    data_path=image_path,
    target_path=annotation_path
)

splitfolders.ratio(
    input=ladd_path,
    output=dataset_path,
    seed=42,
    ratio=(0.80, 0.10, 0.10),
    group_prefix=None,
    move=True
)

import colorama

finalizing_preparation(
    dataset_path,
    ladd_path
)

pip install clearml

!pip install clearml

! clearml-init

import yaml
from ultralytics import YOLO
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

config = {
    "path": "/content/drive/MyDrive/Colab Notebooks/drone-dataset/working/dataset",
    "train": "/content/drive/MyDrive/Colab Notebooks/drone-dataset/working/dataset/train/images",
    "val": "/content/drive/MyDrive/Colab Notebooks/drone-dataset/working/dataset/val/images",
    "predict": "/content/drive/MyDrive/Colab Notebooks/drone-dataset/working/test/train/image",
    "nc": 1,
    "names": ["human"]
}

with open("config.yaml", "w") as f:
    yaml.dump(config, f)

with open("config.yaml", "r") as f:
    print(f.read())

# prompt: exactly which code to be altered to change it to cpu instrad of cuda also alter the code

def main():
    model = YOLO("yolov8n.pt")
    model.train(
        # Project
        project="Polar-Owl",
        name="yolov8n",

        # Random Seed parameters
        deterministic=True,
        seed=42,

        # Data & model parameters
        data="/content/config.yaml",
        save=True,
        save_period=5,
        pretrained=True,
        imgsz=1280,

        # Training parameters
        epochs=20,
        batch=4,
        workers=8,
        val=True,
        device="cpu",

        # Optimization parameters
        lr0=0.0195,
        patience=3,
        optimizer="SGD",
        momentum=0.957,
        weight_decay=0.0005,
        close_mosaic=5,
    )

if __name__ == '__main__':
    main()

