from channels.consumer import AsyncConsumer
import asyncio
import json
from django.utils import formats
from channels.db import database_sync_to_async
from .models import pembayaranModel


class getPayment(AsyncConsumer):
	async def websocket_connect(self, event):
		await self.send({"type":"websocket.accept"})
		key=self.scope['url_route']['kwargs']['key']
		data = await self.get_data(key)
		if data != False:
			dataPayment = {
			'no_pembayaran':data[0].no_pembayaran,
			'tgl_input': str(formats.date_format(data[0].tgl_input, 'd M Y')),
			'invoice':data[1],
			'admin':data[2],
			'jumlah':data[0].jumlah,
			'keterangan':data[0].keterangan,
			'tgl_pembayaran':str(formats.date_format(data[0].tgl_pembayaran, 'd M Y')),
			'slug_pembayaran':data[0].slug_pembayaran
			}
		else:
			dataPayment = {
			'no_pembayaran': False
			}
		await self.send({
			"type":"websocket.send",
			"text":json.dumps(dataPayment),
			})

	@database_sync_to_async
	def get_data(self, key):
		try:
			key = str(key).replace('_', '/')
			data = pembayaranModel.objects.filter(no_pembayaran__contains=key)[0]
			invoice = data.invoice if hasattr(data, 'invoice') else '-'
			if invoice != '-':
				invoice = invoice.Invoice
			user = data.admin if hasattr(data, 'admin') else '-'
			if user != '-':
				user = user.username
			dataAll = [data, invoice, user]
		except Exception as e:
			dataAll = False
		

		return dataAll