from channels.consumer import AsyncConsumer
import asyncio
import json
from django.utils import formats
from channels.db import database_sync_to_async
from django.core import serializers
from .models import SPKModel

class getSPK(AsyncConsumer):

	async def websocket_connect(self, event):
		await self.send({"type":"websocket.accept"})
		key=self.scope['url_route']['kwargs']['key']
		data = await self.get_data(key)
		if data != False:
			dataSPK = data[0]
			teknisi = data[1]
			pesanan = data[2]
			my_data = {
				'no_SPK':dataSPK.no_SPK,
				'tgl_input':formats.date_format(dataSPK.tgl_input, "d M Y"),
				'teknisi':teknisi.username,
				'pesanan':pesanan.Invoice,
				'keterangan': dataSPK.keterangan,
				'tgl_pengerjaan': formats.date_format(dataSPK.tgl_pengerjaan, "d M Y"),
				'keterangan': dataSPK.keterangan,
				'status': dataSPK.get_status_display(),
				'slug':dataSPK.slug_SPK,
			}
		else:
			my_data = {
			'no_SPK': False
			}
		await self.send({
					"type":"websocket.send",
					"text":json.dumps(my_data),
					})

	@database_sync_to_async
	def get_data(self, key):
		try:
			key = str(key).replace('_', '/')
			data = SPKModel.objects.filter(no_SPK__contains=key)[0]
			teknisi = data.teknisi
			pesanan = data.pesanan
			status = data.get_status_display()
			objects = [data, teknisi, pesanan, status]
		except Exception as e:
			objects = False
		
		return objects