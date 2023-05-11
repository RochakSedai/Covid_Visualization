from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
import pandas as pd
# Create your views here.
def home(request):

    url = "https://www.worldometers.info/coronavirus/?utm_campaign=homeAdvegas1?%22%20%5Cl%22countries"
    data = requests.get(url)
    soup = BeautifulSoup(data.text,'html5lib')

    covid_dict = {}
    div = soup.find_all("div", {"id": "maincounter-wrap"})
    for i in div:
        content_div = i.find("div",{"class":"maincounter-number"})
        covid_dict[i.find("h1").text.replace(":","").strip()] = content_div.find("span").text.strip()
    print(covid_dict)

    tables = soup.find_all('table')
    table_header = tables[0].find_all('th')
    table_head = []
    for i in range(15):
        if i != 0:
            table_head.append(table_header[i].text.replace("\n","").replace("\xa0",""))
    print(table_head)

    Covid_data = pd.DataFrame(columns=table_head)
    Covid_data = Covid_data.drop(Covid_data.columns[-2:], axis=1)
    print(Covid_data)
    print(type(Covid_data))
    for row in tables[0].tbody.find_all('tr'):
        col = row.find_all('td')
        if (col != []):
            country = col[1].text.strip()
            totalCases = col[2].text.strip()
            newCases = col[3].text.strip()
            totalDeaths = col[4].text.strip()
            newDeaths = col[5].text.strip()
            totalRecovered = col[6].text.strip()
            newRecovered = col[7].text.strip()
            activeCases = col[8].text.strip()
            serious = col[9].text.strip()
            totalCases_per_m = col[10].text.strip()
            deaths = col[11].text.strip()
            totalTests = col[12].text.strip()
            tests_per_m = col[13].text.strip()
            population = col[14].text.strip()
            new_row = {
            "Country,Other": country,
            "TotalCases": totalCases,
            "NewCases": newCases,
            "TotalDeaths": totalDeaths,
            "NewDeaths": newDeaths,
            "TotalRecovered": totalRecovered,
            "NewRecovered": newRecovered,
            "ActiveCases": activeCases,
            "Serious,Critical": serious,
            "TotCases/1M pop": totalCases_per_m,
            "Deaths/1M pop": deaths,
            "TotalTests": totalTests
            }
            Covid_data = pd.concat([Covid_data, pd.DataFrame(new_row, index=[0])], ignore_index=True)
        
    Covid_data.drop(Covid_data.index[:7],inplace=True)

    Covid_data.to_csv("Covid_data.csv",index=False)
    Covid_json_data = Covid_data.to_json(orient='records')

    # Save JSON data to a file
    with open('/home/sedairochak/Covid_Visualization/covid_tracking/api/static/Covid_data.json', 'w') as f:
        f.write(Covid_json_data)
    return render(request, 'home.html')