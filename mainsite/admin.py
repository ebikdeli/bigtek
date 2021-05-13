from django.contrib import admin
from mainsite.models import Customers


@admin.register(Customers)
class CustomersAdmin(admin.ModelAdmin):
    pass
