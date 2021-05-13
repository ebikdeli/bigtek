from django.contrib import admin
from sales.models import Cart


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    pass
