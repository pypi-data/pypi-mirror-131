# Installing Dependincies
import matplotlib.image as img
import matplotlib.pyplot as plt
import cv2
import pandas as pd
import numpy as np

# Global Variable for Image Size
IMG_SIZE = 28

def test():
    print("Jar Jar")

def image_reducer(data, size=IMG_SIZE):
    """
    Function: image_reducer(path, size=IMG_SIZE)
    Inputs:
    - path
      path is a file path from anywhere,

    - size
      dimension of square image to be reduced into


    Outputs:
    reduced image of data type np.array
    """

    # Reducing from 3d to 2d shape
    data = data[:,:, 0]

    # standardizing data
    data = data / 255

    # Resizeing Image
    reduced_img = cv2.resize(data, (size, size))

    return reduced_img
