from main.models import *
from datetime import datetime
from django.utils.dateformat import format
from django.http import JsonResponse
import time


def getCrawlerRows(records):
	output = []
	for rec in records:
		status = rec.status
		if status == 'SUCCESS':
			status = status + ' : <a href ="http://45.55.35.9/download_result/?id=%d&site=%s"> Download </a>'%(rec.id,rec.site.name)
		started_time = time.strftime("%D %H:%M", time.localtime(int(rec.start_time)))
		total_time = 0
		try:
			total_time  = int(rec.end_time) - int(rec.start_time)
		except:
			pass
		row = '<tr id="crawler_status_%d"><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%d Min</td></tr>'%(rec.id,rec.site.name,rec.keyword,started_time,status,rec.records_downloaded,total_time/60)
		#row = {'id':rec.id, 'site':rec.site.name , 'status':rec.status, 'total':rec.records_downloaded, 'time': rec.start_time}
		#row = {'id':rec.id, 'tr':tr}
		output.append(row)
	#return "{'status':'"+str(res.ready())+"'}"
	#print output
	#return JsonResponse(output,safe=False)	
	return output



def get_all_status_rows():
	#record = reversed(CrawlerRecord.objects.all().order_by("-id")[:5])
	records = CrawlerRecord.objects.all().order_by("-id")[:10]
	return getCrawlerRows(records)

