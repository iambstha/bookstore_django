from django.contrib import admin
from .models import Categories, Item, RegUser, Cart

admin.site.register(Categories)
admin.site.register(Item)
admin.site.register(RegUser)

class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'item', 'quantity')

admin.site.register(Cart, CartAdmin)
