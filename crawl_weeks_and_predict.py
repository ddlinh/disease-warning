import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


from bs4 import BeautifulSoup
import re
import time

chrome_options = Options()
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(executable_path='chromedriver.exe', options=chrome_options)

def get_weather_weeks(location='ho-chi-minh'):
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
    # print(days, len(days))
    # print(temps, len(temps))
    # print(rains, len(rains))
    # print(rain_probas, len(rain_probas))
    # print(gusts, len(gusts))
    # print(humids, len(humids))
    # print(uv_nums, len(uv_nums))
    # print(uv_labels, len(uv_labels))
    data = pd.DataFrame({'days':days,'temps':temps,'rains':rains,'rain_probas':rain_probas,'gusts':gusts,'humids':humids,'uv_nums':uv_nums,'uv_labels':uv_labels})
    data['rains'].fillna(np.mean(data['rains']), inplace=True)
    data_gb = data.groupby('days').agg(['mean', 'max', 'min']).reset_index()
    data_gb.columns = [x[0]+'_'+x[1] for x in data_gb.columns]
    data_gb['days_'] = 1
    data_gbgb = data_gb.groupby('days_').agg(['mean', 'max', 'min']).reset_index()
    data_gbgb.columns = [x[0]+'_'+x[1] for x in data_gbgb.columns]
    return data_gbgb

start = time.time()
data = get_weather_weeks('ho-chi-minh')
# print(data.columns)
selected = [col for col in data.columns if 'uv' not in col and ('mean_mean' in col or 'min_mean' in col or 'max_mean' in col)]
dataX = data[selected]

from joblib import dump, load
h1n1_model = load('model/AH1N1.joblib')
h3_model = load('model/AH3.joblib')
b_model = load('model/B.joblib')
# print(h1n1_model)
print("H1N1:",h1n1_model.predict(dataX))

# print(h3_model)
print("H3:", h3_model.predict(dataX))

# print(b_model)
print("B:", b_model.predict(dataX))
driver.close()
print(time.time() - start)
