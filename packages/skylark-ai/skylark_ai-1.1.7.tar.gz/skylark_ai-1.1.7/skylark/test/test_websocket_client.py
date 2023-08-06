
import sys


sys.path.append('C:/Users/jrish/work/python-sdk/skylark_ai')
# print(sys.path)

from skylark.core.clients import Service
from skylark.core.face_mask_stream import FaceMaskStreamClient
from skylark.core.face_detect_stream import FaceDetectStreamClient
from skylark.core.weapon_detection_stream import WeaponDetectionStreamClient
from skylark.core.facial_landmark_stream import FacialLandmarkStream
from skylark.core.lie_detection_stream import LieDetectionStreamClient
from skylark.core.night_day_stream import NightDayStreamClient
from skylark.core.cab_violence_stream import CabViolenceStreamClient
from skylark.core.face_recog_stream import FaceRecogStreamClient
from skylark.core.general_violence_stream import GeneralViolenceStreamClient
from skylark.core.pedestrian_detect_stream import PedestrianDetectionStreamClient
from skylark.core.crowd_counting_stream import CrowdCountingStreamClient
from skylark.core.dress_insights_stream import DressInsightStreamClient
import time
from skylark.utils.utils import is_connected
from threading import Thread
from skylark.core.multi_stream import MultiStreamer




# user will add authorization token here
token = "abcd"

# user will send fps of incoming stream, size of batch that will be formed while processing ,

# user can continue to perform any further tasks as per need
if __name__ == '__main__':
    print('starting')
    dict = {}
    dict['id'] = 1
    dict['service_name'] = Service.FACE_DETECT
    dict['stream_url'] = "rtsp://admin:admin123@203.134.200.170:8000/cam/realmonitor?channel=12&subtype=0"
    dict['fps'] = 15
    dict['batch_size']=1
    dict['sampling_rate']=1
    dict['show_processed_stream']=True
    dict['save_raw_frames'] = True
    dict['scale_percent'] = 25
    dict['quality'] = 95
    # dict['databaseID']="2db2ae96-f341-4767-8e68-6ddd1c2f972b"
    service_details = dict
    
    client = FaceDetectStreamClient(
                id=dict['id'],
                stream=service_details['stream_url'],
                fps=service_details['fps'],
                batch_size=service_details['batch_size'],
                sampling_rate=service_details['sampling_rate'],
                token=token,
                show_processed_stream=service_details['show_processed_stream'],
                save_raw_frames=service_details['save_raw_frames'],
                scale_percent=service_details['scale_percent'],
                quality=service_details['quality'],
                # databaseID=service_details['databaseID'],
            )

try:
    i=0
    while True:
        print("in mian")
        # print(client.response_jsons)
        time.sleep(1)
except KeyboardInterrupt:
	print("exiting")
	exit()
	
