from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import JsonResponse
from django.utils.dateformat import format
from django.db.models import Q

from django.forms import ModelForm
from django.core.urlresolvers import reverse_lazy
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from celery.result import AsyncResult
from datetime import datetime
import time

from main.models import *
from main.tasks import *

from modules.interface_factory import *
from modules.ajax_response import *


# Create your views here.
def admin(request):
    return redirect('/admin/', permanent=True)

def home(request):
	context = {}
	context['source'] = "test"
	context['location_dropdown'] = getDropdown('location',TripAdvisorLocation)
	context['trip_category_dropdown'] = getDropdown('trip_category',TripAdvisorCat)
	context['status_rows'] = get_all_status_rows()
	#print context['status_rows']

	#return render_to_response('new_crawl.html', context)
	return render(request, 'home.html', context)

def results(request):
	context = {}
	context['status_rows'] = get_all_results()
	return render(request, 'results.html', context)	

def process_form(request):
	parameters = {}
	scrape = '1'
	message = ''

	try:
		parameters['source'] = request.POST.get("source","")
		parameters['keyword'] = request.POST.get("keyword","")

		if parameters['source'] == 'facebook':
			parameters['token'] =  request.POST.get("fb_token","")
			#check if the keyword is already scrapped
			crawler_record = CrawlerRecord.objects.get(keyword=parameters['keyword'])
			if crawler_record:
				scrape = '0'
				message = 'Keyword " %s " already Scrapped. Please search on Result Page'%parameters['keyword'].lower()

		elif parameters['source'] == 'tripadvisor':
			parameters['category'] = request.POST.get("category","")
			parameters['location'] = request.POST.get("location","")
			keyword = parameters['category']+ ' '+parameters['location']
			crawler_record = CrawlerRecord.objects.get(keyword=keyword)
                        if crawler_record:
                                scrape = '0'
                                message = 'Keyword " %s " already Scrapped. Please search on Result Page'%keyword

		elif  parameters['source'] == 'yelp':
			parameters['term'] = request.POST.get("term","")
			parameters['location'] = request.POST.get("location","")
			keyword = parameters['term']+ ' '+parameters['location']
                        crawler_record = CrawlerRecord.objects.get(keyword=keyword)
                        if crawler_record:
                                scrape = '0'
                                message = 'Keyword " %s " already Scrapped. Please search on Result Page'%keyword
		
	except Exception as ex:
		print ex

	if scrape == '1':
		task = run_scraper(parameters)
		res = AsyncResult(task.task_id)
		message = res.state

	data = {'status':scrape,'msg':message}

	#return "{'status':'"+str(res.ready())+"'}"
	return JsonResponse(data)

def auto_refresh(request):
	output = []
	record = CrawlerRecord.objects.filter(updated_time__gte =  int(format(datetime.now(), u'U')) - 10)
	for rec in record:
		started_time = time.strftime("%D %H:%M", time.localtime(float(rec.start_time)))
		status = rec.status
		if status == 'SUCCESS':
			status = status + ' : <a href = "download_result/?id=%d&site=%s"> Download </a>'%(rec.id,rec.site.name)

		total_time = 0
		try:
			total_time  = int(rec.end_time) - int(rec.start_time)
		except:
			pass

		row = '<tr id="crawler_status_%d"><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%d Min</td>/tr>'%(rec.id,rec.site.name,rec.keyword,started_time,status,rec.records_downloaded,total_time/60)
		data = {'id':rec.id, 'row':row,'mode':'refresh'}
		output.append(data)
	#return "{'status':'"+str(res.ready())+"'}"
	#print output

	#queues = CrawlerRecord.objects.filter(Q(status='PENDING') | Q(status='RUNNING') )
	'''
	queues = CrawlerRecord.objects.filter(id__in=[1, 3, 4, 5, 6])
	print len(queues)
	for queue in queues:
		res = AsyncResult(queue.task_id)
		try:
			print res.state
		except:
			print 'ERROR'
	
	ids = request.GET.get("id","").split(",")
	record = CrawlerRecord.objects.filter(id__in=ids)
	for row in record:
		print row.site
	'''
	return JsonResponse(output,safe=False)


def download_result(request):
	if not request.GET.get("id",""):
		return 'Error'
	else:
		import djqscsv
		#crawler = CrawlerRecord.objects.get(id=request.GET.get("id",""))
		crawler_record = CrawlerRecord.objects.get(id=request.GET.get("id",""))
		crawler_mappings = CrawlerSiteMapping.objects.filter(crawler_record = crawler_record, site = Site.objects.get(name=request.GET.get("site","")))
		row_id = []
		for mapping in crawler_mappings:
			row_id.append(mapping.site_row_id)
		#if crawler.site.name == 'facebook':
		#print row_id
		site = crawler_record.site.name

		if site == 'facebook':
			query = FacebookPage.objects.filter(id__in=row_id)
		elif site == 'tripadvisor':
			query = TripAdvisorAttraction.objects.filter(id__in=row_id)
	
		elif site == 'yelp':
			query = Yelp.objects.filter(id__in=row_id)

		return djqscsv.render_to_csv_response(query,filename=crawler_record.keyword)


class CrawlerRecordForm(ModelForm):
	class Meta:
		model = CrawlerRecord
		fields = ['id','site','keyword']
		template_name = 'results_list.html'

def results_list(request, template_name='results_list.html'):
    cr = CrawlerRecord.objects.all().order_by("-id")
    paginator = Paginator(cr, 10) # Show 10 per page
    page = request.GET.get('page')
    try:
    	records = paginator.page(page)
    except PageNotAnInteger:
    	records = paginator.page(1)
    except EmptyPage:
    	records = paginator.page(paginator.num_pages)

    data = {}
    data['rows'] = getCrawlerRows(records)
    data['records'] = records #records#cr 
    return render(request, template_name, data)

def results_edit(request, pk, template_name='results_form.html'):
	cr = get_object_or_404(CrawlerRecord, pk=pk)
	form = CrawlerRecordForm(request.POST or None, instance=cr)
	if form.is_valid():
		form.save()
		return redirect('results_list')
	return render(request, template_name, {'form':form})

def results_delete(request, pk, template_name='results_form.html'):
	cr = get_object_or_404(CrawlerRecord, pk=pk)
	if request.method=='POST':
		cr.delete()
		return redirect('results_list')
	return render(request, template_name, {'object':cr})
