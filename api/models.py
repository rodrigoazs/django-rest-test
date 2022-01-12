from django.db import models


# Create your models here.
class Account(models.Model):
    name = models.CharField(max_length=100)
    date_created = models.DateField(auto_created=True)
    is_active = models.BooleanField(default=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def __str___(self):
        return self.name
