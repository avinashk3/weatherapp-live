from django.shortcuts import render, HttpResponse
from dashboard.forms import CityForm
from .models import City
from .helper import getweatherdata

# Create your views here.


def home(request):
    form = CityForm()
    context = {}
    if request.method == 'POST':
        
        form = CityForm(request.POST)
        if form.is_valid():
            form.save()
            city_name = form.cleaned_data.get("city_name")
            print(city_name)
            weather_data = getweatherdata(city_name)
            

    elif request.method == "GET":
        a = City.objects.first()
  
        if not a:
            weather_data = None
        else:
            city_name = City.objects.latest("date_added").city_name
            print(city_name)
            
            weather_data = getweatherdata(city_name)    
            print(weather_data)
            
    context['weather_data'] = weather_data
    context['form'] = form


    return render(request, 'home.html', context)


def history(request):
    cities = City.objects.all().order_by('-date_added')[:5]
    print(cities)
    weather = []
    for city in cities:
        city_name = city.city_name
        weather.append(getweatherdata(city_name))
    
    context = {
        'weather' : weather,
    }
    return render(request, 'history.html', context)