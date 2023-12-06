from django.urls import path
from vendorManagementApp import views

urlpatterns=[
  path('POST/api/vendors/',views.VendorApi.as_view()),
  path('GET/api/vendors/',views.VendorApi.as_view()),
  path('GET/api/vendors/<int:vendor_id>/',views.UpdateVendorApi.as_view()),
  path('DELETE/api/vendors/<int:vendor_id>',views.VendorApi.as_view()),
  path('PUT/api/vendors/',views.UpdateVendorApi.as_view()),


  #-------purchase order---------------
  path('POST/api/purchase_order/',views.PurchaseOrderApi.as_view()),
  path('GET/api/purchase_order/',views.PurchaseOrderApi.as_view()),
  path('DELETE/api/purchase_order/',views.PurchaseOrderApi.as_view()),
  path('GET/api/purchase_order/<int:po_id>/',views.UpdatePurchaseOrderApi.as_view()),
  path('PUT/api/purchase_order/',views.UpdatePurchaseOrderApi.as_view()),

  #----------------------
  path('GET/api/vendors/<int:vendor_id>/performance/',views.VendorPerformanceView.as_view()),
  path('POST/api/purchase_orders/<int:po_id>/acknowledge/',views.AcknowledgePurchaseOrderView.as_view()),

]