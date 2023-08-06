from skylark.core.streams import StreamClient

import cv2
import time
import asyncio
from skylark.core.clients import RealTimeClient
from skylark.core.clients import Service


class LieDetectionStreamClient(StreamClient):
	def __init__(self, fps, batch_size, sampling_rate, token):
		self.fps = fps
		self.frames = []
		self.json = ""
		self.syncid = -1
		self.batch_size = batch_size
		self.sampling_rate = sampling_rate
		self.sample_length = int(fps / sampling_rate)
		self.delay_sec = 1 / self.fps
		self.vid = cv2.VideoCapture(0, cv2.CAP_DSHOW)
		self.token = token
		self.client = RealTimeClient(Service.LIE_DETECTION, self.on_receive, batch_size,
		                             self.on_network_status_change, token)
		self.response_jsons = []
		self.createTasks()

	async def show_stream(self):
		# on message receive from websocket, we parse json response and show stream using cv2
		while True:
			if len(self.response_jsons) == 0:
				# if no responses then keep waiting for some message to be received
				print("waiting")
				await asyncio.sleep(1)
				continue
			# take out one of the response from beginning and apply the result to the frames
			response = self.response_jsons.pop(0)
			print(response)
			# syncid is used to maintain between sent and received frames
			self.syncid = self.syncid + self.batch_size
			syncids = response["sync"]
			if self.syncid != syncids[-1]:
				# if syncid sent and received for a particular response is not same then acheive sync
				print("not in sync:")
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
						self.frames.pop()
						self.syncid = self.syncid + 1
				continue
			else:
				try:
					result = response["results"]
					print(result)
					prediction = result["class"]
					for i in range(self.sample_length):
						color = (255, 0, 0)
						start = time.time()
						frame = self.frames.pop(0)
						thickness = 2
						print(prediction)
						font = cv2.FONT_HERSHEY_SIMPLEX
						fontScale = 1
						org = (50, 50)
						if prediction != "Lie":
							color = (0, 0, 255)
						cv2.imshow('outputstream', cv2.putText(frame, prediction+" ", org, font, fontScale, color, thickness, cv2.LINE_AA))
						time_spent = time.time() - start
						rem_time = max(self.delay_sec - time_spent, 0)
						await asyncio.sleep(rem_time)
				except Exception as e:
					print("Exception:" + e)
