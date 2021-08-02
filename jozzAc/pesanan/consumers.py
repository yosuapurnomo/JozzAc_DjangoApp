from channels.consumer import AsyncConsumer
import asyncio
import json
from django.utils import formats
from channels.db import database_sync_to_async
from django.core import serializers
from .models import InvoiceModel

class PesananConsumer(AsyncConsumer):
	
	async def websocket_connect(self, event):
		await self.send({
			"type":"websocket.accept",
			# 'text':'hello'
			})
		data = await self.get_data(self.scope['url_route']['kwargs']['id'])
		pesanan = data[0]
		client = data[1]
		my_data = {
			'kwitansi':pesanan.Invoice,
			'keterangan':pesanan.Keterangan,
			'payment': pesanan.get_statusPembayaran_display(),
			'total':pesanan.totalInvoice,
			'nama':client.nama_Client,
			'telp':client.noTelp_Client,
			'alamat':client.alamat_Client,
			'kota':client.kota_Client,
			'approve':data[2],
			'teknisi':data[4],
			'spkProgress':data[3]
		}
		# await asyncio.sleep(3)
		await self.send({
			"type":"websocket.send",
			"text":json.dumps(my_data),
			})

	async def websocket_receive(self, event):
		print("receive", event)

	async def websocket_disconnect(self, event):
		print("disconnect", event)

	@database_sync_to_async
	def get_data(self, id):
		data = InvoiceModel.objects.get(id=id)
		client = data.clientINV
		approv = data.ApprovPesanan if hasattr(data, 'ApprovPesanan') else False
		print(approv.approve)
		spk = data.SPK if hasattr(data, 'SPK') else '-'
		if spk != '-':
			progress = spk.get_status_display()
			teknisi = spk.teknisi.username
		else: teknisi, progress = '-', 'Belum Ada SPK'

		dataAll = [data, client, approv.approve, progress, teknisi.upper()]
		return dataAll


class InvoiceConsumer(AsyncConsumer):
	async def websocket_connect(self, event):
		print(self.scope['url_route']['kwargs']['invoice'])
		await self.send({
			"type":"websocket.accept",
			})

		get_data = await self.get_invoice(self.scope['url_route']['kwargs']['invoice'])
		if get_data == False:
			data = {
			'invoice': False,
			}
		else:
			inv = get_data[0]
			client = get_data[1]
			data = {
				'invoice':inv.Invoice,
				'statusPembayaran':inv.get_statusPembayaran_display(),
				'Keterangan':inv.Keterangan,
				'tanggal':str(formats.date_format(inv.tanggal, "d-M-Y")),
				'totalInvoice':inv.totalInvoice,
				'slug':inv.slug_Invoice,
				'clientINV':client.nama_Client,

			}
			
		
		await self.send({
			"type":"websocket.send",
			"text":json.dumps(data),
			})

	async def websocket_receive(self, event):
		print("receive", event)

	async def websocket_disconnect(self, event):
		print("disconnect", event)

	@database_sync_to_async
	def get_invoice(self, invoice):
		key = str(invoice).replace('_', '/')
		try:
			inv = InvoiceModel.objects.filter(Invoice__contains=key)[0]
			client = inv.clientINV if hasattr(inv, 'clientINV') else '-'
			print(client)
			dataAll = [inv, client]
		except Exception as e:
			dataAll = False
		
		
		return dataAll