# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator



def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'forkilla/static/forkilla/images/{0}/{1}'.format(instance.restaurant_number, filename)

# Create your models here.
class Restaurant(models.Model):
    CATEGORIES = (
        ("Rice", "Rice"),
        ("Fusi", "Fusion"),
        ("BBQ", "Barbecue"),
        ("Chin", "Chinese"),
        ("Medi","Mediterranean"),
        ("Crep","Creperie"),
        ("Hind","Hindu"),
        ("Japa","Japanese"),
        ("Ital","Italian"),
        ("Mexi","Mexican"),
        ("Peru", "Peruvian"),
        ("Russ","Russian"),
        ("Turk","Turkish"),
        ("Basq","Basque"),
        ("Vegy", "Vegetarian"),
        ("Afri","African"),
        ("Egyp","Egyptian"),
        ("Grek","Greek")
    )
    _d_categories = dict(CATEGORIES)
     
    restaurant_number = models.CharField(primary_key=True, max_length=8, unique=True)
    name = models.CharField(max_length=50)
    menu_description = models.TextField()
    price_average = models.DecimalField(max_digits=5, decimal_places=2)
    is_promot = models.BooleanField(default=False)
    rate = models.DecimalField(max_digits=3, decimal_places=1)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    featured_photo = models.ImageField(upload_to=user_directory_path)
    category = models.CharField(max_length=5, choices=CATEGORIES)
    capacity = models.PositiveIntegerField()
    
    def get_human_category(self):
        return self._d_categories[self.category]
        
    def get_static_path(self):
        x = str(self.featured_photo)
        return x[15:]
        
    def __str__(self):
        return ('[**Promoted**]' if self.is_promot else '') + "[" + self.category + "] " \
                "[" + self.restaurant_number + "] " + self.name + " - " + self.menu_description + " (" + str(self.rate) + ")" \
                ": " + str(self.price_average) + u" euros"


class Reservation(models.Model):
    SLOTS = (
        ("morning_first", "12h00"),
        ("morning_second", "13h00"),
        ("morning_third", "14h00"),
        ("morning_fourth", "15h00"),
        ("evening_first", "20h00"),
        ("evening_second", "21h00"),
        ("evening_third", "22h00"),
    )
    _d_slots = dict(SLOTS)
    id = models.AutoField(primary_key=True)
    restaurant = models.ForeignKey(Restaurant)
    day = models.DateField(default=datetime.now)
    time_slot = models.CharField(max_length=15, choices=SLOTS)
    num_people = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])

    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_human_slot(self):
        return self._d_slots[self.time_slot]




class ViewedRestaurants(models.Model):
   id_vr = models.AutoField(primary_key=True)
   restaurant = models.ManyToManyField(Restaurant, through='RestaurantInsertDate')


class RestaurantInsertDate(models.Model):
    viewedrestaurants = models.ForeignKey(ViewedRestaurants, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

class Meta:
    ordering = ['-date_added']

class Review(models.Model):
    id_review = models.AutoField(primary_key=True)
    rate = models.PositiveIntegerField(validators=[MaxValueValidator(10),MinValueValidator(1)])
    message = models.TextField()
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
