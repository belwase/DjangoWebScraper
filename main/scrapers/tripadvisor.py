# -*- coding: utf-8 -*-
# -- coding: utf-8 --

from pyvirtualdisplay import Display
from itertools import islice
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from bs4 import BeautifulSoup
from random import random
import requests
import grequests

import json
import re
import os
import time
import csv
from datetime import datetime
import codecs
import MySQLdb

from main.models import *
from datetime import datetime
from django.utils.dateformat import format


class Tripadvisor():

	def __init__(self,cat_id,loc_url):
		self.crawl_id = 0
		self.crawler_record = None
		self.site = None
		self.LOC_URL = loc_url
		self.LOC_OBJ = None
		self.CAT_ID = cat_id
		self.CAT_OBJ = None		
		self.keyword = self.getKeyword()
		self.count = 0		

		self.BASE_URL = 'http://www.tripadvisor.com'
		#self.LOC_URL = 'http://www.tripadvisor.com/Attractions-g2-Activities-oa{}-Asia.html#LOCATION_LIST'
		#self.LOC_URL = 'http://www.tripadvisor.com/Attractions-g147400-Activities-c55-oa{}-U_S_Virgin_Islands.html#LOCATION_LIST'
		#self.Ajax_Url = 'http://www.tripadvisor.com/AttractionsAjax-{}.html'

		#self.KEYWORD = 'boat'
		#self.CAT_ID = 'c36-t132'
		self.OUTPUT = "wines-south-america.csv"
		self.CITY = "city-south-america.csv"
		self.WEBSITE_ENCODED = ""


		
		#self.CAT = {'boat_tours':'c55-t167','kayaking_canoeing':'c55-t191','dolphins':'c55-t198'}

		self.session = requests.Session()
		self.user_agent = {'User-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/33.0.1750.152 Chrome/33.0.1750.152 Safari/537.36'}
		self.writer = None
		

		#display = Display(visible=0, size=(1024, 768))
		#display.start()

		'''
		dcap = dict(DesiredCapabilities.PHANTOMJS)
		dcap["phantomjs.page.settings.userAgent"] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.91 Safari/537.36'
		dcap["phantomjs.page.settings.resourceTimeout"] = '9000'
		self.driver = webdriver.PhantomJS(desired_capabilities=dcap,service_args=['--ignore-ssl-errors=true'])
		self.driver.set_page_load_timeout(15)
		self.driver.set_script_timeout(10)
		'''
		
		#self.conn = MySQLdb.connect("localhost","root","12345","prspur")
		#self.cursor = self.conn.cursor()


	def getKeyword(self):
		cat = TripAdvisorCat.objects.get(cat=self.CAT_ID)
		loc = TripAdvisorLocation.objects.get(url=self.LOC_URL)
		self.LOC_OBJ = loc
		self.CAT_OBJ = cat
		return cat.name + ' ' + loc.name

	def __del__(self):
		pass
		#self.driver.quit()
		#self.display.stop()
		#self.conn.close()

	def writeToDB(self,data):
		try:
			try:
				row,created = TripAdvisorAttraction.objects.get_or_create(name=data['name'],address=data['address'],location=self.LOC_OBJ,phone=data['phone'],website=data['website'],email=data['email'],description=data['description'],url=data['url'],keywords=self.keyword,category=self.CAT_OBJ,country=data['country'])
				#print created
				if created:
					row.save()
			except:
				pass
			self.count = self.count + 1
			mapping_row = CrawlerSiteMapping.objects.create(crawler_record = self.crawler_record, site = self.site, site_row_id = row.id)
			mapping_row.save()
		except Exception as ex:
			print ex


	def get_business_info(self,biz_url):
		#print biz_url,attraction,state
		try:
			response = self.session.get(biz_url,headers=self.user_agent)
		except:
			return
		soup = BeautifulSoup(response.text)
		business_links = soup.findAll('div',{'class':'property_title'})

		'''
		biz_link_list = []
		for biz in business_links:
			biz_deep_url = self.BASE_URL + biz.find('a')['href']
			biz_link_list.append(biz_deep_url)		

		rs = [grequests.get(u) for u in biz_link_list]

		return
		'''

		for biz in business_links:
			print biz.find('a')['href']
			biz_deep_url = self.BASE_URL + biz.find('a')['href']
			response = self.session.get(biz_deep_url , headers = self.user_agent)
			soup = BeautifulSoup(response.text)

			try:
				business_name = soup.find('h1',{'class':'heading_name'}).text
				business_name = re.sub('\s+',' ',business_name)
				#print business_name
			except:
				business_name = ''
			try:
				address = soup.find('span',{'class':'format_address'}).text.split('Address:')[1]
				#print address
			except:
				address = ''
			try:
				phone = soup.find('div',{'class':'phoneNumber'}).text.split('Phone Number:')[1]
				#print phone
			except:
				phone = ''

			try:
				description = soup.findAll('div',{'class':'details_wrapper'})[-1].text.split('Description:')[1]
				description = re.sub('\s+',' ',description)
				#print description
			except:
				description = ''

			try:
				regex = re.compile(("([a-z0-9!#$%&'*+\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\/=?^_`"
                    "{|}~-]+)*(@|\sat\s)(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?(\.|"
                    "\sdot\s))+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)"))
				email_div = soup.findAll('div',{'class':'taLnk fl'})
				#print email_div
				#print email_div[1].attrs['onclick']
				for email_d in email_div:
					if 'Email' in email_d.attrs['onclick']:
						email_div = email_d
				#print email_div[-1]
				#print email_div
				email = re.findall(regex,str(email_div))
				email = email[0][0]
				#print email
			except Exception as e:
				email = ''
				#print e.message

			try:
			
				website_div = soup.find('span',text='Website')
				#print website_div
				web_code = website_div.attrs['onclick'].split("aHref':'")#[1].split("'")[0]
				web_code =  web_code[1].split("'")[0]
				#print web_code
				website = web_code
			
				#response = self.session.get('http://localhost/test.html?x='+website)
				#print response.text
				#soup = BeautifulSoup(response.text)
				#website = soup.find('input',{'name':'box'}).attrs['value']	
				'''	
				self.driver.get('http://localhost/test.html?x='+web_code)
				element =  self.driver.find_element_by_xpath(".//*[@id='box']")
				website = element.get_attribute("value")
				self.driver.get(self.BASE_URL+website)
				#time.sleep(2)
				website = self.driver.current_url
				
				print website
				#self.driver.close()
				#driver.quit()
				'''
			except:
				website = ''

			try:
				country = soup.find('input',{'id':'GEO_SCOPED_SEARCH_INPUT'}).attrs['value']
				#print country
			except:
				country = ''
			
			try:
				keywords = soup.find('div',{'class':'detail'}).text
			except:
				keywords = ''

			data = {'name': business_name, 'address': address, 'email': email,'website':website, 'phone': phone,'description':description, 'url': biz_deep_url,'country':country,'keywords':keywords}
			print data
			self.writeToDB(data)
			#self.save_to_csv(data)
		

	def get_business(self):
			url = self.BASE_URL + self.LOC_URL
			#http://www.tripadvisor.com/Attractions-g294226-Activities-c55-oa00-Bali.html#ATTRACTION_LIST
			url = url.replace("Activities-","Activities-"+self.CAT_ID+"-oa{}-")
			print url
			response = self.session.get(url,headers=self.user_agent)
			soup = BeautifulSoup(response.text)
			#check for pagination
			try:
				'''
				#Check heading if our keyword is there
				try:
					heading = soup.find('h1',{'class':'heading_name'}).text
					if self.KEYWORD not in heading.lower():
						continue
				except:
					continue
				'''
				pagination = soup.find('div',{'class':'pagination'}).findAll('a',{'class':'pageNum'})
				#print pagination ### I WAS HERE ------
				pages =  pagination[-1].text
				print 'Total Pages : ' + pages
				for page in range(0,(int(pages)*30)+30,30):
					#back_part = url.split('-',1)[1]
					#back_part = back_part.replace(self.CAT_ID,self.CAT_ID+"-oa"+str(page))
					#"g294226-Activities-c55-oa00-Bali"
					#biz_url = self.Ajax_Url.replace("{}",back_part)
					biz_url = url.replace('{}',str(page))
					#print biz_url
					self.get_business_info(biz_url)
					#break
					#Now get all items
					
			except Exception as e:
				print 'no pagination',e.message
				#print 'moving to ',url
				self.get_business_info(url)
				#print 'moved'
			#break

	def main(self):
		self.site = Site.objects.get(name='tripadvisor')
		try:
			#print self.keyword
			record = CrawlerRecord.objects.create(site=self.site,keyword=self.keyword,start_time=format(datetime.now(), u'U'),status='PENDING',updated_time=format(datetime.now(), u'U'))
			record.save()
			self.crawl_id = record.id
			self.crawler_record = CrawlerRecord.objects.get(id=record.id)
		

			status = 'SUCCESS'
			try:
				self.get_business()
			except:
				status = 'FAILED'

			CrawlerRecord.objects.filter(id=record.id).update(status=status,records_downloaded=self.count,end_time=format(datetime.now(), u'U'),updated_time=format(datetime.now(), u'U'))
			return True
		except Exception as ex:
			print ex
			return False


#ta = Tripadvisor()
#ta.get_location()
#ta.get_business()
#ta.get_website()
