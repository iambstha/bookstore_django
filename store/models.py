from django.db import models

from django.contrib.auth.models import User, AbstractBaseUser
from django.contrib.auth.hashers import make_password,check_password


class Categories(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name
    
class Item(models.Model):
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    cost_price = models.IntegerField()
    sell_price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

    class Meta:
        verbose_name_plural = 'Items'

    def __str__(self):
        return self.name

class RegUser(models.Model):
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    
    last_login = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'username'

    def set_password(self, password):
        self.password = make_password(password)

    def check_password(self, password):
        return check_password(password, self.password)
    
    class Meta:
        verbose_name_plural = 'Signed Up Users'

    def __str__(self):
        return self.username
    

class Cart(models.Model):
    user = models.ForeignKey(RegUser, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    # def __str__(self):
    #     return f'{self.user.username} - {self.item.name} ({self.quantity})'
    
