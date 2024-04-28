import cv2
import numpy as np
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.graphics.texture import Texture
import pandas as pd
from ultralytics import YOLO
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from tracker import *

# Initialize YOLO model
model = YOLO('yolov8s.pt')

# State variables
PERSON_DETECTION = "person_detection"
current_state = PERSON_DETECTION
pause_detection = False

# Speaker color range in HSV
SPEAKER_COLOR_RANGE = {
    "lower": (0, 100, 100),  # replace with your speaker's color range in HSV
    "upper": (10, 255, 255)  # replace with your speaker's color range in HSV
}

# Get audio device
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

def find_speaker(frame):
    # Convert to HSV color space
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # Create a mask for speaker color
    mask = cv2.inRange(hsv_frame, np.array(SPEAKER_COLOR_RANGE["lower"]), np.array(SPEAKER_COLOR_RANGE["upper"]))
    # Find contours
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        # Get the largest contour
        largest_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour)
        return x + w // 2, y + h // 2  # Return center of the speaker
    return None

def calculate_average_distance(humans, speaker_position):
    if not humans or speaker_position is None:
        return None
    distances = []
    for human in humans:
        human_center = ((human[0] + human[2]) // 2, (human[1] + human[3]) // 2)
        distance = np.linalg.norm(np.array(human_center) - np.array(speaker_position))
        distances.append(distance)
    return np.mean(distances)

def adjust_volume_based_on_distance(distance):
    # Define your volume adjustment logic based on distance here
    if distance is not None:
        if distance < 100:  # Example threshold
            volume.SetMasterVolumeLevel(-10.0, None)
        else:
            volume.SetMasterVolumeLevel(0.0, None)

class VolumeControlApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
       
        self.volume_label = Label(text='Volume: ')
        self.volume_slider = Slider(min=-63, max=0, value=volume.GetMasterVolumeLevel(), step=1)
        self.volume_slider.bind(value=self.set_volume)

        self.inc_volume_button = Button(text='Increase Volume')
        self.inc_volume_button.bind(on_press=self.increase_volume)

        self.dec_volume_button = Button(text='Decrease Volume')
        self.dec_volume_button.bind(on_press=self.decrease_volume)

        self.toggle_detection_button = ToggleButton(text='Pause Detection')
        self.toggle_detection_button.bind(on_press=self.toggle_detection)

        self.resume_detection_button = Button(text='Resume Detection')
        self.resume_detection_button.bind(on_press=self.resume_detection)

        self.video_label = Image()

        layout.add_widget(self.volume_label)
        layout.add_widget(self.volume_slider)
        layout.add_widget(self.inc_volume_button)
        layout.add_widget(self.dec_volume_button)
        layout.add_widget(self.toggle_detection_button)
        layout.add_widget(self.resume_detection_button)
        layout.add_widget(self.video_label)

        Clock.schedule_interval(self.update_ui, 1.0 / 60.0)  # Update UI every frame
        Clock.schedule_interval(self.update_video_display, 1.0 / 60.0)  # Update video display every frame


        return layout
    def resume_detection(self, instance):
        global pause_detection
        pause_detection = False

    def set_volume(self, instance, value):
        volume.SetMasterVolumeLevel(value, None)
        self.volume_label.text = f'Volume: {value} dB'

    def increase_volume(self, instance):
        current_volume = volume.GetMasterVolumeLevel()
        self.set_volume(None, current_volume + 1)

    def decrease_volume(self, instance):
        current_volume = volume.GetMasterVolumeLevel()
        self.set_volume(None, current_volume - 1)

    def toggle_detection(self, instance):
        global pause_detection
        pause_detection = not pause_detection

    def update_ui(self, dt):
        self.volume_slider.value = volume.GetMasterVolumeLevel()

    def update_video_display(self, dt):
        if not pause_detection:
            ret, frame = cap.read()
            if ret and current_state == PERSON_DETECTION:
                results = model.predict(frame)
                a = results[0].boxes.data
                px = pd.DataFrame(a).astype("float")
                human_list = []

                for index, row in px.iterrows():
                    x1, y1, x2, y2, _, d = int(row[0]), int(row[1]), int(row[2]), int(row[3]), int(row[4]), int(row[5])
                    c = class_list[d]
                    if 'person' in c:
                        human_list.append([x1, y1, x2, y2])

                speaker_position = find_speaker(frame)
                average_distance = calculate_average_distance(human_list, speaker_position)
                adjust_volume_based_on_distance(average_distance)

                # [Rest of your video display update code]

            cv2.imshow("RGB", frame)

    # [Rest of your class code]

if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    my_file = open("coco.txt", "r")
    data = my_file.read()
    class_list = data.split("\n")
    tracker = Tracker()

    VolumeControlApp().run()
