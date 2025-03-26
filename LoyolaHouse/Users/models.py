from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class roles(models.Model):
    role_id = models.AutoField(primary_key=True)
    role_desc = models.CharField(max_length=200)

    def __str__(self):
        return self.role_desc

class UserRole(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role_id = models.IntegerField()