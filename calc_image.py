#!/usr/bin/env python
# coding: utf-8

import os
import cv2
import csv
import numpy as np
import matplotlib.image as mpimg
from matplotlib import pyplot as plt

image_path = os.path.join(os.getcwd(), "image_input")

output_path = os.path.join(os.getcwd(), "output")


def binarize_lib(
    image_file,
    thresh_val=127,
    with_plot=True,
):
    filename = os.path.basename(image_file).split(".")[0]
    result_path = os.path.join(output_path, filename + "_calc.png")
    img = cv2.imread(image_file)
    image_src = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    th, image_b = cv2.threshold(
        src=image_src, thresh=thresh_val, maxval=255, type=cv2.THRESH_BINARY
    )
    ratio = cv2.countNonZero(image_b) / (image_src.size)
    white_percent = ratio * 100
    result = [result_path, white_percent]
    if with_plot:
        original_img = mpimg.imread(image_file)
        cmap_val = "gray"
        fig, (ax1, ax2) = plt.subplots(
            nrows=1,
            ncols=2,
        )
        fig.suptitle("{} - {}%".format(filename, white_percent))

        ax1.axis("off")
        ax1.title.set_text("Original")
        ax1.imshow(original_img, interpolation="none")

        ax2.axis("off")
        ax2.title.set_text("Binarized")
        ax2.imshow(image_b, cmap=cmap_val)
        plt.savefig(result_path)
        # plt.show()
    return result


if not os.path.exists(output_path):
    os.makedirs(output_path)


def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        path = os.path.join(folder, filename)
        img = cv2.imread(path)
        if img is not None:
            images.append(path)
    return images


if __name__ == "__main__":
    images = load_images_from_folder(image_path)
    print("Images founded: {}".format(len(images)))
    print("")

    result = []
    error = []
    for path in images:
        complate = (len(result) / len(images)) * 100
        try:
            res_path, percent = binarize_lib(path)
            result.append([res_path, percent])
            print("Ok - {:.2f}% - {}".format(complate, res_path))
        except:
            result.append([path, "ERROR"])
            print("Error - {:.2f}% - {}".format(complate, path))
            error.append(path)

    table_output = os.path.join(output_path, 'result.csv')
    with open(table_output, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)

        writer.writerow(['file', 'white_percent'])
        writer.writerows(result)

    print('Summary - {}'.format(table_output))