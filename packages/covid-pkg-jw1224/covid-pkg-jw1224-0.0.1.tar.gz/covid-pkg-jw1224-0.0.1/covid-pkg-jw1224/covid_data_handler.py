'''
This module handles the Covid-19 data for the Covid Dashboard.
It retrieves the current figures using an API request then searches through the data in order to pick out the necessary statistics.
'''

from uk_covid19 import Cov19API
import json
import pandas as pd



def parse_csv_data(csv_filename):
    '''Reads a csv file of Covid data and converts into a list of strings'''
    data = open ( csv_filename , 'r' ).readlines() #convert lines into list of strings
    return data
    
def process_covid_csv_data(covid_csv_data) -> int:
    '''Takes in the parsed Covid data and processes it in order to return the required figures'''
    nation_check = covid_csv_data[1].split(',')
    nation_check = str(nation_check[2])
    last7days_cases = 0
    for i in range(3,10): #iterate through 7 days, starting 2 days back
        last7days_cases_lines = covid_csv_data[i].split(',')
        last7days_cases += int(float(last7days_cases_lines[6]))
    if nation_check == 'nation':
        current_hospital_cases_lines = covid_csv_data[1].split(',') #split string into new list, possible change index to something better
        current_hospital_cases = int(float(current_hospital_cases_lines[5]))
    else:
        current_hospital_cases = 0
    if nation_check == 'nation':
        for i in covid_csv_data[1:]:
            if i.split(',')[4] != '':
                total_deaths_lines = i.split(',')
                total_deaths = int(float(total_deaths_lines[4]))
                break #not efficient?
            else:
                next
    else:
        total_deaths = 0
    
    return last7days_cases, current_hospital_cases, total_deaths

def covid_API_request(location: str, location_type: str):
    '''Sends an API request to retrieve the Covid data given certain variables'''
    area = [
    f'areaType={location_type}',
    f'areaName={location}'
]

    cases_and_deaths = {
        "areaCode": "areaCode",
        "areaName": "areaName",
        "areaType": "areaType",
        "date": "date",
        "cumDailyNsoDeathsByDeathDate": "cumDailyNsoDeathsByDeathDate",
        "hospitalCases": "hospitalCases",
        "newCasesBySpecimenDate": "newCasesBySpecimenDate"
    }
    api = Cov19API(filters=area, structure=cases_and_deaths)

    data = api.get_json()

    d = data["data"]
    csv_file = pd.DataFrame(d)
    d = csv_file.to_csv("CovidData.csv", index=False)


