from rest_framework import serializers
from vendorManagementApp.models import*

class PostVendorSerializer(serializers.ModelSerializer):
    name=serializers.CharField()
    class Meta:
        model=Vendor
        fields=['name', 'contact_details','address', 'vendor_code', 'on_time_delivery_rate',
                'quality_rating_avg','average_response_time','fulfillment_rate',]

    def validate_name(self,data):
        if Vendor.objects.filter(name=data).exists():
            raise serializers.ValidationError(" vendor name already exist")
        return data
    
            
    
class GetVendorSerializer(serializers.ModelSerializer):
    class Meta:
        model=Vendor
        fields=['id','name', 'contact_details','address', 'vendor_code', 'on_time_delivery_rate',
                'quality_rating_avg','average_response_time','fulfillment_rate',]
        
class UpdateVendorSerializer(serializers.ModelSerializer):
    name=serializers.CharField()
    class Meta:
        model=Vendor
        fields=['name', 'contact_details','address', 'vendor_code', 'on_time_delivery_rate',
                'quality_rating_avg','average_response_time','fulfillment_rate',]
        
    def validate_name(self,data):
        vendor_id=self.context.get('vendor_id')
        if Vendor.objects.filter(name=data).exclude(id=vendor_id).exists():
            raise serializers.ValidationError(" vendor name already exist")
        return data
    
#-----------purchase order----------------

class PostPurchaseOrderSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=PurchaseOrder
        fields=['po_number', 'vendor','order_date', 'delivery_date', 'items',
                'quantity','status','quality_rating','issue_date','acknowledgment_date']
class GetPurchaseOrderSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=PurchaseOrder
        fields=['id','po_number', 'vendor','order_date', 'delivery_date', 'items',
                'quantity','status','quality_rating','issue_date','acknowledgment_date']
        
class UpdatePurchaseOrderSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=PurchaseOrder
        fields=['po_number', 'vendor','order_date', 'delivery_date', 'items',
                'quantity','status','quality_rating','issue_date','acknowledgment_date']


#---------Historical performance-------------
class HistoricalPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricalPerformance
        fields = '__all__'