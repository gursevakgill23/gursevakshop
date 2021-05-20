from django.db import models
from .product import Product
from .customer import Customer

import datetime
class Order(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)
    address=models.CharField(max_length=80,default="",blank=True)
    phone=models.IntegerField(default="",blank=True)
    price=models.IntegerField()
    date=models.DateField(default=datetime.datetime.today)
    status=models.BooleanField(default=False)


    def __str__(self):
        return self.product.name

    

    @staticmethod
    def get_orders_by_customer(customer_id):
           return Order.objects.filter(customer=customer_id)
        
     
