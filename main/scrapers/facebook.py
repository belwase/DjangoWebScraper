import requests
import csv
import json
import time
from itertools import islice
from main.models import *
from datetime import datetime
from django.utils.dateformat import format

class Facebook():
	def __init__(self,token,keyword):
		self.crawl_id = 0
		self.crawler_record = None
		self.site = None
		self.requests = requests.Session()
		self.token = token
		self.keyword = keyword
		self.count = 0

	def writeToDB(self,jsonResponse,keyword):
		location = ""
		emails = ""
		try:
			name = jsonResponse['name']
		except:
			name = ""
		try:
			locJson = jsonResponse['location']
			try:
				for item in locJson:
					try:
						location = location + str(locJson[item]) + " ,  "
					except:
						pass
		
			except Exception as ex:
				print 'ex' + ex.message
		except:
			pass
			
		try:
			city = jsonResponse['location']['city']
		except:
			city = ''
			
		try:
			country = jsonResponse['location']['country']
		except:
			country = ''	

		try:
			emailList = jsonResponse['emails']
			emails = ''.join(emailList)	
		except:
			pass

		try:
			pid = jsonResponse['id']
		except:
			pid = ""
		
		try:
			link = jsonResponse['link']
		except:
			link = ""


		try:
			category = jsonResponse['category']
		except:
			category = ""
		

		try:
			phone = jsonResponse['phone']
		except:
			phone = ""


		try:
			website = jsonResponse['website']
		except:
			website = ""
		try:
			likes = jsonResponse['likes']
		except:
			likes = ""
		data = {
		'pid':str(pid),
		'name':str(name),
		'link':str(link),
		'phone':str(phone),
		'website':str(website),
		'category':str(category),
		'likes':str(likes),
		'email':str(emails),
		'city':str(city),
		'country':str(country),
		'location':str(location),
		'keyword':keyword
		}
		print data	
		try:
			row,created = FacebookPage.objects.get_or_create(pid=data['pid'],name=data['name'],link=data['link'],phone=data['phone'],website=data['website'],category=data['category'],likes=data['likes'],email=data['email'],city=data['city'],location=data['location'],country=data['country'],keyword=data['keyword'])
			if created:
				row.save()
			self.count = self.count + 1
			mapping_row = CrawlerSiteMapping.objects.create(crawler_record = self.crawler_record, site = self.site, site_row_id = row.id)
			mapping_row.save()
		except Exception as ex:
			print ex

	def getPageDetail(self,pageId,keyword):

		try:
			url = 'https://graph.facebook.com/%s?fields=phone,website,location,current_location,emails,contact_address,company_overview,category,link,likes,hometown,general_info,display_subtext&access_token=%s'%(pageId,self.token)

			response = requests.get(url)
			if response.status_code == 200:
				jsonResponse = json.loads(response.text)
				self.writeToDB(jsonResponse,keyword)
			else:
				pageId = pageId.split('-')
				url = 'https://graph.facebook.com/%s?fields=phone,website,location,current_location,emails,contact_address,company_overview,category,link,likes,hometown,general_info,display_subtext&access_token=%s'%(pageId[-1],self.token)
				response = requests.get(url)
				jsonResponse = json.loads(response.text)
				self.writeToDB(jsonResponse,keyword)
		except Exception as ex:
			print ex

	def getSearchResult(self):
		self.site = Site.objects.get(name='facebook')
		record = CrawlerRecord.objects.create(site=self.site,keyword=self.keyword,start_time=format(datetime.now(), u'U'),status='PENDING',updated_time=format(datetime.now(), u'U'))
		record.save()
		self.crawl_id = record.id
		self.crawler_record = CrawlerRecord.objects.get(id=record.id)
		record.save()
		status = 'SUCCESS'
		try:
			keyword = self.keyword
			print keyword
			url = 'https://graph.facebook.com/search?q=%s&type=place&access_token=%s'%(keyword,self.token)
			response = requests.get(url)
			jsonResponse = json.loads(response.text)
			for x in jsonResponse['data']:
				try:
					self.getPageDetail(x['id'],keyword)
					time.sleep(3)
				except Exception as ex:
					print ex
					continue

		except Exception as ex:
			return 'Token Expired'
			status = 'FAILED'
		CrawlerRecord.objects.filter(id=record.id).update(status=status,records_downloaded=self.count,end_time=format(datetime.now(), u'U'),updated_time=format(datetime.now(), u'U'))
		return True		
