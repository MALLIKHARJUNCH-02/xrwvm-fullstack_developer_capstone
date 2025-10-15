from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from .models import CarMake, CarModel
import json
import logging

logger = logging.getLogger(__name__)


@csrf_exempt
def login_user(request):
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return JsonResponse({"userName": username, "status": "Authenticated"})
    return JsonResponse({"userName": username, "status": "Failed"})


def logout_request(request):
    logout(request)
    return JsonResponse({"userName": ""})


@csrf_exempt
def registration(request):
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    first_name = data['firstName']
    last_name = data['lastName']
    email = data['email']

    if User.objects.filter(username=username).exists():
        return JsonResponse({"userName": username, "error": "Already Registered"})

    user = User.objects.create_user(
        username=username,
        first_name=first_name,
        last_name=last_name,
        password=password,
        email=email
    )
    login(request, user)
    return JsonResponse({"userName": username, "status": "Authenticated"})


def get_cars(request):
    """
    Return all car models with their make.
    If database is empty, populate initial CarMake and CarModel data.
    """
    if CarMake.objects.count() == 0:
        # Populate initial data
        toyota = CarMake.objects.create(name="Toyota", description="Japanese car manufacturer")
        honda = CarMake.objects.create(name="Honda", description="Japanese car manufacturer")
        ford = CarMake.objects.create(name="Ford", description="American car manufacturer")

        CarModel.objects.create(car_make=toyota, name="Corolla", type="SEDAN", year=2020)
        CarModel.objects.create(car_make=toyota, name="RAV4", type="SUV", year=2021)
        CarModel.objects.create(car_make=honda, name="Civic", type="SEDAN", year=2019)
        CarModel.objects.create(car_make=ford, name="Mustang", type="SEDAN", year=2022)

    car_models = CarModel.objects.select_related('car_make')
    cars = [{"CarModel": cm.name, "CarMake": cm.car_make.name} for cm in car_models]
    return JsonResponse({"CarModels": cars})
