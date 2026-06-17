from django.contrib import admin
from .models import (
    Customer, 
    PaintProduct, PaintInvoice, PaintInvoiceItem,
    ElectricalProduct, ElectricalInvoice, ElectricalInvoiceItem
)
# Register your models here.
admin.site.register(Customer)
admin.site.register(PaintProduct)
admin.site.register(PaintInvoice)
admin.site.register(PaintInvoiceItem)
admin.site.register(ElectricalProduct)
admin.site.register(ElectricalInvoice)
admin.site.register(ElectricalInvoiceItem)