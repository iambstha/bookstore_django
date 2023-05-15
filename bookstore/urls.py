
from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView
from django.contrib.auth import views as auth_views

from store.views import index, shop, addCategory, addItem, signup, signin, add, logout_view, logout, mycart

urlpatterns = [
    path('',index, name='index'),
    path('addcategory/', addCategory, name='addCategory'),
    path('additem/', addItem, name='addItem'),
    path('shop/', shop, name='shop'),
    path('mycart/', mycart, name='mycart'),
    path('signup/', signup, name='signup'),
    path('signin/', signin, name='signin'),
    path('logout_view/', logout_view, name='logout_view'),
    path('logout/', logout, name='logout'),
    path('add/', add, name='add'),
    path('admin/', admin.site.urls),
    # path('login/', LoginView.as_view(template_name='app/signin.html'), name='login'),
    # path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    # path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
]
