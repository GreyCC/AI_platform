from operator import mod
import cv2
import time
import imageio
import tkinter as tk
import numpy as np

from gui_lib import frame_resize, screenshot, call_from_folder
from pytorchyolo import detect, models
from detection import yolov3
from PIL import Image, ImageTk
from tkinter.constants import RIDGE, SUNKEN
from tkinter import font


def widget():  # Initial widget ex. labels, buttons

    list_label = tk.Label(gui, bg='Yellow', relief=RIDGE, text='Video List', font='Arial 17')
    list_label.place(x=15, y=40, width=110)

    video_or_label = tk.Label(gui, bg='#FF00FF', relief=RIDGE, text='Source Video', font='Verdana 22 bold')
    video_or_label.place(x=150 + box_w / 2 - 150, y=30, width=300, height=40)

    video_pr_label = tk.Label(gui, bg='#FFFF00', relief=RIDGE, text='Processed Video', font='Verdana 22 bold')
    video_pr_label.place(x=150 + 20 + box_w / 2 * 3 - 150, y=30, width=300, height=40)

    save_button = tk.Button(gui, text='Screenshot', relief=RIDGE, bg='white', font='Arial 14', command=save_frame)
    save_button.place(x=g_w - 200, y=box_h + 220, width=150, height=50)


def print_list():
    video_list = tk.Listbox(bg='white', relief=SUNKEN)  # Set a list
    video_list.place(x=15, y=80, width=110)  # Set position
    for i, name in enumerate(list):  # Enumerate: return [index, content]
        video_list.insert(i, name)  # List name w.r.t. index and name
    video_list.bind('<<ListboxSelect>>', onselect)  # When selected, run onselect


def onselect(evt):
    global start
    w = evt.widget  # get widget that call this function
    index = int(w.curselection()[0])  # get the index of the object clicked
    value = w.get(index)  # get the name accroding to the index
    vid = imageio.get_reader('Video/' + value)  # Read video from 'Your_Folder' + name of video
    vid_name = value
    if object:  # Stop processing while switching to other video
        start_obj()
    update_text.delete('1.0', tk.END)
    show_video(vid, vid_name)  # Show video


def show_video(vid, vid_name):
    global object
    global action
    global pause
    global save

    frame = 0
    fps = cv2.VideoCapture('Video/' + vid_name).get(cv2.CAP_PROP_FPS)
    frame_rest = 1 / fps
    screenshot_name = vid_name[:-4]
    colors = np.random.uniform(0, 255, size=(80, 3))
    for name in script_list:
        if screenshot_name in name:
            with open('script/' + name) as file:
                lines = file.readlines()
            first_line = lines[0].split()

    for image in vid.iter_data():  # Loop video in frames
        frame += 1
        image_pr = image.copy()  # Do nothing
        start_time = time.time()

        # ---------------------------------------------------------------------------------------------------------
        if object:  # When start button is clicked
            result = detect.detect_image(model, image_pr)
            image_pr = yolov3(image_pr, result, colors)

        # ---------------------------------------------------------------------------------------------------------
        if action:
            while int(first_line[0]) < frame:
                lines.pop(0)
                first_line = lines[0].split()
            if int(first_line[0]) == frame:
                update_text.insert(tk.END, 'Frame ' + str(frame) + ': ' + first_line[1] + '\n')
                lines.pop(0)
                first_line = lines[0].split()
            elif mod(frame, 120) == 0:
                update_text.insert(tk.END, 'No Action\n')

        if save:
            screenshot(screenshot_name, frame, image, image_pr, object)
            time.sleep(0.2)
            save = False

        AI_process_time = time.time() - start_time
        var_time.set(str(AI_process_time)[:8])

        image_re = frame_resize(image, box_w, box_h)
        image_pr_re = frame_resize(image_pr, box_w, box_h)

        # Output image frame to original video box
        image_frame = Image.fromarray(image_re)
        frame_image = ImageTk.PhotoImage(image_frame)
        video_box_or.config(image=frame_image)
        video_box_or.image = frame_image

        # Output image frame to processed video box
        image_frame_pr = Image.fromarray(image_pr_re)
        frame_image_pr = ImageTk.PhotoImage(image_frame_pr)
        video_box_pr.config(image=frame_image_pr)
        video_box_pr.image = frame_image_pr

        video_process_time = time.time() - start_time

        while pause:
            time.sleep(0.01)
            gui.update()
            if save:
                screenshot(screenshot_name, frame, image, image_pr, object)
                time.sleep(0.2)
                save = False
        if AI_process_time < frame_rest and frame_rest > (
                video_process_time):  # If process time smaller than frame interval time
            time.sleep(frame_rest - video_process_time)  # Adjust video speed

        update_text.see(tk.END)
        gui.update()  # Update GUI for new frame

    gui.after(100, show_video(vid, vid_name))  # Loop the video


