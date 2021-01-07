from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .form import AccountForm
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import datetime

from selenium.webdriver.chrome.options import Options
#from selenium.webdriver.firefox.options import Options
import re
import time

chrome_options = Options()
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(executable_path='chromedriver.exe', options=chrome_options)
#driver = webdriver.Firefox(options=chrome_options)

# Create your views here.
def index(request):
    if request.session.get('location'):
        location = request.session.get('location')
        del request.session['location']
    else:
        location = ""

    if request.session.get('temp'):
        temp = request.session.get('temp')
        del request.session['temp']
    else:
        temp = "0"

    if request.session.get('humidity'):
        humid = request.session.get('humidity')    
        del request.session['humidity']
    else:
        humid = "Humidity: 0%"

    if request.session.get('violet'):
        violet = request.session.get('violet')
        del request.session['violet']
    else:
        violet = "Ultraviolet: Unknown"

    if request.session.get('h1n1'):
        h1n1 = request.session.get('h1n1')
        del request.session['h1n1']
    else:
        h1n1 = ""

    if request.session.get('h3'):
        h3 = request.session.get('h3')
        del request.session['h3']
    else:
        h3 = ""

    if request.session.get('b'):
        b = request.session.get('b')
        del request.session['b']
    else:
        b = ""

    return render(request,"homes.html", {'location': location, 'temp': temp, 'humid': humid, 'violet': violet, 'h1n1': h1n1, 'h3': h3, 'b': b})

def test(request):
    if request.session.get('date'):
        date = request.session.get('date')
        del request.session['date']
    else:
        date = ""

    if request.session.get('h1n1_test'):
        h1 = request.session['h1n1_test']
        del request.session['h1n1_test']
    else:
        h1 = ""

    if request.session.get('h3_test'):
        h3 = request.session['h3_test']
        del request.session['h3_test']
    else:
        h3 = ""

    if request.session.get('b_test'):
        b = request.session['b_test']
        del request.session['b_test']
    else:
        b = ""


    return render(request, "test.html", {'date': date, 'h1n1': h1, 'h3': h3, 'b': b})

def getWeatherByWeek(location):

    driver.get('https://thoitietvietnam.locvy.com/thoi-tiet-hang-ngay/'+location)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    day_sources = soup.find_all('div', {'class':'panel-body daily'})
    days = []
    temps = []
    rain_probas = []
    rains = []
    gusts = []
    humids = []
    uv_nums = []
    uv_labels = []
    
    def add_data(day_num, day_source):
        for idx, ele in enumerate(day_source):
            if (ele.name == 'div' and ele.string is not None):
                if idx == 5:
                    days.append(day_num)
                    temp = int(re.search('Cao \d+',ele.string).group().split()[-1])
                    rain_proba = re.search('Khả năng có mưa \d+',ele.string)
                    if rain_proba is None:
                        rain_proba = 0
                    else:
                        rain_proba = int(rain_proba.group().split()[-1])
                    rain = re.search('Lượng mưa khoảng \d+',ele.string)
                    if rain is None and rain_proba < 60:
                        rain = 0
                    elif rain is not None:
                        rain = int(rain.group().split()[-1])
                    else:
                        rain = None
                    temps.append(temp)
                    rain_probas.append(rain_proba)
                    rains.append(rain)
                if idx == 9:
                    gust = int(re.search('Tốc độ gió: \d+',ele.string).group().split()[-1])
                    gusts.append(gust)
                    # print(gust, end='')
                if idx == 11:
                    humid = int(re.search('Độ ẩm: \d+',ele.string).group().split()[-1])
                    humids.append(humid)
                    # print(humid)
                if idx == 13:
                    uv_num = int(ele.string.split(': ')[-1])
                    uv_nums.append(uv_num)
                if idx == 15:
                    uv_label = ele.string.split(': ')[-1]
                    uv_labels.append(uv_label)
                if idx == 23:
                    days.append(day_num)
                    temp = int(re.search('Thấp \d+',ele.string).group().split()[-1])
                    rain_proba = re.search('Khả năng có mưa \d+',ele.string)
                    if rain_proba is None:
                        rain_proba = 0
                    else:
                        rain_proba = int(rain_proba.group().split()[-1])
                    rain = re.search('Lượng mưa khoảng \d+',ele.string)
                    if rain is None and rain_proba < 60:
                        rain = 0
                    elif rain is not None:
                        rain = int(rain.group().split()[-1])
                    else:
                        rain = None
                    temps.append(temp)
                    rain_probas.append(rain_proba)
                    rains.append(rain)
                if idx == 27:
                    gust = int(re.search('Tốc độ gió: \d+',ele.string).group().split()[-1])
                    gusts.append(gust)
                if idx == 29:
                    humid = int(re.search('Độ ẩm: \d+',ele.string).group().split()[-1])
                    humids.append(humid)
                if idx == 31:
                    uv_num = int(ele.string.split(': ')[-1])
                    uv_nums.append(uv_num)
                if idx == 33:
                    uv_label = ele.string.split(': ')[-1]
                    uv_labels.append(uv_label)

    for day_num, day_source in enumerate(day_sources):
        add_data(day_num, day_source)
    
    data = pd.DataFrame({'days':days,'temps':temps,'rains':rains,'rain_probas':rain_probas,'gusts':gusts,'humids':humids,'uv_nums':uv_nums,'uv_labels':uv_labels})
    data['rains'].fillna(np.mean(data['rains']), inplace=True)
    data_gb = data.groupby('days').agg(['mean', 'max', 'min']).reset_index()
    data_gb.columns = [x[0]+'_'+x[1] for x in data_gb.columns]
    data_gb['days_'] = 1
    data_gbgb = data_gb.groupby('days_').agg(['mean', 'max', 'min']).reset_index()
    data_gbgb.columns = [x[0]+'_'+x[1] for x in data_gbgb.columns]

    # start = time.time()
    # data = get_weather_weeks(location)
    # print(data.columns)
    selected = [col for col in data_gbgb.columns if 'uv' not in col and ('mean_mean' in col or 'min_mean' in col or 'max_mean' in col)]
    dataX = data_gbgb[selected]

    from joblib import dump, load
    h1n1_model = load('model/AH1N1.joblib')
    h3_model = load('model/AH3.joblib')
    b_model = load('model/B.joblib')
    # print(h1n1_model)
    return [h1n1_model.predict(dataX)[0], h3_model.predict(dataX)[0], b_model.predict(dataX)[0]]

