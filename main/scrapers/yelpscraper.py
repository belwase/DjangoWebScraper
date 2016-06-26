from yelpapi import YelpAPI
from pprint import pprint
import requests
from bs4 import BeautifulSoup
import MySQLdb
from datetime import datetime
from django.utils.dateformat import format

from main.models import *

class YelpScraper():

	def __init__(self,params):
		self.BASE_URL = 'https://www.yelp.com/'
		self.yelp = YelpAPI('pvImIXD6_9XDcw5TEBWdEw','fBbKhobgly9fsjqnlsTNA5SyQI4','Nj9xR2XNdp0yQzf6eJysd9AJkj-FFW4M','u5YhqlY6ptEoleexrhQZmqM5vg8')
		self.crawl_id = 0
		self.crawler_record = None
		self.site = None
		self.session = requests.Session()
		self.params = params
		self.keyword = params['term']+ ' '+params['location']
		self.count = 0


	def getWebsite(self,url):
		#print 'Getting ' + url
		response = self.session.get(url)
		soup = BeautifulSoup(response.text)
		try:
			web = soup.find('div',{'class':'biz-website'}).find('a').text
			return web
		except:
			return url	


	def getValue(self,key,dictonary):
		try:
			return dictonary[key]
		except:
			return ''

	def search(self):
		
		self.site = Site.objects.get(name='yelp')
		record = CrawlerRecord.objects.create(site=self.site,keyword=self.keyword,start_time=format(datetime.now(), u'U'),status='PENDING',updated_time=format(datetime.now(), u'U'))
		record.save()
		self.crawl_id = record.id
		self.crawler_record = CrawlerRecord.objects.get(id=record.id)
		status = 'FAILED'
		

		try:
			response = self.yelp.search_query(term='boats rental',location='new york',offset=900)
			total = response['total']
			print 'Total Biz ' + str(total)
			pages = total/20
			for page in range(0,pages+1):
				response = self.yelp.search_query(term=self.params['term'],location=self.params['location'],offset=page*20)#,limit=1)
				#print len(response['businesses'])
				for business in response['businesses']:
					website = self.getWebsite(business['url'])
					data = {'rating':self.getValue('rating',business),
						'name':self.getValue('name',business),
						'url':self.getValue('url',business),
						'phone':self.getValue('phone',business),
						'website':website,
						'category':self.getValue('categories',business),
						'location':self.getValue('coordinate',business['location']),
						'address':self.getValue('display_address',business['location'])
						}
						#data = {'rating':business['rating'], 'name':business['name'], 'url':business['url'], 'category':business['categories'],'phone':business['phone'],'website':website,'location':business['location']['coordinate'],'address':business['location']['display_address']}

					try:
						row,created = Yelp.objects.get_or_create(name=data['name'],url=data['url'],phone=data['phone'],website=data['website'],category=data['category'],rating=data['rating'],location=data['location'],address=data['address'])
						if created:
							row.save()
						self.count = self.count + 1
						mapping_row = CrawlerSiteMapping.objects.create(crawler_record = self.crawler_record, site = self.site, site_row_id = row.id)
						mapping_row.save()
					except Exception as ex:
						print ex
						continue

					#print data
					#break
				#break
			status = 'SUCCESS'
				#l = [(k,v) for k,v in response.items()]
				#pprint(response['businesses'])
				#response = self.yelp.business_query(id='the-loeb-boathouse-bike-and-boat-rental-new-york')

				


		except Exception as ex:
			print ex
			pass

		CrawlerRecord.objects.filter(id=record.id).update(status=status,records_downloaded=self.count,end_time=format(datetime.now(), u'U'),updated_time=format(datetime.now(), u'U'))



'''
params = {'term':'boats rental','location':'new york'}
yp = YelpScraper(params)
yp.search()
'''

