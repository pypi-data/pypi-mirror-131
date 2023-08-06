"""
Handles covid information from both a static CSV and the UK Covid-19 API
"""

#Imports
import sched
import time
import logging
from typing import Tuple
from flask import request
from uk_covid19 import Cov19API
from time_handler import seconds_from_now_to_hhmm

FORMAT='%(levelname)s:%(asctime)s:%(message)s'
logging.basicConfig(format=FORMAT,filename='sys.log', encoding='utf-8', level=logging.INFO)

data_scheduler = sched.scheduler(time.time, time.sleep)
data_scheduler.run(blocking=False)
updates = {}
covid_data = {}

def parse_csv_data(csv_filename: str) -> list:
    """
    Takes the name of a file and returns a list of each individual line in the file
    """
    with open(csv_filename, "r", encoding="UTF-8") as file:
        logging.info("Opening %s", csv_filename)
        lines = file.readlines()
        lines = [i.strip('\n') for i in lines]
        print(lines[1])
    return list(lines)

def process_covid_csv_data(covid_csv_data: list) -> Tuple:
    """
    Takes a list containing Covid data as formatted by parse_csv_data and returns 3 values:
    Number of cases in the last 7 days taking data not including the
    most recent since that is not up to date
    The current number of hospital cases
    And the cumulative deaths because of covid
    """

    #Splitting the csv into individual values
    broken_stats=[i.split(",") for i in covid_csv_data]

    #getting the current hospital cases
    current_hospital_cases = int(broken_stats[1][5])

    #Gets cumulative deaths from covid
    i=0
    first_value = False
    while not first_value:
        i+=1
        if broken_stats[i][4] != "":
            first_value = True
    total_deaths = int(broken_stats[i][4])

    #Getting the number of cases in the last 7 days with accurate data
    i=1
    first_value=False
    while not first_value:
        if broken_stats[i][6] != "":
            first_value = True
        i+=1
    last7days_cases=0
    for j in range(7):
        last7days_cases += int(broken_stats[i+j][6])

    return last7days_cases, current_hospital_cases, total_deaths


def covid_API_request(location: str ="Exeter",
    location_type: str ="ltla", local: str =True) -> dict:
    """
    Uses the live UK covid data API to return up-to-date covid data
    based at the location and location type
    """
    area_filter=[f'areaType={location_type}', f'areaName={location}']
    if local:
        cases_and_deaths = {
            "date":"date",
            "newCasesByPublishDate":"newCasesByPublishDate",
        }
    else:
        cases_and_deaths = {
            "date":"date",
            "newCasesByPublishDate":"newCasesByPublishDate",
            "hospitalCases":"hospitalCases",
            "cumDeaths28DaysByDeathDate":"cumDeaths28DaysByDeathDate"
        }

    logging.info("Requesting covid data from %s", location)
    api = Cov19API(filters=area_filter, structure=cases_and_deaths)
    data = api.get_json()
    return data

def process_covid_api_data(covid_api_data: dict, local: bool =True) -> Tuple:
    """
    Takes local covid data in the form of a JSON dictionary and returns the 7-day infection rate

    day: Today's date which de-iterates to 7 days ago
    day_count: How many days have been done iterates up to 7 in order to limit data received
    infection_rate: how many new cases in the last 7 days
    daystr: The date in string format for easy comparison with the API
    """

    infection_rate=0
    i=0
    while covid_api_data["data"][i]["newCasesByPublishDate"] is None:
        i+=1
    for j in range(i, i+7):
        infection_rate += covid_api_data["data"][j]["newCasesByPublishDate"]

    if local:
        return infection_rate
    else:
        i=0
        while covid_api_data["data"][i]["hospitalCases"] is None:
            i+=1
        hospital_cases = covid_api_data["data"][i]["hospitalCases"]
        j=0
        while covid_api_data["data"][j]["cumDeaths28DaysByDeathDate"] is None:
            print(covid_api_data["data"][j]["cumDeaths28DaysByDeathDate"])
            j+=1
        deaths_total = covid_api_data["data"][j]["cumDeaths28DaysByDeathDate"]
        return infection_rate, hospital_cases, deaths_total


def full_api_gather(local: str ="Exeter",
    local_type: str ="ltla", nation: str ="England", nation_type: str ="nation") -> dict:
    """
    Gets both local and national covid data stats and compiles it into a dictionary

    Bundled into 1 function for the scheduler to execute
    """
    local_data = process_covid_api_data(covid_API_request(local, local_type, True))
    national_data = process_covid_api_data(covid_API_request(nation, nation_type, False), False)
    all_data = {
        "local_7day":local_data,
        "local_area":local,
        "local_type":local_type,
        "national_7day":national_data[0],
        "hospital_cases":national_data[1],
        "deaths_total":national_data[2],
        "national_area":nation,
        "national_type":nation_type
    }

    return all_data

def update(update_interval: int, update_name: str, time_occur: str, repeat: bool = True) -> None:
    """
    Updates the covid data and creates a new update in the same interval if requested

    Executed by the scheduler
    """
    global covid_data
    local = covid_data["local_area"]
    local_type = covid_data["local_type"]
    nation = covid_data["national_area"]
    nation_type = covid_data["national_type"]
    covid_data = full_api_gather(local, local_type, nation, nation_type)
    updates.pop(update_name)
    if repeat:
        updates[update_name] = [data_scheduler.enter(
            update_interval, 1, update, (update_interval, update_name, time_occur, repeat)),
            repeat, time_occur]

def schedule_covid_updates(update_interval: int, update_name: str, repeat: bool = False) -> None:
    """
    Schedules the automatic covid updates

    """
    time_occur = seconds_from_now_to_hhmm(update_interval)
    for name in updates.keys():
        if name == update_name:
            logging.error("Update with that name already exists. Terminating this update attempt")
            return

    updates[update_name] = [data_scheduler.enter(
        update_interval, 1, update, (update_interval, update_name, time_occur, repeat)),
        repeat, time_occur]
    logging.info("data update scheduled")
    logging.info(updates)

def delete_update(update_name: str) -> None:
    """
    Deletes the update with the assigned name from the scheduler event
    """
    data_scheduler.cancel(updates.pop(update_name))
