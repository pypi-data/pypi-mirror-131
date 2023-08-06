import cv2
import time
import asyncio
import math
import threading
import json
from skylark.core.clients import RealTimeClient
import sys
import imutils
from skylark.utils.utils import VideoGet
import logging


class StreamClient:
	def __init__(self, fps, batch_size, sampling_rate, service,
	 show_stream, scale_coordinates, token, show_processed_stream=False, save_raw_frames=False, scale_percent=100, quality=100,stream=0):
		self.fps = fps
		self.frames = []
		self.json = ""
		self.syncid = -1
		self.batch_size = batch_size
		self.sampling_rate = sampling_rate
		self.sample_length = int(fps / sampling_rate)
		self.delay_sec = 1 / self.fps
		self.show_stream = show_stream
		self.scale_coordinates = scale_coordinates
		self.stream = stream
		# self.vid = VideoGet(self.stream).start()
		self.vid = VideoGet(self.stream).start()
		print(self.stream)
		self.service = service
		self.token = token
		self.show_processed_stream = show_processed_stream
		self.save_raw_frames = save_raw_frames
		self.scale_percent = scale_percent
		self.quality = quality
		self.client = RealTimeClient(service, self.on_receive, batch_size, self.on_network_status_change, token)
		self.response_jsons = []
		self.tasksThread = None
		self.createTasks()
	
	def get_or_create_eventloop(self):
		try:
			return asyncio.get_event_loop()
		except RuntimeError as ex:
			if "There is no current event loop in thread" in str(ex):
				loop = asyncio.new_event_loop()
				asyncio.set_event_loop(loop)
				return asyncio.get_event_loop()


	def createTasks(self):
		# running these three tasks on a seperate thread so that the main thread does'nt gets blocked
		# print(self.show)
		if self.show_processed_stream:
			tasks = [
				asyncio.ensure_future(self.start_stream()),
				asyncio.ensure_future(self.client.receive_message()),
				asyncio.ensure_future(self.show_stream()),
			]
		else:
			tasks = [
				asyncio.ensure_future(self.start_stream()),
				asyncio.ensure_future(self.client.receive_message()),
			]
		self.tasksThread = threading.Thread(target=self.run_tasks, args=(self.get_or_create_eventloop(), tasks))
		self.tasksThread.setDaemon(True)
		self.tasksThread.start()





	async def on_network_status_change(self):
		# method to restart tasks stopped if some network issue occurs and websocket connection gets closed
		print("re-running tasks")
		await self.client.re_connect()
		await asyncio.sleep(3)

	def run_tasks(self, loop, tasks):
		# runs the tasks sent as a list here
		asyncio.set_event_loop(loop)
		loop.run_until_complete(asyncio.wait(tasks))

		

	def on_receive(self, json):
		try:
			# whenever a message is received we store them in a list
			if "results" in json and self.frames.__len__() > 0:
				self.response_jsons.append(json)
				print(len(self.response_jsons))
				# print(json)
				if self.scale_percent is not 100:
					self.scale_coordinates(json)
				print("results there in response hence appended")
			else:
				print(json)

		except Exception as e:
			logging.error("streams.py")
			print(str(e))
			exit()

	async def start_stream(self):
		# variable used to maintain the count of frames already sampled
		counter = 0
		while True:
			try:
				
				start = time.time()
				frame = self.vid.frame
				# cv2.imshow('inputstream', frame)
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
						width = int(selected_frame.shape[1] * self.scale_percent / 100)
						height = int(selected_frame.shape[0] * self.scale_percent / 100)
						dim = (width, height)
						selected_frame = cv2.resize(selected_frame, dim)
						# print(selected_frame.shape)
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
