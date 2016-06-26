from django.contrib import admin
from django.contrib.admin import AdminSite
from adminplus.sites import AdminSitePlus
from django.utils.translation import ugettext_lazy

from main.models import *

# Register your models here.
class MyAdminSite(AdminSitePlus):
    # Text at the end of each page's <title>.
    site_title = ugettext_lazy('PrSpur Scraper Management')

    # Text in each page's <h1>.
    site_header = ugettext_lazy('PCS : PrSpur Scraper Management')

    # Text at the top of the admin index page.
    index_title = ugettext_lazy('Hello')

admin_site = MyAdminSite()

class SiteAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'scraper')

admin_site.register(Site, SiteAdmin)