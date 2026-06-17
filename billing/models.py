from django.db import models

# Create your models here.

class Customer(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=10,unique=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.phone_number}"

class PaintProduct(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.IntegerField(default=0)
    low_stock_threshold = models.IntegerField(default=10)
    hsn_code = models.CharField(max_length=20, default='0000')
    gst_rate = models.DecimalField(max_digits=5, decimal_places=2, default=18.00)

    def __str__(self):
        return self.name

class PaintInvoice(models.Model):
    invoice_number = models.CharField(max_length=50, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    date_created = models.DateTimeField(auto_now_add=True)
    sub_total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    final_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    def __str__(self):
        return self.invoice_number

class PaintInvoiceItem(models.Model):
    invoice = models.ForeignKey(PaintInvoice, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(PaintProduct, on_delete=models.PROTECT)
    quantity = models.IntegerField()
    price_at_sale = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity}x {self.product.name}"

class ElectricalProduct(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    stock_quantity = models.IntegerField(default=0)
    low_stock_threshold = models.IntegerField(default=5)

    def __str__(self):
        return self.name
    
class ElectricalInvoice(models.Model):
    invoice_number = models.CharField(max_length=50, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    date_created = models.DateTimeField(auto_now_add=True)
    sub_total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    final_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    def __str__(self):
        return self.invoice_number
    
class ElectricalInvoiceItem(models.Model):
    invoice = models.ForeignKey(ElectricalInvoice, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(ElectricalProduct, on_delete=models.PROTECT)
    quantity = models.IntegerField()
    price_at_sale = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity}x {self.product.name}"