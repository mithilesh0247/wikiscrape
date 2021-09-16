from django.shortcuts import render

# Create your views here.
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
from lxml import etree


def home(request):
    url = "https://en.wikipedia.org/wiki/India"
    HEADERS = ({'User-Agent':
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
            (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
                'Accept-Language': 'en-US, en;q=0.5'})
    table_class = "infobox ib-country vcard"
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')
    aaa = soup.find('a', {'class': 'image'})['href']
    aaa = 'https://en.wikipedia.org' + aaa
    dom = etree.HTML(str(soup))
    city = []
    language = []
    totalData = []
    totalData.append(aaa)
    capital = dom.xpath(
        '//*[@id="mw-content-text"]/div[1]/table[1]/tbody/tr[7]/td/a')[0].text
    totalData.append(capital)
    largest_city = dom.xpath(
        '//*[@id="mw-content-text"]/div[1]/table[1]/tbody/tr[8]/td/div')
    for tr in largest_city:
        tr = list(map(lambda x: x.text, tr.iter()))
    for t in tr:
        if t is not None and t != '\n':
            city.append(t)

    totalData.append(city)
    lang = dom.xpath(
        '//*[@id="mw-content-text"]/div[1]/table[1]/tbody/tr[9]/td/div')
    for tr in lang:
        tr = list(map(lambda x: x.text, tr.iter()))
    for th in tr:
        if th is not None:
            language.append(th)

    totalData.append(language)
    area = dom.xpath(
        '//*[@id="mw-content-text"]/div[1]/table[1]/tbody/tr[33]/td')[0].text
    totalData.append(area)
    population = dom.xpath(
        '//*[@id="mw-content-text"]/div[1]/table[1]/tbody/tr[36]/td/text()[1]')
    totalData.append(population)
    gdp = dom.xpath(
        '//*[@id="mw-content-text"]/div[1]/table[1]/tbody/tr[43]/td/span')[0].text
    totalData.append(gdp)
    print(area, population, gdp, city, capital, language)
    # india_table = soup.find('table', attrs={'class': table_class})
    # df = pd.read_html(str(india_table))

    # df['json'] = df.apply(lambda x: x.to_json(), axis=1)
    # for i in df.index:
    #     df.loc[i].to_json("row{}.json".format(i))
    # print(df)
    # '''indiatable=soup.find('table',{'class':"infobox"})
    # df=pd.read_html(str(indiatable))
    # df.drop(columns=['Repiblic of india', 'Motto'])
    # #df=pd.DataFrame(df[0])'''
    return render(request, 'home.html', {"df": totalData})
