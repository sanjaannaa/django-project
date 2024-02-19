from django.contrib import admin
from product import models

# Register your models here.
class Product_Admin(admin.ModelAdmin):
    list_display = ['id','name','price','details','category','is_active','rating','image']

admin.site.register(models.Product_Table,Product_Admin)
admin.site.register(models.Cart_Table)
admin.site.register(models.OrderTable)
admin.site.register(models.CustomerDetails)
