from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
# Register your models here.
from .models import Sales

class SalesAdmin(ImportExportModelAdmin):
    list_display = ('id',  'order_id', 'order_date','ship_date','ship_mode','customer_id',
    'customer_name', 'segment','country','city','state','postal_code','region','product_id','category','subcategory','product_name','sales')

admin.site.register(Sales, SalesAdmin)