import threading
import json
import time
from enum import Enum
from functools import reduce
import uuid

import os
import socket
import asyncio
import websockets

from skylark.utils.utils import get_websocket_auth_token, get_bytes_from_file
from skylark.constants.constants import HOST
from skylark.utils.utils import is_connected
import websocket
import ssl



class Service(Enum):
	FACE_MASK = 1,
	FACE_DETECT = 2,
	FACIAL_LANDMARK = 3,
	WEAPON_DETECTION = 4,
	LIE_DETECTION = 5,
	NIGHT_DAY = 6,
	CAB_VIOLENCE = 7,
	TEMPORAL = 8,
	FACE_RECOG = 9,
	GENERAL_VIOLENCE=10,
	PEDESTRIAN_DETECTION=11,
	CROWD_COUNTING=12,
	DRESS_INSIGHTS = 13,

	def get_uri(self):
		return service_uri_map.get(self, None)


service_uri_map = {
	Service.FACE_MASK: "face-mask/",
	Service.FACE_DETECT: "face-detect/",
	Service.FACIAL_LANDMARK: "facial-landmark/",
	Service.WEAPON_DETECTION: "weapon-detection/",
	Service.LIE_DETECTION: "lie-detection/",
	Service.NIGHT_DAY: "night-day/",
	Service.CAB_VIOLENCE: "cab-violence/",
	Service.TEMPORAL:"process-temporal/",
	Service.FACE_RECOG: "face-recog-bulk/",
	Service.GENERAL_VIOLENCE:"violence-detection/",
	Service.PEDESTRIAN_DETECTION:"pedestrian-detection/",
	Service.CROWD_COUNTING:"crowd-counting/",
	Service.DRESS_INSIGHTS: "dress-insights/",

}


class RealTimeClient:
	protocol = "ws://"
	route = "ws/"

	def get_or_create_eventloop(self):
		try:
			print("getting loop")
			return asyncio.get_event_loop()
		except RuntimeError as ex:
			if "There is no current event loop in thread" in str(ex):
				loop = asyncio.new_event_loop()
				print("no loop !!!")
				asyncio.set_event_loop(loop)
				return asyncio.get_event_loop()

	def __init__(self, service, on_receive, batch_size, on_network_status_change, token=None, databaseID=None):
		self.service = service
		self.on_network_status_change = on_network_status_change
		self.url = self.protocol + HOST + "/" + self.route + service.get_uri()
		self.path = os.path.join(os.getcwd(), "media", "directory_streams", "test_stream")
		print(self.url)
		self.databaseID = databaseID
		print("got token")
		print(token)
		self.token = token
		self.syncid = 0
		self.websocket_token = get_websocket_auth_token(token)
		print("token")
		print(self.websocket_token)
		self.on_receive = on_receive
		self.url = self.url + "?authorization=%s" % self.websocket_token
		print("url is :")
		print(self.url)
		self.websocket = None
		loop = self.get_or_create_eventloop()
		loop.run_until_complete(self._connect())
		loop.run_until_complete(self.set_batch_size(batch_size))
		loop.run_until_complete(self.set_databaseID(databaseID))

	async def start_stream(self, byte_array):
		while self.websocket is None:
			print("none")
			await asyncio.sleep(1)
			continue
		try:
			if byte_array is not None:
				# starting and sending frame one by one
				await self.start_frame(byte_array.__len__(), self.syncid)
				await self.send_frame(byte_array)
		except websockets.exceptions.ConnectionClosed:
			print("connection closed in start stream")
			print("re-establishing connection...")
			self.websocket = None
			await self.on_network_status_change()

		except socket.gaierror:
			await self.on_network_status_change()

	async def set_batch_size(self, batch_size):
		print("setting batch size")
		while self.websocket is None:
			# if connection is closed we wait for reconnection
			print("none")
			await asyncio.sleep(1)
			continue
		try:
			if is_connected():
				await self.websocket.send(json.dumps({
					"action": 'set_batch_size',
					"batchSize": batch_size
				}))
			else:
				self.websocket = None
				await self.on_network_status_change()

		except websockets.exceptions.ConnectionClosed:
			print("connection closed in setting batch size")
			print("re-establishing connection...")
			self.websocket = None
			await self.on_network_status_change()

	async def set_databaseID(self, databaseID):
		print("setting batch size")
		while self.websocket is None:
			# if connection is closed we wait for reconnection
			print("none")
			await asyncio.sleep(1)
			continue
		try:
			if is_connected():
				await self.websocket.send(json.dumps({
					"action": 'set_database',
					"database_id": databaseID
				}))
			else:
				self.websocket = None
				await self.on_network_status_change()

		except websockets.exceptions.ConnectionClosed:
			print("connection closed in setting batch size")
			print("re-establishing connection...")
			self.websocket = None
			await self.on_network_status_change()


	async def start_frame(self, byte_length, syncid):
		print("starting frame")
		self.syncid = self.syncid + 1
		while self.websocket is None:
			await asyncio.sleep(1)
			print("none found")
			continue
		try:
			if is_connected():
				print("sending frames!!")
				await self.websocket.send(json.dumps({
					"fileSize": byte_length,
					"syncId": syncid,
					"action": "start_frame"
				}))
			else:
				self.websocket = None
				# await self.on_network_status_change()

		except websockets.exceptions.ConnectionClosed:
			print("connection closed in starting frame")
			print("re-establishing connection...")
			self.websocket = None
			await self.on_network_status_change()

	async def send_frame(self, array):
		while self.websocket is None:
			print("none")
			await asyncio.sleep(1)
			continue
		try:
			if is_connected(): 
			# the converted bytearray is sent using websockets
				await self.websocket.send(array)
			else:
				self.websocket = None
				# await self.on_network_status_change()

		except websockets.exceptions.ConnectionClosed:
			print("connection closed in sending frame")
			print("re-establishing connection...")
			self.websocket = None
			await self.on_network_status_change()

	def connect(self, loop):
		asyncio.set_event_loop(loop)
		loop.run_until_complete(self._connect())

	async def receive_message(self):
		while self.websocket is None:
			print("none")
			await asyncio.sleep(1)
			continue
		while True:
			print('inside receive msg')
			try:
				# when a message is received, its converted to dictionary and sent for processing
				message = await self.websocket.recv()
				print(message)
				self.on_receive(json.loads(message))
			except websockets.exceptions.ConnectionClosed:
				print("connection closed in recieve msg")
				print("re-establishing connection...")
				self.websocket = None
				await self.on_network_status_change()
			except socket.gaierror:
				await self.on_network_status_change()
			except Exception as e:
				print(e)

	async def _connect(self):
		if self.websocket is None:
			try:
				self.websocket = await websockets.connect(self.url)
				if self.websocket.open:
					print("Connection established correctly. Client Connected!")
				# self.websocket = websocket.WebSocketApp(self.url )
				# self.socketself.websocket.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
						
				await asyncio.sleep(1)
			except socket.gaierror:
				print("client.py socket error!!")
				await asyncio.sleep(1)
				await self.on_network_status_change()
		else:
			print("Already Connected!")

	async def re_connect(self):
		# if internet is down we try and reconnect
		if self.websocket is None:
			print("Internet not found while reconnecting..")
			await self._connect()
