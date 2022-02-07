import cv2
import torch
import numpy as np


def yolov3(image, boxes, colors):
    with open('yolov3/coco.name', 'r') as f:
        classes = [line.strip() for line in f.readlines()]
    font = cv2.FONT_HERSHEY_PLAIN
    for i in range(len(boxes)):
        x, y, x2, y2, cls, label = boxes[i]
        if x2 - x < 400 or y2 - y < 400:
            color = colors[int(label)]
            label = str(float("{:.3f}".format(cls))) + str(classes[int(label)])
            cv2.rectangle(image, (int(x), int(y)), (int(x2), int(y2)), color, 3)
            cv2.putText(image, label, (int(x), int(y) - 5), font, 1, color, 2)
    return image
