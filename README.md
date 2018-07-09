# destiny-flavor-text-generator

This is a bot which generates item descriptions for Destiny using Markov Chains. The main bot script was written for Reddit

It has scripts included for scraping the data and generating Markov models from it, so it's easy to implement them in anything. It currently scrapes only the weapon data. 

## Setup

The scripts need Python 3.6 to run, and you need to following installed too:

* markovify
* BeautifulSoup4

If you're using _bot.py_ to deploy your own Reddit Bot, you'd need a custom _praw.ini_ file with the following information:

```
[bot_name]
client_id=
client_secret=
username=
password=
user_agent=
```

## Getting the model set up

To set up the model, you need to:

1. Run `python3 wft_crawler.py` to scrape the data from DestinyTracker and store it.
2. Run `python3 create_json_mode.py` to make a JSON Markov model from the collected data.

## Running the bot

Run `python3 bot.py` to get the bot running.

The bot currently runs until stopped, and sleeps for the required minutes when it gets the posting limit exception from Reddit. 