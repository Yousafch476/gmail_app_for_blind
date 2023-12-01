from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class app_password(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    password=models.CharField(max_length=100)

    def __str__(self):
        return self.password    

