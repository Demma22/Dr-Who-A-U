from django.urls import path
from invo import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('index/',views.index, name='index'),
    path('home/',views.index, name='home'),
    path('',auth_views.LoginView.as_view(template_name = 'products/login.html'), name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name = 'products/logout.html'), name='logout'),
     # this route is for BUY ITEM button
    path('index/<int:product_id>', views.product_detail, name = 'product_detail'),
    path('issue_item/<str:pk>/', views.issue_item, name = 'issue_item'),
    path('add_to_stock/<str:pk>/', views.add_to_stock, name = 'add_to_stock'),
    #tis handles the receipt after saccessful sale
    path('receipts/', views.receipt, name = 'receipt'),
    #handling a request from the web browser for all sales
    path('all_sales/', views.all_sales, name = 'all_sales'),
    path('receipt/<int:receipt_id>', views.receipt_detail, name = 'receipt_detail' ),
    path('delete/<int:product_id>', views.delete_detail, name = 'delete_detail' )
]