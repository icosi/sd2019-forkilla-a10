 
from django.conf.urls import url

from . import views
from django.contrib.auth.views import login, logout
from django.conf.urls import url, include
from rest_framework import routers
from forkilla import views




listOfAddresses = ["sd2019-forkilla-a10.herokuapp.com/"]
#listOfAddresses = ["127.0.0.1:8000/"]

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^restaurants/$', views.restaurants, name='restaurants'),
    url(r'^restaurants/(?P<city>.*)/$', views.restaurants, name='restaurants'),
    url(r'^restaurant/(?P<restaurant_number>.*)/$', views.details, name='details'),
    url(r'^restaurants/(?P<city>.*)/(?P<category>.*)/$', views.restaurants, name='restaurants'),

    url(r'^restaurants/(?P<category>.*)/$', views.restaurants, name='restaurants'),
    url(r'^restaurants/(\d+)/$', views.restaurants, name='restaurant'),
    url(r'^reservation/$', views.reservation, name='reservation'),
    url(r'^checkout/$', views.checkout, name='checkout'),
    url(r'^review/$', views.leftReview, name='leftReview'),
    url(r'^register/$', views.register, name='register'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^comparator$', views.comparator, {'ips': listOfAddresses},name='comparator'),

    url(r'^delReservation/(?P<reservation_id>.*)/$', views.delReservation,name='delReservation'),
    url(r'^delReview/(?P<review_id>.*)/$', views.delReview,name='delReview')

]

