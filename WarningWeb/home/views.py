from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .form import AccountForm
from selenium import webdriver
from bs4 import BeautifulSoup

# Create your views here.
def index(request):
    location = request.session.get('location')
    temp = request.session.get('temp')
    humid = request.session.get('humidity')
    violet = request.session.get('violet')
    if request.session.get('location'):
        del request.session['location']
    return render(request,"homes.html", {'location': location, 'temp': temp, 'humid': humid, 'violet': violet})
  

def getCurrentWeather(location):
    driver = webdriver.Chrome('chromedriver')
    print("location: ", location)
    location = '-'.join(location.split('+')).lower()
    driver.get("https://thoitietvietnam.locvy.com/thoi-tiet-"+location)
    temp = driver.find_element_by_class_name('hientai')
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    info = soup.find_all('div', {'class': 'col-md-6'})[1]
    info_txt = info.find_all('div')[1:]

    humid = info_txt[2].text
    humid = humid.replace("Độ ẩm", "Humidity")

    violet = info_txt[6].text
    violet = violet.replace("Bức xạ UV", "Ultraviolet")
    violet = violet.replace("Thấp", "Low")
    violet = violet.replace("Cao", "High")

    return [temp.text, humid, violet]

def get_account_form(request):
    if request.method == "POST":
        form = AccountForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data['location'])
            locate = form.cleaned_data['location'].split(' ')
            locate = '+'.join(locate)
            request.session['location'] = locate
            info = getCurrentWeather(locate)
            request.session['temp'] = info[0]
            request.session['humidity'] = info[1]
            request.session['violet'] = info[2]
        return HttpResponseRedirect('/')
    return render(request, 'homes.html')