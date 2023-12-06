from django.contrib import admin
from vendorManagementApp import models
# Register your models here.
admin.site.register(models.Vendor)
admin.site.register(models.PurchaseOrder)
admin.site.register(models.HistoricalPerformance)
