"""
The core module of the program.

Handles Flask integration and brings in data from covid_data_handler
and news from covid_news_handling as well as scheduling events
"""
import json
import logging
from flask import Flask
from flask import request
from flask import render_template
from time_handler import hhmm_to_seconds_from_now
import covid_data_handler as cdh
import covid_news_handling as cnh

FORMAT='%(levelname)s:%(asctime)s:%(message)s'
logging.basicConfig(format=FORMAT,filename='sys.log', encoding='utf-8', level=logging.INFO)

with open('config.json', 'r', encoding="UTF-8") as f:
    config = json.load(f)
    local_area = config["localArea"]
    local_area_type = config["localAreaType"]
    national_area = config["nationalArea"]
    national_area_type = config["nationalAreaType"]
    news_terms = config["newsTerms"]
    articles_shown=config["articlesShown"]
    updates_shown=config["updatesShown"]

app = Flask(__name__)
blacklist = []

updates = []
news_articles = []

@app.route("/index")
def index() -> None:
    """
    Decorator function that creates and determines what is show on the website.

    Makes sure that events are scheduled and articles are deleted.
    """
    #Delete Article
    deleted_article = request.args.get("notif")
    if deleted_article:
        logging.info("Article to be blacklisted: %s", deleted_article)
        cnh.add_to_blacklist(deleted_article)

    #Delete Update
    deleted_update = request.args.get("update_item")
    if deleted_update:
        logging.info("Update to be cancelled: %s", deleted_update)
        global updates
        for update in updates:
            if deleted_update==update["title"]:
                is_news = update["news"]
                is_data = update["data"]
                if is_news:
                    logging.info("Update is news update")
                    cdh.delete_update(deleted_update)
                if is_data:
                    logging.info("Update is data update")
                    cnh.delete_update(deleted_update)

    #schedule update
    data_update = request.args.get("covid-data")
    news_update = request.args.get("news")
    if data_update or news_update:
        name = request.args.get("two")
        logging.info("Update requested: %s", name)
        time_of_update = request.args.get("update")
        repeat = bool(request.args.get("repeat"))
        if time_of_update:
            time_till_update = hhmm_to_seconds_from_now(time_of_update)
            if data_update:
                logging.info("Update is data update")
                cdh.schedule_covid_updates(time_till_update, name, repeat)
            if news_update:
                logging.info("Update is news update")
                cnh.schedule_news_update(time_till_update, name, repeat)

    updates = all_updates()

    logging.info("Rendering page")
    return render_template("index.html",
                        title = "Coronavirus Dashboard",
                        favicon = "static/images/SARS-CoV-2.png",
                        image = "SARS-CoV-2.png",
                        location = cdh.covid_data["local_area"],
                        local_7day_infections = cdh.covid_data["local_7day"],
                        nation_location = cdh.covid_data["national_area"],
                        national_7day_infections = cdh.covid_data["national_7day"],
                        hospital_cases =
                            f"National hospital cases: {cdh.covid_data['hospital_cases']}",
                        deaths_total = f"National total deaths: {cdh.covid_data['deaths_total']}",
                        news_articles = news_articles[0:articles_shown],
                        updates=updates[0:updates_shown]
                        )

def all_updates() -> list:
    """
    Compiles the lists of updates of data and news and combines them into 1 list
    which stores more information for the toasts. If an update on each list
    shares a name, it merges then into a single update on this list
    """
    unique_updates = {}
    shared_updates = {}
    combined_updates = []
    data_updates = cdh.updates
    news_updates = cnh.updates
    for data_key, data_value in data_updates.items():
        if data_key not in news_updates.keys():
            unique_updates[data_key] = data_value
        else:
            shared_updates[data_key] = data_value

    for news_key, news_value in news_updates.items():
        is_data = True if news_key in shared_updates.keys() else False
        update_detailed = {
            "title":news_key,
            "news":True,
            "data":False,
            "news_event": news_value[0],
            "repeat":news_value[1],
            "time":news_value[2]
        }
        if is_data:
            update_detailed["data"] = True
            for data_key,data_value in shared_updates.items():
                if data_key==news_key:
                    update_detailed["data_event"] = data_value[0]
        combined_updates.append(update_detailed)

    for data_key,data_value in unique_updates.items():
        update_detailed = {
            "title":data_key,
            "news":False,
            "data":True,
            "data_event": data_value[0],
            "repeat":data_value[1],
            "time":data_value[2]
        }
        combined_updates.append(update_detailed)

    for update in combined_updates:
        content=""
        if update["data"]:
            content+="Data Update, "
        if update["news"]:
            content+="News Update, "
        if update["repeat"]:
            content+="Repeated daily "
        content+=f"at {update['time']}"
        update["content"]=content

    return combined_updates

if __name__ == '__main__':
    cdh.covid_data = cdh.full_api_gather(
        local_area, local_area_type, national_area, national_area_type)
    news_articles = cnh.parse_news_API(cnh.news_API_request(news_terms))
    logging.info("Begin running")
    app.run()
    