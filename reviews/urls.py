# Defines what views different urls point to
from django.urls import include, path, re_path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic.base import TemplateView
from django.contrib.auth.models import User
from reviews import views as core_views

urlpatterns = [
    path('', views.Home, name='home'),
    path('restaurants/', views.RestaurantList, name='restaurants'),
    path('search/', views.RestaurantSearch, name='restaurant-search'),
    path('account/', views.Account, name='account'),
    path('password_reset/', views.PassReset, name='password-reset'),
    path('restaurants/<int:restaurant_id>', views.RestaurantDetails, name='restaurant-detail'),
    path('about',views.About, name ='about'),
    path('cafes', views.Cafes, name='cafes'),
    path('campus', views.Campus, name='campus'),
    path('contact/', views.Contact, name='contact'),
]

urlpatterns += staticfiles_urlpatterns()

#Adds Django site authentication urls (for login, logout, password management)
urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
    # Account creation url
    re_path(r'^signup/$', core_views.Signup, name='signup'),
]