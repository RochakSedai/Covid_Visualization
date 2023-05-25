from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
import pandas as pd
import matplotlib.pyplot as plt
import geopy
import folium
from folium import plugins
from datetime import datetime, timedelta

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

    context = {
        "coronavirus_cases": covid_dict['Coronavirus Cases'],
        "Deaths": covid_dict['Deaths'],
        "Recovered": covid_dict['Recovered']
    }
   

    return render(request, 'home.html', context)


def get_table(request):
    return render(request, 'table.html')

def visualize_world(request):

    # Read the CSV file
    df = pd.read_csv('Covid_data.csv')

    # Drop the second row
    df = df.drop(0)

    # Remove commas from 'total Deaths' column and convert to float
    df['TotalCases'] = df['TotalCases'].str.replace(',', '').astype(float)
    df['TotalDeaths'] = df['TotalDeaths'].str.replace(',', '').astype(float)

    # Sort the DataFrame by total deaths in descending order
    df_sorted_cases = df.sort_values('TotalCases', ascending=False)
    df_sorted_deaths = df.sort_values('TotalDeaths', ascending=False)

    # Get the top 10 countries with maximum total deaths
    top_10_countries_cases = df_sorted_cases['Country,Other'].head(9).tolist()
    print(top_10_countries_cases)
    top_10_countries_deaths = df_sorted_deaths['Country,Other'].head(9).tolist()
    print(top_10_countries_deaths)

    # Calculate the sum of total deaths for the remaining countries
    other_cases = df_sorted_cases.loc[~df_sorted_cases['Country,Other'].isin(top_10_countries_cases), 'TotalCases'].sum()
    other_deaths = df_sorted_deaths.loc[~df_sorted_deaths['Country,Other'].isin(top_10_countries_deaths), 'TotalDeaths'].sum()

    # Create a new DataFrame for pie chart data
    pie_data_cases = pd.Series(df_sorted_cases.loc[df_sorted_cases['Country,Other'].isin(top_10_countries_cases), 'TotalCases'])
    pie_data_cases = pd.concat([pie_data_cases, pd.Series([other_cases], index=['Other'])])

    pie_data_deaths = pd.Series(df_sorted_deaths.loc[df_sorted_deaths['Country,Other'].isin(top_10_countries_deaths), 'TotalDeaths'])
    pie_data_deaths = pd.concat([pie_data_deaths, pd.Series([other_deaths], index=['Other'])])

    # Calculate the percentage values
    percentage_values_cases = pie_data_cases / pie_data_cases.sum() * 100
    percentage_values_deaths = pie_data_deaths / pie_data_deaths.sum() * 100


    # Plot the pie chart for total cases
    plt.pie(pie_data_cases, labels=None, autopct='%1.1f%%')
    plt.title('Top 10 Countries with Maximum TotalCases')
    plt.axis('equal')

    # # Retrieve country names from DataFrame based on index
    # country_names = [df.loc[df['TotalCases'] == cases, 'Country,Other'].values[0] for cases in pie_data.index]
    top_10_countries_cases.append('Other')

    # Create the legend labels with country names and percentages
    legend_labels = [f'{country}: {percentage:.1f}%' for country, percentage in zip(top_10_countries_cases, percentage_values_cases)]

    # Add the legend
    plt.legend(legend_labels, loc='best')

    # Save the plot as a PNG image file
    plt.savefig('api/static/TotalCases.png', dpi=300)

    # Display the plot
    plt.show()

    # Plot the pie chart for total deaths
    plt.pie(pie_data_deaths, labels=None)
    plt.title('Top 10 Countries with Maximum TotalDeaths')
    plt.axis('equal')

    # # Retrieve country names from DataFrame based on index
    # country_names = [df.loc[df['TotalCases'] == cases, 'Country,Other'].values[0] for cases in pie_data.index]
    top_10_countries_deaths.append('Other')

    # Create the legend labels with country names and percentages
    legend_labels = [f'{country}: {percentage:.1f}%' for country, percentage in zip(top_10_countries_deaths, percentage_values_deaths)]

    # Add the legend
    plt.legend(legend_labels, loc='best')

    # Save the plot as a PNG image file
    plt.savefig('api/static/TotalDeaths.png', dpi=300)

    # Display the plot
    plt.show()

    return render(request, 'visualization_world.html')


def world_heatmap(request):

    data = pd.read_csv('Covid_data.csv')

    # Drop the second row
    data = data.drop(0)

    # Remove commas from 'total Deaths' column and convert to float
    data['TotalCases'] = data['TotalCases'].str.replace(',', '').astype(float)
    # df['TotalDeaths'] = df['TotalDeaths'].str.replace(',', '').astype(float)

    # Initialize geocoder
    geolocator = geopy.geocoders.Nominatim(user_agent='heatmap_plot')

    # Geocode the locations in the dataset
    data['Location'] = data['Country,Other'].apply(lambda x: geolocator.geocode(x, timeout=10) if x is not None else None)
    data['Latitude'] = data['Location'].apply(lambda loc: loc.latitude if loc is not None else None)
    data['Longitude'] = data['Location'].apply(lambda loc: loc.longitude if loc is not None else None)

    # Create a folium map centered on the first location
    map_heatmap = folium.Map(location=[data['Latitude'].iloc[0], data['Longitude'].iloc[0]], zoom_start=2)

    # Generate heatmap layer
    heat_data = [[row['Latitude'], row['Longitude'], row['TotalCases']] for index, row in data.iterrows()]
    plugins.HeatMap(heat_data).add_to(map_heatmap)
    # Display the map
    map_heatmap.save('api/templates/heatmap.html')
    
    return render(request, 'heatmap.html')



def visualize_nepal(request):

    url = "https://www.worldometers.info/coronavirus/country/nepal/"
    data = requests.get(url)
    soup = BeautifulSoup(data.text,'html5lib')

    covid_dict = {}
    div = soup.find_all("div", {"id": "maincounter-wrap"})
    for i in div:
        content_div = i.find("div",{"class":"maincounter-number"})
        if content_div is not None:
            h1_tag = i.find("h1")
            if h1_tag is not None:
                key = h1_tag.text.replace(":", "").strip()
                value = content_div.find("span").text.strip()
                covid_dict[key] = value
    print(covid_dict)



    updates = soup.find_all('div', {"class": "news_post"})

    values = []
    for update in updates:
        strong_tags = update.find('strong')
        for tag in strong_tags:
            value = int(tag.get_text().split()[0]) 
            values.append(value)
    
    print(values)

    # Get the current date
    today = datetime.now().date()

    # Calculate the dates of the past 8 days
    dates = []
    for i in range(8):
        delta = timedelta(days=i)
        date = today - delta
        dates.append(date.strftime('%Y-%m-%d'))

    print(dates)

    actual_value_str = covid_dict['Coronavirus Cases']
    actual_value = int(actual_value_str.replace(',', '').strip())

    covid_data = [actual_value]
    for value in values:
        actual_value -= value
        covid_data.append(actual_value)

    print(covid_data)

    context = {
        "coronavirus_cases": covid_dict['Coronavirus Cases'],
        "Deaths": covid_dict['Deaths'],
        "Recovered": covid_dict['Recovered']
    }
   

    return render(request, 'visualization_nepal.html', context)