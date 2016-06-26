#from yelp.client import Client
#from yelp.oauth1_authenticator import Oauth1Authenticator
from yelpapi import YelpAPI
from pprint import pprint
import requests
from bs4 import BeautifulSoup

class Yelp():

	def __init__(self):
		self.BASE_URL = 'https://www.yelp.com/'
#		auth =  Oauth1Authenticator(consumer_key=YOUR_CONSUMER_KEY,consumer_secret=YOUR_CONSUMER_SECRET,token=YOUR_TOKEN,token_secret=YOUR_TOKEN_SECRET)
	
#		auth =  Oauth1Authenticator(consumer_key='pvImIXD6_9XDcw5TEBWdEw',consumer_secret='fBbKhobgly9fsjqnlsTNA5SyQI4',token='Nj9xR2XNdp0yQzf6eJysd9AJkj-FFW4M',token_secret='u5YhqlY6ptEoleexrhQZmqM5vg8')
#		client = Client(auth)
		self.yelp = YelpAPI('pvImIXD6_9XDcw5TEBWdEw','fBbKhobgly9fsjqnlsTNA5SyQI4','Nj9xR2XNdp0yQzf6eJysd9AJkj-FFW4M','u5YhqlY6ptEoleexrhQZmqM5vg8')


	def getWebsite(self,url):
		response = requests.get(url)
		soup = BeautifulSoup(response.text)
		try:
			web = soup.find('div',{'class':'biz-website'}).find('a').text
			return web
		except:
			return url	


	def search(self,params):
		#response = client.search('San Francisco', **params)
		#print response.businesses
		response = self.yelp.search_query(term=params['term'],location=params['location'],limit=1)
		print self.getWebsite(response['businesses'][0]['url'])
		#pprint(response['businesses'])
		#response = self.yelp.business_query(id='the-loeb-boathouse-bike-and-boat-rental-new-york')
#		pprint(response)


yp = Yelp()
params = {'term':'boats rental','location':'new york'}
yp.search(params)
