from django import forms

from .models import Categories, Item, RegUser

class SignupForm(forms.ModelForm):
    class Meta:
        model = RegUser
        fields = ['username','password']

class SignInForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = RegUser
        exclude = ['last_login']

class CategoriesForm(forms.ModelForm):
    class Meta:
        model = Categories
        fields = ['name','created_by']


class ItemsForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['category','name','author','cost_price','sell_price','created_by']