from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from knox.auth import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from vendorManagementApp.serializers import*
from vendorManagementApp.models import Vendor
from django.db.models import RestrictedError
import traceback
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import timedelta

class VendorApi(APIView):
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [TokenAuthentication]

    def post(self, request):
        """
        Function for  create a new vendor
        """
        try:
            serializer = PostVendorSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'status': "success", 'message': "vendor created successfully"}, status=status.HTTP_201_CREATED)
            return Response({'status': "failed", 'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'status':'failed','message':'something went wrong'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def get(self,request):
        """
       Function for  get All vendor details 
        """
        try:

            queryset = Vendor.objects.all()
            serializer = GetVendorSerializer(queryset, many=True)
            return Response({'status': "success", 'message': "", 'data': serializer.data}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'status':'failed','message':'something went wrong'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def delete(self,request,vendor_id):
       
        try:

            Vendor.objects.get(id=vendor_id).delete()
            
            return Response({'status': 'success', 'message': "vendor deleted successfully"}, status=status.HTTP_200_OK)
        except Vendor.DoesNotExist:
            return Response({'status': 'failed', 'message': "vendor not found"}, status=status.HTTP_404_NOT_FOUND)
        except RestrictedError:
            return Response({'status': 'failed', 'message': "vendor is referenced with another instance"}, status=status.HTTP_400_BAD_REQUEST)

class UpdateVendorApi(APIView):
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [TokenAuthentication]

    def get(self,request,vendor_id):
        """
        Function for  Retrieve a specific vendor's details.
        """
        try:
        
            queryset=Vendor.objects.get(id=vendor_id)
            serializer = GetVendorSerializer(queryset)
            return Response({'status': "success", 'message': "", 'data': serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status':'failed','message':'something went wrong'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def put(self,request):
        """
        Function for Update a vendor's details.
        """
        try:
            vendor_id = request.query_params.get('vendor_id')
            queryset=Vendor.objects.get(id=vendor_id)
            serializer=UpdateVendorSerializer(instance=queryset,data=request.data,context={'vendor_id':vendor_id})
            if serializer.is_valid():
                serializer.save()
                return Response({'status': "success", 'message': "vendor details updated successfully"}, status=status.HTTP_201_CREATED)
            return Response({'status': "failed", 'message':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'status':'failed','message':'something went wrong'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#-----------------------------Purchase Order---------------------


class PurchaseOrderApi(APIView):
#     permission_classes = [IsAuthenticated]
#     authentication_classes = [TokenAuthentication]

    def post(self, request):
        """
        Function for create new purchase order
        """
        try:
            serializer = PostPurchaseOrderSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'status': "success", 'message': "purchase order created successfully"}, status=status.HTTP_201_CREATED)
            return Response({'status': "failed", 'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({'status': 'failed', 'message': 'something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def get(self,request):
        """
        Function for get all purchase order details
        """
        try:

            vendor_id = request.query_params.get('vendor_id')
            queryset=PurchaseOrder.objects.all()
            if vendor_id:
                queryset=queryset.filter(vendor=vendor_id)
            serializer = GetPurchaseOrderSerializer(queryset, many=True)
            return Response({'status': "success", 'message': "", 'data': serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status':'failed','message':'something went wrong'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def delete(self,request):
        """
        Function for delete specific purchase order
        """
        po_id = request.query_params.get('po_id')
        try:
            vendor = PurchaseOrder.objects.get(id=po_id)
            vendor.delete()
            return Response({'status': 'success', 'message': "Purchase order deleted successfully"}, status=status.HTTP_200_OK)
        except Vendor.DoesNotExist:
            return Response({'status': 'failed', 'message': "Purchase order not found"}, status=status.HTTP_404_NOT_FOUND)
        except RestrictedError:
            return Response({'status': 'failed', 'message': "Purchase order is referenced with another field"}, status=status.HTTP_400_BAD_REQUEST)

class UpdatePurchaseOrderApi(APIView):
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [TokenAuthentication]

    def get(self,request,po_id):
        """
        Function for Retrieve details of a specific purchase order
        """

        try:

            queryset=PurchaseOrder.objects.get(id=po_id)
            serializer = GetPurchaseOrderSerializer(queryset)
            return Response({'status': "success", 'message': "", 'data': serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status':'failed','message':'something went wrong'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def put(self,request):
        """
        Function for  update the purchase order details
        """
        try:

            po_id = request.query_params.get('po_id')
            queryset=PurchaseOrder.objects.get(id=po_id)
            serializer=UpdatePurchaseOrderSerializer(queryset,data=request.data,context={'po_id':po_id})
            if serializer.is_valid():
                serializer.save()
                return Response({'status': "success", 'message': "purchase details updated successfully"}, status=status.HTTP_201_CREATED)
            return Response({'status': "failed", 'message':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({'status':'failed','message':'something went wrong'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AcknowledgePurchaseOrderView(APIView):

    # permission_classes = [IsAuthenticated]
    # authentication_classes = [TokenAuthentication]
    """
    Function for update the purchase order Acknowledge time 
    """

    def post(self, request, po_id):
        try:
            purchase_order = PurchaseOrder.objects.get(pk=po_id)

            # Acknowledge the purchase order
            purchase_order.acknowledgment_date = timezone.now()
            purchase_order.save()

            return Response({'message': 'Purchase order acknowledged successfully.'})
        except Exception as e:
            return Response({'status':'failed','message':'something went wrong'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)





class VendorPerformanceView(APIView):
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [TokenAuthentication]
    """
        Function for calculate vendor perfomace and Retrieve vendor perfomance details
    """
    def get(self, request, vendor_id):
        try:

            vendor = Vendor.objects.get(pk=vendor_id)

            # Calculate performance metrics
            completed_pos = PurchaseOrder.objects.filter(vendor=vendor, status='completed')
            total_pos = PurchaseOrder.objects.filter(vendor=vendor)

            on_time_delivery_rate = (completed_pos.filter(delivery_date__lte=models.F('acknowledgment_date')).count()
                                    / completed_pos.count()) * 100 if completed_pos.count() > 0 else 0

            quality_rating_avg = completed_pos.exclude(quality_rating__isnull=True).aggregate(avg_rating=models.Avg('quality_rating'))['avg_rating'] or 0

            avg_response_time = completed_pos.exclude(acknowledgment_date__isnull=True).aggregate(avg_response=models.Avg(models.F('acknowledgment_date') - models.F('issue_date')))['avg_response'] or 0

            avg_response_time = avg_response_time.total_seconds()/60
            
            fulfillment_rate = (completed_pos.filter(status='completed', quality_rating__isnull=True).count()
                                / total_pos.count()) * 100 if total_pos.count() > 0 else 0

            # Update or create historical performance record
            HistoricalPerformance.objects.update_or_create(
                vendor=vendor,
                defaults={
                    'on_time_delivery_rate': on_time_delivery_rate,
                    'quality_rating_avg': round(quality_rating_avg,2),
                    'average_response_time': avg_response_time,
                    'fulfillment_rate': fulfillment_rate,
                }
            )

            # Retrieve and return performance metrics
            performance = HistoricalPerformance.objects.filter(vendor=vendor).latest('date')
            serializer = HistoricalPerformanceSerializer(performance)
            
            return Response({'status':'success','message':'','data':serializer.data},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status':'failed','message':'something went wrong'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)




