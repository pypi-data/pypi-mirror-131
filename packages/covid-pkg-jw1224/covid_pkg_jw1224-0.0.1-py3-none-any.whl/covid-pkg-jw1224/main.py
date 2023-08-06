'''
This module creates the web page for the Covid Dashboard to be displayed on.
It also handles the making of schedules to let the server know when to update the data.
'''

import sched
import schedule
import time
import covid_data_handler
import covid_news_handling
import time_calculation
import logging

from flask import Flask
from flask import render_template
from flask import request
from covid_data_handler import *
from covid_news_handling import *
from time_calculation import *

app = Flask(__name__)

logging.basicConfig(filename='sys.log', encoding='utf-8')
s = sched.scheduler(time.time, time.sleep)
location_nation, location_type_national = 'England', 'nation'
location_local, location_type_local = 'Exeter', 'ltla'

news = []
update = []
current_jobs=[]
def add_news() -> None:
    '''Sends a request to update the list of news dictionaries to be displayed'''
    new_articles = update_news()
    for article in new_articles:
        news.append(article) 
    
    repeat_sched()
    
def get_covid_data() -> None:
    '''Retrieves and updates the Covid statistics for the html page'''
    covid_API_request(location_nation, location_type_national)
    data = parse_csv_data('CovidData.csv')
    last7days_cases_national, current_hospital_cases_national, total_deaths_national = process_covid_csv_data(data)
    covid_API_request(location_local, location_type_local)
    data = parse_csv_data('CovidData.csv')
    last7days_cases_local, current_hospital_cases_local, total_deaths_local = process_covid_csv_data(data)
    
    repeat_sched()
    return last7days_cases_local, last7days_cases_national, current_hospital_cases_national, total_deaths_national
    
def repeat_sched():
    '''Redifines any schedule which is requested to be repeated'''
    for u in update:
        check_time = u['time']
        equal = time_passed(check_time)
        if equal:
            if u['repeat']:
                new_update_interval = u['time']
                new_update_name = u['title']
                if u['type'] == 'covid':
                    schedule_covid_updates(new_update_interval, new_update_name)
                elif u['type'] == 'news':
                    schedule_news_updates(new_update_interval, new_update_name)
        
def schedule_covid_updates(update_interval, update_name):
    '''Initiates a scheduled job for a Covid data update'''
    copy = 0
    sched_name = str(update_interval)+str(update_name)
    for sched in update:
        if sched['title'] == update_name:
            copy = 1
            break
        else:
            copy = 0 
    repeat = request.args.get('repeat')
    if repeat:
        repeat_content = "will repeat"
    else:
        repeat_content = "will not repeat"
    
    if copy == 0:
        schedule_time = time_difference(update_interval)
         
        sched_name = s.enter(schedule_time,1,get_covid_data)
        update.append({"title": update_name, "content": f"Covid update at: {update_interval}.\nThis update {repeat_content}", "name": sched_name, "time": update_interval, "repeat": repeat, "type": 'covid'})
def schedule_news_updates(update_interval, update_name):
    '''Initiates a scheduled job for a News update'''
    copy = 0
    sched_name = str(update_interval)+str(update_name)
    for sched in update:
        if sched['title'] == update_name:
            copy = 1
            break
        else:
            copy = 0
    repeat = request.args.get('repeat')
    if repeat:
        repeat_content = "will repeat"
    else:
        repeat_content = "will not repeat"
    
    if copy == 0:
        schedule_time = time_difference(update_interval)
        sched_name = s.enter(schedule_time,1,add_news)
        update.append({"title": update_name, "content": f"News update at: {update_interval}.\nThis update {repeat_content}", "name": sched_name, "time": update_interval, "repeat": repeat, "type": 'news'})


    
@app.route('/index')
def hello():
    '''Runs the html and creates the web page to display it on'''
    current_jobs = s.queue
    text_field = request.args.get('two')
    if text_field:        
        if request.args.get('covid-data'):
            schedule_covid_updates(request.args.get('update'), request.args.get('two'))
        elif request.args.get('news'):
            schedule_news_updates(request.args.get('update'), request.args.get('two'))
    remove_news = request.args.get('notif')
    if remove_news:
        for n in range(len(news)):
            if news[n]['title'] == remove_news:
                del news[n]
                break               
    remove_update = request.args.get('update_item')
    if remove_update:
        for u in range(len(update)):
            if update[u]['title'] == remove_update:
                for job in current_jobs:
                    if job == update[u]['name']:
                        s.cancel(job)
                        break
                del update[u]
                break
    schedule.run_pending()
    s.run(blocking=False) 
    return render_template('index.html', 
    title='Daily update',
    location= location_local,
    local_7day_infections= local_7day,
    nation_location= location_nation,
    national_7day_infections= national_7day,
    hospital_cases= f"Current hospital cases: {national_hopsital}",
    deaths_total= f"Total deaths: {national_deaths}",
    news_articles= news,
    updates = update)

    

if __name__ == '__main__':
    local_7day, national_7day, national_hopsital, national_deaths = get_covid_data()        
    add_news()

    app.run()