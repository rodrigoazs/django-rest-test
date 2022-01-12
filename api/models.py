from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Account(models.Model):
    date_created = models.DateField(auto_created=True)
    is_active = models.BooleanField(default=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str___(self):
        return self.name
