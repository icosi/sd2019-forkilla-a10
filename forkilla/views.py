# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from django.urls import reverse
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.
from django.http import HttpResponse
from .models import * #Restaurant, ViewedRestaurants, Reservation, RestaurantInsertDate, Review

from django import forms
from .forms import ReservationForm, ReviewForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import auth

from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from .serializers import RestaurantSerializer, ReviewSerializer
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from .permissions import *
from rest_framework import permissions
import datetime

import json
from django.core.serializers.json import DjangoJSONEncoder

from django.shortcuts import render_to_response
from django.template import RequestContext


# localhost:8000/admin --> user: quim       password: distribuit


def index(request):
    #return HttpResponse("Funciona.")
    return restaurants(request)

#@login_required
def restaurants(request,city="", category=""):

    search_field = request.GET.get('search', '')
    print("search field: ",search_field)

    if (city == ""):
        try:
            city = request.GET["city"]
        except:
            city = ""
    
    if (category == ""):
        try:
            category = request.GET["category"]
        except:
            category = "" 



    if city and category:
        restaurants = Restaurant.objects.filter(city__iexact=city, category__iexact=category)
    elif city:
        restaurants = Restaurant.objects.filter(city__iexact=city)
    else:
        restaurants = Restaurant.objects.all()

    context = {
        'city': city,
        'category': category,
        'restaurants': restaurants,
        'promoted': Restaurant.objects.filter(is_promot=True).order_by('?')[:4],
        'viewedrestaurants': _check_session(request),
        'authenticated': request.user.is_authenticated,
        'username': request.user.username
    }
    return render(request, 'forkilla/restaurants.html', context)



def details(request,restaurant_number=""):
    #del request.session["restaurant_number"]
    print("yea")
    request.session["restaurant_number"] = restaurant_number

    try:
        if request.method == "POST":
            form = ReviewForm(request.POST)
            if form.is_valid():
                rate = form.cleaned_data['rate']
                message = form.cleaned_data['message']

                restaurant = Restaurant.objects.get(restaurant_number=restaurant_number)

                rev = form.save(commit=False)
                rev.restaurant = restaurant
                rev.author = request.user
                rev.save()

                request.session["restaurant_number"] = restaurant_number
                request.session["result"] = "OK"
            else:
                request.session["result"] = form.errors
            return HttpResponseRedirect(reverse('details', args=(restaurant_number,)))

        elif request.method == "GET":
            viewedrestaurants = _check_session(request)
            restaurant = Restaurant.objects.get(restaurant_number=restaurant_number)
            lastviewed = RestaurantInsertDate(viewedrestaurants=viewedrestaurants,restaurant= restaurant)
            lastviewed.save()

            reviews = Review.objects.filter(restaurant = restaurant)
            context = {
                'restaurant': restaurant,
                'viewedrestaurants': viewedrestaurants,
                'reviews': reviews,
                'reviewForm': ReviewForm(),
                'authenticated': request.user.is_authenticated,
                'username': request.user.username,
                'static_path': restaurant.get_static_path
            }
    except Restaurant.DoesNotExist:
        return HttpResponse("Restaurant Does not exists")
    return render(request, 'forkilla/details.html', context)

@login_required
def reservation(request):
    try:
        if request.method == "POST":
            form = ReservationForm(request.POST)
            if form.is_valid():
                day = form.cleaned_data['day']
                time_slot = form.cleaned_data['time_slot']
                num_people = form.cleaned_data['num_people']

                restaurant_number = request.session["reserved_restaurant"]
                restaurant = Restaurant.objects.get(restaurant_number=restaurant_number)
                # Afagem totes les reserves del restaurant durant el dia i la hora seleccionades
                reservations = Reservation.objects.filter(restaurant = restaurant, time_slot = time_slot, day = day)

                # Calculem el numero de gent que hi ha reservada en aquest moment
                totalPeople = 0
                for reserva in reservations:
                    print ("Reserva comprovada")
                    totalPeople = totalPeople + reserva.num_people

                # Si la nova reserva no es pot fer, no la realitzem
                if (totalPeople + num_people > restaurant.capacity):
                    print ("Superada capacitat maxima del restaurant per aquesta hora")
                    request.session["result"] = "FULL"
                
                else:
                    resv = form.save(commit=False)
                    resv.restaurant = restaurant
                    resv.author = request.user
                    resv.save()
                    request.session["reservation"] = resv.id
                    request.session["result"] = "OK"

            else:
                 request.session["result"] = form.errors
            return HttpResponseRedirect(reverse('checkout'))

        elif request.method == "GET":
            restaurant_number = request.GET["reservation"]
            restaurant = Restaurant.objects.get(restaurant_number=restaurant_number)
            request.session["reserved_restaurant"] = restaurant_number

            viewedrestaurants = _check_session(request)
            lastviewed = RestaurantInsertDate(viewedrestaurants=viewedrestaurants,restaurant= restaurant)
            lastviewed.save()

            form = ReservationForm()
            context = {
                'restaurant': restaurant,
                'viewedrestaurants': viewedrestaurants,
                'form': form,
                'authenticated': request.user.is_authenticated,
                'username': request.user.username
            }
    except Restaurant.DoesNotExist:
        return HttpResponse("Restaurant Does not exists")
    return render(request, 'forkilla/reservation.html', context)



def _check_session(request):
    if "viewedrestaurants" not in request.session:
        viewedrestaurants = ViewedRestaurants()
        viewedrestaurants.save()
        request.session["viewedrestaurants"] = viewedrestaurants.id_vr
    else:
        viewedrestaurants = ViewedRestaurants.objects.get(id_vr=request.session["viewedrestaurants"])
    return viewedrestaurants


