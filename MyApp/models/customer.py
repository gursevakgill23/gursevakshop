from django.db import models


class Customer(models.Model):
    fname = models.CharField(max_length=50,  default="")
    lname = models.CharField(max_length=50,  default="")
    phone = models.CharField(max_length=15,  default="")
    email = models.EmailField()
    password = models.CharField(max_length=500, default="")

    def __str__(self):
        return self.fname

    def isExists(self):
        if Customer.objects.filter(email=self.email):
            return True
        return False

    @staticmethod
    def get_customer_by_email(email):
        try:
            return Customer.objects.get(email=email)
        except:
            return False

