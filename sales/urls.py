from django.urls import path
from sales import views

app_name = 'sales'

urlpatterns = [
    path('invoice/', views.invoice, name='invoice'),
    path('payment/', views.result_invoice, name='result_invoice'),
    path('invoice_pdf/', views.invoice_pdf, name='invoice_pdf'),
    path('update_invoice/', views.update_invoice, name='update_invoice'),
    path('tail_order/', views.tail_order, name='tail_order'),
]