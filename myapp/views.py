from django.shortcuts import render
from pprint import pprint
# Create your views here.
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
from lxml import etree
import json


def home(request):
    url = "https://en.wikipedia.org/wiki/India"
    table_class = "infobox ib-country vcard"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    india_table = soup.find('table', attrs={'class': table_class})
    aaa = soup.find('a', {'class': 'image'})['href']
    name = soup.find('title').text.replace(" - Wikipedia", "")
    result = []
    aaa = 'https://en.wikipedia.org' + aaa
    result.append({'flag_url': aaa})

    table_row = [row for row in india_table.find_all('tr')[6:]]
    for row in table_row:
        for data in row.find_all('th'):
            for td in row.find_all('td'):
                result.append({data.text.replace("\xa0", " "): td.text})

    print(result)
    return render(request, 'home.html', {"name": name, "df": result})
