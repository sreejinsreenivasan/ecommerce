from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class UserModel(AbstractUser):

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'password']


    created_at = models.DateTimeField(auto_now_add=True)
    refferal = models.ForeignKey("app.Refferal", on_delete=models.CASCADE,null=True,blank=True,)
    wallet = models.FloatField(default=0.00)

class Refferal(models.Model):
    code = models.CharField(max_length=50, unique=True)
    user = models.ForeignKey("app.UserModel", on_delete=models.CASCADE,related_name="reffered_by")
    is_expired = models.BooleanField(default=False)


class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.FloatField(default=0.00)
    created_by = models.ForeignKey("app.UserModel", on_delete=models.CASCADE)



class ProductLink(models.Model):
    generated_link = models.TextField(max_length=200)
    created_by = models.ForeignKey("app.UserModel", on_delete=models.CASCADE)
    product = models.ForeignKey("app.Product",on_delete=models.CASCADE)
