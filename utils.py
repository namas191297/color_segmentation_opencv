import cv2
import numpy as np
import os
import matplotlib.pyplot as plt
import io
from PIL import Image
import numpy as np

def process_bgr_image(img, lb, ub, channel):

    # Define the lower and upperbounds based on the image channel.
    if channel == 'Blue':
        lb = np.array([lb, 0, 0], np.uint8)
        ub = np.array([ub, 255, 255], np.uint8)
    elif channel == 'Green':
        lb = np.array([0, lb, 0], np.uint8)
        ub = np.array([255, ub, 255], np.uint8)
    elif channel == 'Red':
        lb = np.array([0, 0, lb], np.uint8)
        ub = np.array([255, 255, ub], np.uint8)

    # Calculate the histograms for the BGR color space and the Hue channel in the HSV image.
    hist_b, hist_g, hist_r = calculateHistogram(img, mode='BGR')

    # Plot the histograms
    hist_bgr = plotHistogram((hist_b, hist_g, hist_r), mode='BGR')

    # Calculate the mask for the given bounds from hsv image
    op = calculateMask(img, lb, ub, mode='BGR')

    return  hist_bgr, op

def process_hsv_image(img, lb, ub):
    
    # Conver the image to the HSV color space
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Define the lower and upperbounds for Hue
    lb = np.array([lb, 0, 0], np.uint8)
    ub = np.array([ub, 255, 255], np.uint8)

    # Calculate the histograms for the BGR color space and the Hue channel in the HSV image.
    hist_hue = calculateHistogram(img_hsv, mode='HSV')

    # Plot the histogram.
    hist_hsv = plotHistogram(hist_hue, mode='HSV')

    # Calculate the mask for the given bounds from hsv image
    op = calculateMask((img_hsv, img), lb, ub, mode='HSV')

    return hist_hsv, op


def calculateHistogram(img, mode):

    if mode == 'BGR':
        hist_b = cv2.calcHist([img], [0], None, [256], [0,255])
        hist_g = cv2.calcHist([img], [1], None, [256], [0,255])
        hist_r = cv2.calcHist([img], [2], None, [256], [0,255])

        return hist_b, hist_g, hist_r
    
    elif mode == 'HSV':

        hist_hue = cv2.calcHist([img], [0], None, [180], [0,180])
        return hist_hue

def plotHistogram(hists, mode):

    if mode == 'BGR':
        hist_b, hist_g, hist_r = hists
        plt.figure(figsize=(10,2))
        plt.plot(hist_b, color='b', label='Blue')
        plt.plot(hist_g, color='g', label='Green')
        plt.plot(hist_r, color='r', label='Red')
        plt.xlim([0, 255])
        plt.legend()
        buf_bgr= io.BytesIO()
        plt.savefig(buf_bgr, format='png')
        buf_bgr.seek(0)
        hist_bgr = Image.open(buf_bgr)
        plt.close()
        return hist_bgr
    
    if mode == 'HSV':

        hist_hue = hists
        plt.figure(figsize=(10,2))
        plt.plot(hist_hue, color='black', label='Black')
        plt.xlim([0, 180])
        buf_hsv = io.BytesIO()
        plt.savefig(buf_hsv, format='png')
        buf_hsv.seek(0)
        hist_hsv = Image.open(buf_hsv)
        plt.close()
        return hist_hsv

def calculateMask(imgs, lb, ub, mode):

    op = None

    if mode == 'BGR':
        img = imgs
        mask_1d = cv2.inRange(img, lb, ub)
        mask_3d = cv2.merge([mask_1d, mask_1d, mask_1d])
        op = cv2.bitwise_and(img, mask_3d)
    
    if mode == 'HSV':
        img_hsv, img = imgs
        mask_1d = cv2.inRange(img_hsv, lb, ub)
        mask_3d = cv2.merge([mask_1d, mask_1d, mask_1d])
        op = cv2.bitwise_and(img, mask_3d)

    return op