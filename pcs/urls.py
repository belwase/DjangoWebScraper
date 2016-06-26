"""pcs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from main.admin import admin_site

from main import views

urlpatterns = [
	url(r'^$', 'main.views.home'),
#	url(r'^', include(admin_site.urls)),
	url(r'^home/$', 'main.views.home'),
	#url(r'^results/$', 'main.views.results'),

    url(r'^results/$',views.results_list, name='results_list'),
    url(r'^edit/(?P<pk>\d+)$', views.results_edit, name='results_edit'),
    url(r'^delete/(?P<pk>\d+)$', views.results_delete, name='results_delete'),

	url(r'^process_form/$', 'main.views.process_form'),
	url(r'^auto_refresh/$', 'main.views.auto_refresh'),
	url(r'^download_result/$', 'main.views.download_result')
	#url(r'^admin/', include(admin_site.urls))
   #url(r'^admin/', include(admin.site.urls)),
]
