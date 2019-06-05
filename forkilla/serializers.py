from .models import Restaurant, Review
from rest_framework import serializers


class RestaurantSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Restaurant
        fields = (
        'restaurant_number', 'name', 'menu_description', 
	'price_average', 'is_promot', 'rate', 'address', 
	'city', 'country', 'featured_photo', 'category', 
	'capacity')

class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = ('id_review',
        'rate', 'message', 'restaurant', 
	'author')


