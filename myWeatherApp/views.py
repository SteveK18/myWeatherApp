from django.shortcuts import render, redirect
from django.http import HttpResponse
import datetime
import requests
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from . forms import UserRegisterForm
from django.contrib.auth.decorators import login_required


    
# Create your views here.
#Function to read and use the API key to fetch data for a POST request
def index(request):
    API_KEY = open("C:\\Users\\k_ste\Desktop\\Django\\weatherProject\\myWeatherApp\\API_KEY", "r").read()
    weather_data= "https://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&APPID={}"
    forecast = "https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude=current,minutely,hourly,alerts&appid={}"

    #If its a POST request from the user then get data through the URL
    if request.method == "POST":
        city = request.POST['city'] #POST allows python to read the user's input
        weather_output = data_received(city, API_KEY, weather_data, forecast)
    
        context = {
            "weather_output": weather_output
        }
        return render(request, "weather_app/home.html", context)
    else: #if its a GET request then just render and display the file
        return render(request, "weather_app/home.html")
    
    

#Fuction that receives the data from user input (POST)
def data_received(city, API_KEY, weather_data, forecast):
    response = requests.get(weather_data.format(city, API_KEY)).json()
    lat, lon = response['coord']['lat'], response['coord']['lon']
    forecast_response = requests.get(forecast.format(lat, lon, API_KEY)).json()
    temp = round(response['main']['temp'])
    degree = '\u00b0'

    #Variable that takes the above info and formats it into a template for html
    weather_output = {
        "City": city,
        "Temperature": round(response['main']['temp']),
        "Description": response['weather'][0]['description'],
        "icon": response['weather'][0]['icon']
    }

    return weather_output


#Defining the user registration page below
def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Welcome { username }, your account was created')
            return redirect('index')
    else:
        form = UserRegisterForm()

    return render(request, 'weather_app/register.html', {'form':form})

#Defining the user profile below
@login_required
def profile(request):
    return render(request, 'weather_app/profile.html')

#Defining the About us page
def about_us(request):
    return render(request, 'weather_app/about_us.html')

#Defining the resource page on our wensite below
def resources(request):
    return render(request, 'weather_app/resources.html')