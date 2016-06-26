from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Site(models.Model):
    name = models.CharField(max_length=30)
    url = models.TextField()
    scraper = models.CharField(max_length=30)

    def __unicode__(self):
        return self.name

class CrawlerRecord(models.Model):
	site = models.ForeignKey(Site)
	task_id = models.CharField(max_length=125,null=True,blank=True)
	keyword = models.CharField(max_length=225,null=True,blank=True)
	records_downloaded = models.CharField(max_length=25,null=True,blank=True)
	records_merged = models.CharField(max_length=25,null=True,blank=True)
	records_new = models.CharField(max_length=25,null=True,blank=True)
	bytes_downloaded = models.CharField(max_length=25,null=True,blank=True)
	start_time = models.CharField(max_length=25,null=True,blank=True)
	end_time = models.CharField(max_length=25,null=True,blank=True)
	updated_time = models.CharField(max_length=25,null=True,blank=True)
	status = models.CharField(max_length=25,null=True,blank=True)
	mailed = models.NullBooleanField(max_length=25)

class CrawlerSiteMapping(models.Model):
	crawler_record = models.ForeignKey(CrawlerRecord)
	site = models.ForeignKey(Site)
	site_row_id = models.IntegerField()


class Country(models.Model):
	name = models.CharField(max_length=25)
	abbr = models.CharField(max_length=5)
	def __unicode__(self):
		return self.name


class State(models.Model):
	name = models.CharField(max_length=25)
	abbr = models.CharField(max_length=5)
	country = models.ForeignKey(Country)
	def __unicode__(self):
		return self.name


class TripAdvisorLocation(models.Model):
	name = models.CharField(max_length=250,unique=True)
	url = models.TextField()
	def __unicode__(self):
		return self.name

class TripAdvisorCat(models.Model):
	name = models.CharField(max_length=255,unique=True)
	cat = models.CharField(max_length=250)
	def __unicode__(self):
		return self.name

class TripAdvisorAttraction(models.Model):
	name = models.CharField(max_length=255,unique=True)
	address = models.CharField(max_length=255)
	location = models.ForeignKey(TripAdvisorLocation,null=True)
	phone = models.CharField(max_length=255)
	website = models.TextField()
	email = models.CharField(max_length=255)
	description = models.TextField()
	url = models.TextField()
	keywords = models.CharField(max_length=255)
	category = models.ForeignKey(TripAdvisorCat)
	country = models.CharField(max_length=250)
	def __unicode__(self):
		return self.name

class FacebookPage(models.Model):
	pid = models.CharField(max_length=50,unique=True)
	name = models.CharField(max_length=255)
	link = models.TextField()
	phone = models.CharField(max_length=255)
	website = models.TextField()
	category = models.TextField()
	likes = models.CharField(max_length=5)
	email = models.CharField(max_length=255)
	city = models.CharField(max_length=255)
	location = models.CharField(max_length=255)
	country = models.CharField(max_length=255)
	keyword = models.CharField(max_length=255)
	
	def __unicode__(self):
		return self.name

class Yelp(models.Model):
	name = models.CharField(max_length=255)
	phone = models.CharField(max_length=25)
	website = models.CharField(max_length=255)
	url = models.TextField(max_length=255)
	location = models.TextField(max_length=255)
	address = models.TextField(max_length=255)
	category = models.CharField(max_length=255)
	rating = models.CharField(max_length=25)

	def __unicode__(self):
		return self.name
