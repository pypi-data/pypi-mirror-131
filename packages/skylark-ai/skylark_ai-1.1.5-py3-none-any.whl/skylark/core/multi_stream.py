
import sys

from skylark.core.clients import Service
from skylark.core.face_mask_stream import FaceMaskStreamClient
from skylark.core.face_detect_stream import FaceDetectStreamClient
from skylark.core.weapon_detection_stream import WeaponDetectionStreamClient
from skylark.core.facial_landmark_stream import FacialLandmarkStream
from skylark.core.lie_detection_stream import LieDetectionStreamClient
from skylark.core.night_day_stream import NightDayStreamClient
import time
from skylark.utils.utils import is_connected
from threading import Thread



# accepts a valid api_key and a list of form [{service_name,stream_url }, {service_name,stream_url} .....  ]

class MultiStreamer():
    def __init__(self, token, service_dict):
        self.token = token
        self.service_dict = service_dict
        self.client = []
        self.multi_stream()
        

    def multi_stream(self):
        #start the streams here using dictionary list:
        id = 0
        for item in self.service_dict:
            print("starting threads")
            print(item)
            Thread(target=self.func, args=(id, item)).start()
            id = id+1


# user will send fps of incoming stream, size of batch that will be formed while processing ,
# the rate at which sampling is done, and the token
    def func(self, id, service_details):
        if service_details['service_name'] == 'face_mask':
            self.client.append(FaceMaskStreamClient(
                id=id,
                stream=service_details['stream_url'],
                fps=service_details['fps'],
                batch_size=service_details['batch_size'],
                sampling_rate=service_details['sampling_rate'],
                token=self.token,
                show_processed_stream=service_details['show_processed_stream'],
                save_raw_frames=service_details['save_raw_frames'],
                scale_percent=service_details['scale_percent'],
                quality=service_details['quality']
            )
            )
        if service_details['service_name'] == Service.FACE_DETECT:
            print("face-detect starting")
            self.client.append(FaceDetectStreamClient(
                id=id,
                stream=service_details['stream_url'],
                fps=service_details['fps'],
                batch_size=service_details['batch_size'],
                sampling_rate=service_details['sampling_rate'],
                token=self.token,
                show_processed_stream=service_details['show_processed_stream'],
                save_raw_frames=service_details['save_raw_frames'],
                scale_percent=service_details['scale_percent'],
                quality=service_details['quality']
            )
            )


# user can continue to perform any further tasks as per need

	
