from skylark.core.streams import StreamClient

import cv2
import time
import asyncio
from skylark.core.clients import RealTimeClient
from skylark.core.clients import Service
import logging
from skylark.utils.utils import VideoGet


class FaceRecogStreamClient(StreamClient):
    def __init__(self,id, fps, batch_size, sampling_rate, token, show_processed_stream=False,save_raw_frames=False, scale_percent=100, quality=100, stream=0, databaseID=None):
        self.fps = fps
        self.frames = []
        self.json = ""
        self.syncid = -1
        self.batch_size = batch_size
        self.sampling_rate = sampling_rate
        self.sample_length = int(fps / sampling_rate)
        self.delay_sec = 1 / self.fps
        self.stream = stream
        self.vid = VideoGet(self.stream).start()
        self.token = token
        print("real time hit")
        self.databaseID = databaseID
        self.client = RealTimeClient(Service.FACE_RECOG, self.on_receive, batch_size, self.on_network_status_change, self.token, self.databaseID)
        print("hit done")
        self.response_jsons = []
        self.show_processed_stream = show_processed_stream
        self.save_raw_frames = save_raw_frames
        self.scale_percent = scale_percent
        self.quality = quality
        self.id = id
        self.createTasks()

    def scale_coordinates(self, json):
        print('scaling')
        print(json)
        if 'results' in json:
            print("WHILE SCALING FOUND")
            results = json['results']
            recognitions = results['face_recognition_output']
            print(type(results['face_recognition_output']))
            results = results['final_output']
            new_results = []
            for result in results:
                new_result = [None] * 4
                new_result[0] = int(result[0][0] * 100 / self.scale_percent)
                new_result[1] = int(result[0][1] * 100 / self.scale_percent)
                new_result[2] = int(result[1][0] * 100 / self.scale_percent)
                new_result[3] = int(result[1][1] * 100 / self.scale_percent)
                new_results.append(new_result)
            final_output = {'final_output': new_results }
            # print(recognitions)
            final_output['face_recognition_output'] = recognitions


            json['results'] = final_output
            print("SCALED")
            print(json)

    def draw_boxes(self, frame, coord_list, color, thickness):
        for coords in coord_list:
            start_point = (int(coords[0]),int(coords[1]))
            end_point = (int(coords[2]),int(coords[3]))
            frame = cv2.rectangle(frame,start_point,end_point, color, 3)
        return frame


    async def show_stream(self):
        # on message receive from websocket, we parse json response and show stream using cv2
        if self.show_processed_stream:
            while True:
                try:
                    # print("######################################################show stream")
                    if len(self.response_jsons) == 0:
                        # if no responses then keep waiting for some message to be received
                        print("waiting inside show stream")
                        print(len(self.response_jsons))
                        await asyncio.sleep(1)
                        continue
                    # print("#############################  have content  #############################")
                    print(len(self.response_jsons))
                    # take out one of the response from beginning and apply the result to the frames
                    response = self.response_jsons.pop(0)
                    # syncid is used to maintain between sent and received frames
                    self.syncid = self.syncid + self.batch_size
                    syncids = response["sync"]
                    if self.syncid != syncids[-1]:
                        # if syncid sent and received for a particular response is not same then acheive sync
                        print("##########################not in sync:###################################")
                        print(self.syncid)
                        print(syncids[-1])
                        if self.syncid > syncids[-1]:
                            # discarding results
                            while self.syncid != syncids[-1]:
                                syncids = response["sync"]
                                self.response_jsons.pop(0)
                        else:
                            # discarding frames
                            while self.syncid != syncids[-1]:
                                self.frames.pop(0)
                                self.syncid = self.syncid + 1
                        continue
                    
                except Exception as e:
                    logging.error("Error")
                    exit()

                else:
                    # when in sync move further
                    print("############### in sync ###########################")
                    try:
                        org = (50, 50)
                        font = cv2.FONT_HERSHEY_SIMPLEX
                        fontScale = 0.5
                        color = (255, 0, 0)
                        thickness = 1
                        self.delay_sec = 1/(self.fps + len(self.frames)/5)
                        results = response["results"]
                        print("$$$$$$$$$$$$$ test")
                        print(response)
                        original_response = response['results']
                        print(original_response)
                        results = results["final_output"]
                        match = None
                    
                        for i in range(self.sample_length):
                            frame = self.frames.pop(0)
                            start_time = time.time()
                            k = 0
                            for result in results:
                                print(result)
                                start = (int(result[0]), int(result[1]))
                                end = (int(result[2]), int(result[3]))
                                if int(result[0]) != -1:
                                    frame = cv2.rectangle(frame,start,end, (255,0,0),3)
                                if 'face_recognition_output' in original_response:
                                    org = (start[0]-20, start[1]-20)
                                    recognition = original_response['face_recognition_output'][k]
                                    frame = cv2.putText(frame, recognition, org, font, fontScale, color, thickness, cv2.LINE_AA)
                                k = k+1
                            cv2.imshow(str(self.id), frame)
                            cv2.waitKey(1)
                            time_spent = time.time() - start_time
                            rem_time = max(self.delay_sec - time_spent, 0)
                            await asyncio.sleep(rem_time)

                    except Exception as e:
                        logging.exception("Error")
                        print("ex in face_mask_stream line 129")
                        exit()
