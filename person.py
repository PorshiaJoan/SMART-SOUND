import cv2
import pandas as pd
from ultralytics import YOLO
from tracker import *
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import pyttsx3
import speech_recognition as sr
import sys
#Code 1: Volume Control
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

countperson = 4
if countperson >= 0:
        currentVolumeDb = volume.GetMasterVolumeLevel()
        print('Volume:', currentVolumeDb)

        if currentVolumeDb < -63:
            print('Minimum volume')
        elif currentVolumeDb > 0:
            print('Maximum volume')
        else:
            if countperson == 1 :
                # Set volume to 20%
                volume.SetMasterVolumeLevel(-27.0, None)
                volume.SetMute(0, None)
                print('Volume set to 20%')
            elif countperson == 2:
                # Set volume to 30%
                volume.SetMasterVolumeLevel(-18.0, None)
                volume.SetMute(0, None)
                print('Volume set to 30%')
            elif countperson == 3:
                # Set volume to 30%
                volume.SetMasterVolumeLevel(-18.0, None)
                volume.SetMute(0, None)
                print('Volume set to 30%')
            elif countperson == 4:
                # Set volume to 40%
                volume.SetMasterVolumeLevel(-9.0, None)
                volume.SetMute(0, None)
                print('Volume set to 40%')
            elif countperson >= 5:
                # Set volume to 100%
                volume.SetMasterVolumeLevel(0.0, None)
                volume.SetMute(0, None)
                print('Volume set to 100%')
            elif countperson == 0:
                # Mute the speaker
                volume.SetMute(1, None)
                print('Speaker muted')