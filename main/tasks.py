
from celery.decorators import task
from celery.utils.log import get_task_logger
from celery.result import AsyncResult
import time
from datetime import datetime
from django.utils.dateformat import format

from main.models import *
from django.db.models import Q


logger = get_task_logger(__name__)

@task(name="add_num")
def add(a, b):
    logger.info("Sent feedback email"+a+b)


def load_scraper(name):
    name = name.strip('.py')
    s = __import__('main.scrapers.' + name, fromlist=[name])
    return s



@task(name="main.tasks.run_yelp_task")
def run_yelp_task(parameters):
        from main.scrapers.yelpscraper import *
	yp = YelpScraper(parameters)
	yp.search()


@task(name="main.tasks.run_tripadvisor_task")
def run_tripadvisor_task(parameters):
	from main.scrapers.tripadvisor import *
	t = Tripadvisor(parameters['category'],parameters['location'])
	t.main()
	#stat =  f.getSearchResult()


@task(name="main.tasks.run_facebook_task")
def run_facebook_task(parameters):
	from main.scrapers.facebook import *

	f = Facebook(parameters['token'],parameters['keyword'])
	stat =  f.getSearchResult()
	'''
	status = 'FAILED'
	if stat == True:
		status = 'COMPLETED'
	inserted_id = CrawlerRecord.objects.latest('id')
	row = CrawlerRecord.objects.filter(id=inserted_id).update(status = status)
	print status
	print 'here'
	row.save()
	'''




@task(name="execute_scraper")
def run_scraper(parameters):
	#scraper = load_scraper(name)
	if parameters['source'] == 'facebook':
		task = run_facebook_task.delay(parameters)
		time.sleep(2)

	if parameters['source'] == 'yelp':
		task = run_yelp_task.delay(parameters)

	elif parameters['source'] == 'tripadvisor':
		category = parameters['category']
		location = parameters['location']
		try:
			#Check if new category or location?
			if ':' in category:
				cat = category.split(':')
				category = cat[1]
				tc  = TripAdvisorCat.objects.create(name=cat[0],cat=cat[1])
				tc.save()
			if ':' in location:
				loc = location.split(':')
				location = loc[1]
				tl  = TripAdvisorLocation.objects.create(name=loc[0],url=loc[1])
				tc.save()	
		except Exception as ex:
			print ex

		parameters = {'category':category,'location':location}
		print parameters
		task = run_tripadvisor_task.delay(parameters)
		time.sleep(2)

	return task

	#run_facebook_task.apply_async(args=(parameters,))

@task(name="check_status")
def check_status():
	records = CrawlerRecord.objects.filter(Q(status='PENDING') | Q(status='RUNNING') )
	for rec in records:
		try:
			r = AsyncResult(rec.task_id)
			if r.state == 'SUCCESS':
				print 'Updating' + str(rec.id)
				CrawlerRecord.objects.filter(id=rec.id).update(status='SUCCESS', updated_time=int(format(datetime.now(), u'U')))
		except Exception as ex:
			print ex
	pass
