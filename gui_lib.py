import cv2
import os

def call_from_folder(path):
    video_path = path                       # Folder name contain your testing video
    video_list = os.listdir(video_path)     # list out all files inside folder
    return video_list                       # Return list

def screenshot(name, frame, img, img_pr, start):
    turned_img = cv2.cvtColor(img, cv2.COLOR_RGB2BGRA)
    cv2.imwrite('Screenshot/' + name + '_' + str(frame) + '.jpg', turned_img)
    if start:
        turned_img = cv2.cvtColor(img_pr, cv2.COLOR_RGB2BGRA)
        cv2.imwrite('Screenshot/' + name + '_' + str(frame) + '_result' + '.jpg', turned_img)

def frame_resize(image, w, h):
    if image.shape[0] > image.shape[1]:
        if image.shape[0] > h:
            image = cv2.resize(image, (0, 0), fx=(h / image.shape[0]), fy=(h / image.shape[0]), interpolation=cv2.INTER_AREA)
        elif image.shape[1] > w:
            image = cv2.resize(image, (0, 0), fx=(w / image.shape[1]), fy=(w / image.shape[1]), interpolation=cv2.INTER_AREA)
    else:
        if image.shape[1] > w:
            image = cv2.resize(image, (0, 0), fx=(w / image.shape[1]), fy=(w / image.shape[1]), interpolation=cv2.INTER_AREA)
        elif image.shape[0] > h:
            image = cv2.resize(image, (0, 0), fx=(h / image.shape[0]), fy=(h / image.shape[0]), interpolation=cv2.INTER_AREA)
    return image