def checkout(request):
    form_result = request.session["result"]

    # On base.html. slice doesn't work as expected

    if (form_result == "FULL"):
        context = {
            'form_full': form_result,
            'authenticated': request.user.is_authenticated,
            'username': request.user.username
        }
    else:
        context = {
            'form_ok': form_result,
            'reservation_id': request.session["reservation"],
            'viewedrestaurants': _check_session(request),
            'authenticated': request.user.is_authenticated,
            'username': request.user.username
        }

    return render(request, 'forkilla/checkout.html', context)


@login_required
def leftReview(request):
    form_result = request.session["result"]
    restaurant_number = request.session["restaurant_number"]
    restaurant = Restaurant.objects.get(restaurant_number=restaurant_number)

    reviews = Review.objects.filter(restaurant = restaurant)

    if (form_result == "OK"):
        context = {
            'restaurant': restaurant,
            'form_full': form_result,
            'viewedrestaurants': _check_session(request),
            'reviews': reviews,
            'authenticated': request.user.is_authenticated,
            'username': request.user.username
        }
    else:

        context = {
            'restaurant': restaurant,
            'viewedrestaurants': _check_session(request),
            'reviews': reviews,
            'authenticated': request.user.is_authenticated,
            'username': request.user.username
        }
    return render(request, 'forkilla/details.html', context)



def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect(reverse("index"))
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {
        'form': form,
    })

def logout_view(request):
    logout(request)
    context = {
        'authenticated': request.user.is_authenticated,
        'username': request.user.username
    }
    return render(request, 'registration/logged_out.html', context)

def profile(request):
    Reservation.objects.order_by('day')

    reservations = Reservation.objects.filter(author = request.user)
    reviews = Review.objects.filter(author = request.user)

    #reservation_json = json.dumps(list(reservations), cls=DjangoJSONEncoder)

    ## IMPORTANT -- Encara hi ha un error al mostrar 'viewedrestaurants' 
    #           amb slice:"5" a la vista
    context = {
        'authenticated': request.user.is_authenticated,
        'username': request.user.username,
        'reservations': reservations,
        #'reservations_json': reservations_json,
        'reviews': reviews,
        'viewedrestaurants': _check_session(request),
        'time': datetime.datetime.now()

    }
    return render(request, 'forkilla/profile.html', context)



class RestaurantViewSet(viewsets.ModelViewSet):
            """
            API endpoint that allows Restaurants to be viewed or edited.
            """
            queryset = Restaurant.objects.all().order_by('category')
            #permission_classes = [read_run_permission,Comercial_permission]
            permission_classes =[Comercial_permission]

            serializer_class = RestaurantSerializer
            

            def get_queryset(self):
                """
                Optionally restricts the returned purchases to a given user,
                by filtering against a `username` query parameter in the URL.
                """
                queryset = Restaurant.objects.all()
                category = self.request.query_params.get('category', None)
                city = self.request.query_params.get('city', None)
                price_average = self.request.query_params.get('price', None)

                if category is not None:
                    queryset = queryset.filter(category=category)
                if city is not None:
                    queryset = queryset.filter(city=city)
                if price_average is not None:
                    queryset = queryset.filter(price_average__lte=price_average)
                return queryset

     
            # Detail view from /api/restaurants/{{restaurant_number}}
            def retrieve(self, request, pk=None):
                print ("RETRIEVE")
                restaurant = Restaurant.objects.get(restaurant_number=pk)
                serializer = RestaurantSerializer(restaurant)
                return Response(serializer.data)

            #permission_class = [IsAdminUser,]
            #http_method_names = ['get', 'post', 'head']

            """def retrieve(self, request, pk=None):
                print ("RETRIEVE")
                restaurant = Restaurant.objects.get(restaurant_number=pk)
                serializer = RestaurantSerializer(restaurant)
                return Response(serializer.data)
            
            def destroy(self, request, pk=None):
                print ("DESTROY")
                restaurant = Restaurant.objects.get(restaurant_number=pk).delete()
                return HttpResponseRedirect('/api/restaurants')

            def update(self, request, pk=None):
                print ("PUT")
                #print (request.body)
                restaurant2=request.body
                restaurant = Restaurant.objects.get(restaurant_number=pk)
                
                return HttpResponseRedirect('/api/restaurants')"""



class ReviewViewSet(viewsets.ModelViewSet):
            """
            API endpoint that allows Restaurants to be viewed or edited.
            """
            queryset = Review.objects.all()
            permission_classes = [Comercial_permission]
            
            serializer_class = ReviewSerializer

            


def comparator(request, ips):
    context = {
        'authenticated': request.user.is_authenticated,
        'username': request.user.username,
        'ips': ips,
        'length': len(ips)
    }
    return render(request, 'forkilla/comparator.html', context)




def handler404(request):
    data = {}
    return render(request, 'forkilla/404.html', data)


def handler500(request):
    data = {}
    return render(request, 'forkilla/500.html', data)


## IMPORTANT -- 
#           Poder eliminar reserves i comentaris des del perfil
#           Agafar la foto de cada restaurant de forma dinamica
#           (Done) Error views (done. settings.py DEGUB = False)
#           (Almost) Restfull (Falta: afegir 'snippers' als models Restaurants i Review per a que un usuari no pugui modificar un model que ha creat algu altre)
#           Heroku
#           (Done) Web comparator


#   Entrega:
#       - Deploymen fet a heroku (comprovacio en localhost)
#       - Resum sessio de test -->
#               Registre/Login   |   Comparador     |     
#       - Especificar user/pass d'usuaris
#       - Comentaris sobre el codi