def getCurrentWeather(location):
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

def getHistoricalPredict(weeks, year):
    weeks = int(weeks)
    year = int(year)
    weeks += 2
    data = pd.read_csv('model/data_label.csv')
    selected = [col for col in data.columns if 'uv' not in col and ('mean_mean' in col or 'min_mean' in col or 'max_mean' in col)]
    dataX = data[(data['year'] == year) & (data['weeks'] == weeks)][selected]
    from joblib import dump, load
    h1n1_model = load('model/AH1N1.joblib')
    h3_model = load('model/AH3.joblib')
    b_model = load('model/B.joblib')
    # print(h1n1_model)
    print(dataX)
    return [h1n1_model.predict(dataX)[0], h3_model.predict(dataX)[0], b_model.predict(dataX)[0]]

def get_position_form(request):
    if request.method == "POST":
        form = AccountForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data['location'])
            locate = form.cleaned_data['location'].split(' ')
            locate = '+'.join(locate)
            request.session['location'] = locate

            location = '-'.join(locate.split('+')).lower()

            info = getCurrentWeather(location)
            request.session['temp'] = info[0]
            request.session['humidity'] = info[1]
            request.session['violet'] = info[2]

            # location = '-'.join(locate.split('-'))
            warning = getWeatherByWeek(location)
            request.session['h1n1'] = warning[0]
            request.session['h3'] = warning[1]
            request.session['b'] = warning[2]
            print(warning)
        return HttpResponseRedirect('/')
    return render(request, 'homes.html')

def get_date_form(request):
    if request.method == "POST":
        form = AccountForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data['location'])
            # 2021-01-12 / YYYY-MM-DD
            date = form.cleaned_data['location']
            request.session['date'] = date
            d = datetime.datetime.strptime(date, "%Y-%m-%d")
            weeks, year = d.strftime('%U %Y').split()
            print(weeks, year)
            warning = getHistoricalPredict(weeks, year)
            request.session['h1n1_test'] = warning[0]
            request.session['h3_test'] = warning[1]
            request.session['b_test'] = warning[2]
            print(warning)
            print(request)
        return HttpResponseRedirect('/test')
    return render(request, 'test.html')