# Covid-19 Dashboard
## Introduction
This is a Python project that creates a locally-hosted web page detailing up-to-date Covid-19 data and news articles. It can also schedule automatic updates to the data and articles
## Pre-requisites

 - Python 3.9.7 or above
 - The Built-In Modules:
	 - Sched
	 - Time
	 - Logging
	 - Typing
	 - Json
 - A NewsAPI API key (create an account [here](https://newsapi.org))
 
 ## Installation
 To install the dashboard run the following command in a command prompt:
 
    pip install covid-dashboard-jis206

You will also need the flask module as well as the uk_covid-19 module, pytest and requests.
You will need to run these commands as well:

	pip install flask
	pip install uk-covid19
	pip install pytest
	pip install requests

## Getting Started
You will need to copy your API key into the `config.json` replacing the `<Insert API key here>` text.
Then to run the program, navigate to your installation location in the command prompt and run the command

	python main.py
Once the programme is running, head to this [webpage](http://127.0.0.1:5000/index) for your dashboard.
### Covid Data
In the centre of the screen, you should see the infection rate in Exeter as well as the infection rate, number of hospital cases and number of deaths across England. The areas of these data sources can be adjusted in the config file.
### Updates
You can schedule an update with the form in the bottom middle of the screen. Fill in when you want the update to occur, what you want the update to be called, then select what it should update and whether it should update every day or not.

If this has been done correctly, once you have hit the 'Submit' button, a toast should pop-up in the top-left hand corner detailing the update. How many toasts appear on the screen can be changed in the config file.

If you would like to cancel the update, just hit the 'x' on the toast and the update will no longer occur
### News Articles
On the right hand side of the screen, you can see news articles that relate to Covid from the UK. You can see the name of each article, its source and a brief description of its contents. Furthermore, it contains a hyperlink to the full article if you would like to see more.

You can also hide the news articles with the 'x' in the top-right corner of each article. This will cause the article to not be displayed even after an update.
### Config File
- api-key: Where your key should go. This should be obtained from [here](https://newsapi.org)
- localArea: The region for which local data will be taken from. Most towns/cities are acceptable
- localAreaType: This is how large the area is. Options are `ltla, utla, region, nhsRegion`. For more information, see the [UK-covid-19 API documentation](https://coronavirus.data.gov.uk/details/developers-guide/main-api#filters-authorised_filter_metrics)
- nationalArea: The region where the national data is retrieved. Must be a country within the UK or the UK itself
- nationalAreaType: What region this is. Options are `nation, overview`. For more information, see the [UK-covid-19 API documentation](https://coronavirus.data.gov.uk/details/developers-guide/main-api#filters-authorised_filter_metrics)
- newsTerms: These are the terms queried by the News API. Any article containing at least one of these words will be identified. Each item to be searched must be separated by a space. To search for phrases, the phrase must be surrounded by quotes (").
- newsCountry: The country that the articles found originate from. By default, the UK. The options for countries are `ae ar at au be bg br ca ch cn co cu cz de eg fr gb gr hk hu id ie il in it jp kr lt lv ma mx my ng nl no nz ph pl pt ro rs ru sa se sg si sk th tr tw ua us ve za`.
- articlesShown: The number of articles on the screen at any given time
- updatesShown: The number of updates on the screen at any given time
## Details
- Released under the MIT License into the public domain
- Written by Jack Souster