# deadlock-api
This a Flask REST API written to get statistics about alve's upcoming game deadlock

Currently this uses data obtained from deadlock-api.com

A full list of hero and item names can be found at https://deadlock.wiki/

# Routes

**/hero-stat/<hero_name>**

GET - gets the heroes all time statistics

*example*: /hero-stat/infernus

**/hero-stat/current-patch/<hero_name>**

GET - gets the heroes stats for the current patch

*Path Parameters*
- hero_name: The name of the hero you are querying for

*example*: /hero-stat/current-patch/shiv

**/hero-win-rate/current-patch/<hero_name>**

GET - gets the heroes win rate for the current patch

*Path Parameters*
- hero_name: The name of the hero you are querying for

*example*: /hero-win-rate/current-patch/lash

**/hero-win-rate/current-patch/all**

GET - gets a list of all heroes and their win rates in the current patch

**/hero-items/current-patch/<hero_name>?sort=SORT**

GET - gets either the top or bottom five items in the current patch for a given hero based on win rate

*Path Parameters*
- hero_name: The name of the hero you are querying for

*Query Parameters*
- sort: Either top or bottom, for which subset of items you want to view(the top win rate or the bottom win rate)

*example*: /hero-items/current-patch/wraith?sort=top

*example*: /hero-items/current-patch/seven?sort=bottom

**/hero-items/current-patch/<hero_name>/<item_type>?sort=SORT**

GET - gets either the top or bottom five items in the current patch for a given hero and item type based on win rate

*Path Parameters*
- hero_name: The name of the hero you are querying for
- item_type: The type of item you want to query for(Spirit, Weapon, or Vitality)

*Query Parameters*
- sort: Either top or bottom, for which subset of items you want to view(the top win rate or the bottom win rate)

*example*: /hero-items/current-patch/yamato/spirit?sort=top

*example*: /hero-items/current-patch/vyper/weapon?sort=bottom

*example*: /hero-items/current-patch/dynamo/vitality?sort=top

## Quick-Start/Install Instructions ##

Currently this is a work in progress flask api and not hosted anywhere, so if you want to pull this down to take a look at it locally here are the instructions

1. clone the repo
2. This is currently running on python 3.9.7, but I believe anything above 3.7 should work fine
3. create a python venv, and activate it for ease of use https://docs.python.org/3/library/venv.html
4. pip install any missing packages, should need Flask, numpy, requests, and python-dateutil
5. run flask --app routes run --debug to start up the api, and then navigate to 127.0.0.1:5000 + any route to see the data returned

If when running the final command you get errors related to missing packages, you may have to pip install any I forgot to write down
