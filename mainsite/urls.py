from mainsite import views
from django.urls import path

app_name = 'mainsite'

urlpatterns = [
    path('', views.index, name='index'),
    path('register_order/', views.register_order, name='register_order'),
    path('change_order/', views.change_order, name='change_order'),
    # path('has_registered/', views.has_registered, name='has_registered')
]
