 
from django.conf.urls import url

from . import views
from django.contrib.auth.views import login, logout


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^restaurants/$', views.restaurants, name='restaurants'),
    url(r'^restaurants/(?P<city>.*)/$', views.restaurants, name='restaurants'),
    url(r'^restaurant/(?P<restaurant_number>.*)/$', views.details, name='details'),
    url(r'^restaurants/(?P<city>.*)/(?P<category>.*)$', views.restaurants, name='restaurants'),
    url(r'^reservation/$', views.reservation, name='reservation'),
    url(r'^checkout/$', views.checkout, name='checkout'),
    url(r'^review/$', views.leftReview, name='leftReview'),
    url(r'^accounts/login/$',  login, name='login'),
    url(r'^accounts/logout/$',  logout,  {'next_page': '/'}, name='logout'),
    url(r'^register/$', views.register, name='register'),
    url(r'^reservationlist/$', views.reservationlist, name='reservationlist')


]
