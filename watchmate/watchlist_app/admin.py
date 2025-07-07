from django.contrib import admin
from watchlist_app import models
# Register your models here.
admin.site.register(models.Watchlist)
admin.site.register(models.Platform)
admin.site.register(models.Review)