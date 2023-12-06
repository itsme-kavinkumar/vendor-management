from django.db import models

from django.utils import timezone

class Vendor(models.Model):
    name = models.CharField(max_length=255)
    contact_details = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    vendor_code = models.CharField(max_length=50, unique=True)
    on_time_delivery_rate = models.FloatField(default=0)
    quality_rating_avg = models.FloatField(default=0)
    average_response_time = models.FloatField(default=0)
    fulfillment_rate = models.FloatField(default=0)
    def __str__(self):
        return self.name
        
    

class PurchaseOrder(models.Model):
    status = (
        ('pending', 'pending'),
        ('canceled', 'canceled'),
        ('completed', 'completed'),
    )
    po_number = models.CharField(max_length=50, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.RESTRICT)
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateTimeField(blank=True, null=True)
    items = models.JSONField(blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=50,choices=status, default='pending')
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField(blank=True, null=True)
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.RESTRICT,blank=True, null=True)
    date = models.DateTimeField(default=timezone.now,blank=True, null=True)
    on_time_delivery_rate = models.FloatField(blank=True, null=True)
    quality_rating_avg = models.FloatField(blank=True, null=True)
    average_response_time = models.FloatField(blank=True, null=True)
    fulfillment_rate = models.FloatField(blank=True, null=True)
