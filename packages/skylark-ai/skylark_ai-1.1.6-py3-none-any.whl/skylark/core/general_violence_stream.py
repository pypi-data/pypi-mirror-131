from skylark.core.streams import StreamClient

import cv2
import time
import asyncio
from skylark.core.clients import RealTimeClient
from skylark.core.clients import Service
import logging
from skylark.utils.utils import VideoGet
import numpy as np
from math import ceil, floor
import math
import base64


class GeneralViolenceStreamClient(StreamClient):
    def __init__(self,id, fps, batch_size, sampling_rate, token, show_processed_stream=False,
        save_raw_frames=False, scale_percent=100, quality=95, stream=0):
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
        self.client = RealTimeClient(Service.GENERAL_VIOLENCE, self.on_receive, batch_size, self.on_network_status_change, self.token)
        print("hit done")
        self.response_jsons = []
        self.show_processed_stream = show_processed_stream
        self.save_raw_frames = save_raw_frames
        self.scale_percent = scale_percent
        self.quality = quality
        self.id = id
        self.start_stream = self.start_stream
        self.show_stream = self.show_stream
        self.createTasks()

    
    def np_from_json(self, obj, prefix_name=""):
        return np.frombuffer(base64.b64decode(obj["{}_item".format(prefix_name)].encode("utf-8")),
                            dtype=np.dtype(obj["{}_dtype".format(prefix_name)])).reshape(
            obj["{}_shape".format(prefix_name)])

    def postprocess(self,frames,s_hat, y_hat, w, h):
            postprocessed_frames = []
            # y_hat, s_hat = outputs
            s_hat = s_hat[0]
            print(y_hat)
            y_prob = self.softmax(y_hat)
            y_hat = y_hat.argmax(1)
            y_hat = y_hat[0]
            y_prob = y_prob[0][y_hat]
            print(f'Predicted: {"violence" if y_hat == 1 else "nonviolence"} | Prob: {y_prob:.5f}')
            predict = "violence" if y_hat == 1 else "nonviolence"
            for frame_idx, frame in enumerate(frames):
                frame = cv2.resize(frame, (w, h))
                frame = cv2.putText(frame, predict,(10, 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
                if y_hat == 1 and y_prob >= 0.9:
                    if frame_idx % (len(frames) // 4) == 0 and len(s_hat) > 0:
                        latest_sampled_detections = s_hat[0]
                        s_hat = s_hat[1:]
                        boxes = self.get_bounding_boxes(latest_sampled_detections, (w, h))

                    heatmap = self.heatmap_to_rgb(latest_sampled_detections, (w, h))

                    for box in boxes:
                        bx, by, bw, bh = cv2.boundingRect(box)
                        frame[by: by + bh, bx: bx + bw] = 0.7 * frame[by: by + bh,
                                                                    bx: bx + bw] + 0.3 * heatmap[by: by + bh, bx: bx + bw]
                        cv2.rectangle(frame, (bx, by), (bx+bw, by+bh), (0, 0, 255), 3)

                postprocessed_frames.append(frame)
            return postprocessed_frames

    def scale_coordinates(self, json):
        # results = json['results']
        # prediction = results['prediction']
        output =json['results']

        s_hat = self.np_from_json(output['s_hat'])

        y_hat = self.np_from_json(output['y_hat'])
        new_result = {}
        new_result['s_hat']= s_hat
        new_result['y_hat'] = y_hat

        json['results'] = new_result
        print("################################################  converted json #################################################")
        print(json)

        # json['prediction'] = prediction
        # print("###################################################  JSON IS  ###############################################")
        # print(json['prediction'])
        # print(json)
    

    
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
                        self.delay_sec = 1/(self.fps + len(self.frames)/5)
                        results = response["results"]
                        print(results)
                        postprocessed_frames = self.postprocess(self.frames, results['s_hat'], results['y_hat'], 720, 720)
                        # results = results["final_output"]
                    
                        for frame in postprocessed_frames:
                            # frame = self.frames.pop(0)
                            start_time = time.time()
                            # for result in results:
                            #     print(result)
                            #     start = (int(result[0]), int(result[1]))
                            #     end = (int(result[2]), int(result[3]))
                            #     if int(result[0]) != -1:
                            #         frame = cv2.rectangle(frame,start,end, (255,0,0),3)
                            cv2.imshow(str(self.id), frame)
                            cv2.waitKey(1)
                            time_spent = time.time() - start_time
                            rem_time = max(self.delay_sec - time_spent, 0)
                            await asyncio.sleep(rem_time)

                    except Exception as e:
                        logging.exception("Error")
                        print("ex in face_mask_stream line 129")
                        exit()

        
    async def start_stream(self):
        # variable used to maintain the count of frames already sampled
        print("CUSTOM START STREAM................................................................")
        counter = 0
        while True:
            try:
                
                start = time.time()
                frame = self.vid.frame
                cv2.imshow('inputstream', frame)
                self.frames.append(frame)
                print("len of frames")
                print(self.frames.__len__())
                # for every frames equal to sample_length picking one frame from the middle and sending for processing
                counter = (counter + 1) % self.sample_length
                if counter == 0:
                    # print("len:")
                    # print(self.frames.__len__())
                    selected_frame = self.frames[-self.sample_length:][-int(math.floor(math.floor(self.sample_length / 2)))]
                    if not self.save_raw_frames:
                        self.frames = []

                    if self.scale_percent is not 100:
                        # print(selected_frame.shape)
                        # width = int(selected_frame.shape[1] * self.scale_percent / 100)
                        # height = int(selected_frame.shape[0] * self.scale_percent / 100)
                        # dim = (width, height)
                        selected_frame = cv2.resize(selected_frame, (256,190), interpolation=cv2.INTER_LINEAR)
                        # selected_frame = self.preprocess_frame(frame, spatial_resolution)
                        print(selected_frame.shape)
                    if self.quality is not 100 and selected_frame is not None:
                        encode_params = [cv2.IMWRITE_JPEG_QUALITY, self.quality]
                        byte_array = cv2.imencode('.jpg', selected_frame, encode_params)[1].tostring()

                    elif selected_frame is not None:
                        byte_array = cv2.imencode('.jpg', selected_frame)[1].tostring()
                    await self.client.start_stream(byte_array)
                time_spent = time.time() - start
                rem_time = max(self.delay_sec - time_spent, 0)
                await asyncio.sleep(rem_time)
                # if q is pressed we stop showing output stream
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    self.vid.stop()
                    cv2.destroyAllWindows()
                    break

            except Exception as e:
                # print("EEEEEEEEEEEXXXXXXXXXXXXXX")
                logging.error("Error")
                print(str(e))
                exit()

    
    def get_bounding_boxes(self, spatial_detection, reshape):
        spatial_detection = cv2.resize(np.array(spatial_detection), reshape)
        spatial_detection *= 255.0

        spatial_detection = spatial_detection.astype('uint8')
        thresh = cv2.threshold(spatial_detection, 0, 255,
                            cv2.THRESH_OTSU + cv2.THRESH_BINARY)[1]

        cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]

        return cnts
    
    def softmax(self, x):
        e_x = np.exp(x - np.max(x))
        return e_x / e_x.sum(axis=1)

    def heatmap_to_rgb(self, heatmap: np.ndarray, reshape=None, heatmap_style=cv2.COLORMAP_JET):
        heatmap = (heatmap - heatmap.min())/(heatmap.ptp())
        heatmap = (heatmap * 255.0).astype('uint8')

        heatmap = cv2.applyColorMap(heatmap, heatmap_style)

        if reshape:
            heatmap = cv2.resize(heatmap, reshape)

        return heatmap

def draw_boxes(self, frame, coord_list, color, thickness):
    for coords in coord_list:
        start_point = (int(coords[0]),int(coords[1]))
        end_point = (int(coords[2]),int(coords[3]))
        frame = cv2.rectangle(frame,start_point,end_point, color, 3)
    return frame