def start_obj():
    global object
    global var_obj_det
    object = not object  # True -> False, vice versa
    if object:  # Change button text alternatively
        var_obj_det.set('Stop Object Detect')
    else:
        var_obj_det.set('Start Object Detect')


def start_act():
    global action
    global var_action
    action = not action
    if action:
        var_action.set('Stop Action Recognition')
    else:
        var_action.set('Start Action Recognition')


def pause_vid():
    global pause
    global var_pause
    pause = not pause
    if pause:  # Change button text alternatively
        var_pause.set('Resume Video')
    else:
        var_pause.set('Pause Video')


def save_frame():
    global save
    save = not save


if __name__ == "__main__":
    object = False
    pause = False
    save = False
    action = False

    gui = tk.Tk()  # GUI initial
    gui.attributes('-zoomed', True)     # Ubuntu
    # gui.state('zoomed')     # Window
    gui.resizable(0, 0)
    gui.update()

    g_h = gui.winfo_height()  # gui window height
    g_w = gui.winfo_width()  # gui window width

    box_w = (g_w - 200) / 2  # video box width
    box_h = box_w * 3 / 4  # video box height

    video_box_or = tk.Label(gui, bg='white', relief=SUNKEN)
    video_box_or.place(x=150, y=80, width=box_w, height=box_h)

    video_box_pr = tk.Label(gui, bg='white', relief=SUNKEN)
    video_box_pr.place(x=150 + 20 + box_w, y=80, width=box_w, height=box_h)

    widget()  # Set labels

    while True:
        time_label = tk.Label(gui, text='Processing time:', font='Arial 12 bold')
        time_label.place(x=10, y=80 + box_h - 50, width=135, height=25)

        var_time = tk.StringVar()
        test_time = tk.Label(gui, bg='#FDFDFD', relief=SUNKEN, textvariable=var_time, font='14')
        test_time.place(x=10, y=80 + box_h - 25, width=135, height=25)

        var_obj_det = tk.StringVar()
        var_obj_det.set('Start Object Detection')
        object_detect_button = tk.Button(gui, relief=RIDGE, bg='#DDDDDD', font='Arial 14', textvariable=var_obj_det,
                                         command=start_obj)
        object_detect_button.place(x=g_w - 570, y=box_h + 100, width=250, height=50)

        var_action = tk.StringVar()
        var_action.set('Start Action Recognition')
        object_detect_button = tk.Button(gui, relief=RIDGE, bg='#DDDDDD', font='Arial 14', textvariable=var_action,
                                         command=start_act)
        object_detect_button.place(x=g_w - 300, y=box_h + 100, width=250, height=50)

        var_pause = tk.StringVar()
        var_pause.set('Pause video')
        pause_button = tk.Button(gui, relief=RIDGE, bg='white', font='Arial 14', textvariable=var_pause,
                                 command=pause_vid)
        pause_button.place(x=g_w - 200, y=box_h + 160, width=150, height=50)

        log_label = tk.Label(gui, text='Action', font='Arial 12 bold')
        log_label.place(x=150, y=80 + box_h + 30)

        update_text = tk.Text(gui, bg='#FDFDFD', relief=SUNKEN, font='14')
        update_text.place(x=150, y=80 + box_h + 60, width=200, height=250)

        list = call_from_folder("Video")  # Find all files in the folder
        print_list()  # List out all files
        script_list = call_from_folder("script")
        model = models.load_model(
            "yolov3/yolov3.cfg",
            "yolov3/yolov3.weights")
        break

    gui.mainloop()  # Start GUI
