from flask import Flask
import requests
from dateutil.parser import isoparse
import utils
from base_urls import BaseUrl



app = Flask(__name__)

@app.route("/hero-stat/<hero_name>", methods=['GET'])
def get_stat_by_hero_name_all_time(hero_name):
    hero_stats = []

    hero_asset = requests.get(BaseUrl.BASE_ASSETS + "/v2/heroes/by-name/" + hero_name)
    if(hero_asset.ok):
        hero_id = hero_asset.json()["id"]
    else:
        return "An error ocurred", 500
    hero_stats = utils.getAllTimeHeroStats(hero_id=hero_id)
    hero_stats["name"] = hero_asset.json()["name"]
    
    return hero_stats

@app.route("/hero-stat/current-patch/<hero_name>", methods=['GET'])
def get_stat_by_hero_name_current_patch(hero_name):
    latest_patch_time = utils.getLatestPatchTime()
    if(latest_patch_time == -1):
        return "An error ocurred while getting the latest patch time", 500

    hero_asset = requests.get(BaseUrl.BASE_ASSETS + "/v2/heroes/by-name/" + hero_name)
    if(hero_asset.ok):
        hero_id = hero_asset.json()["id"]
    else:
        return "An error ocurred", 500
    hero_stats = utils.getHeroStats(hero_id=hero_id, latest_patch_time=latest_patch_time)

    hero_stats["name"] = hero_asset.json()["name"]
    
    return hero_stats


@app.route("/hero-win-rate/current-patch/<hero_name>", methods=["GET"])
def get_hero_win_rate_by_hero_name_for_current_patch(hero_name):
    latest_patch_time = utils.getLatestPatchTime()
    if(latest_patch_time == -1):
        return "An error ocurred while getting the latest patch time", 500

    hero_asset = requests.get(BaseUrl.BASE_ASSETS + "/v2/heroes/by-name/" + hero_name)
    if(hero_asset.ok):
        hero_id = hero_asset.json()["id"]
    else:
        return "An error ocurred", 500
    
    hero_stats = utils.getHeroStats(hero_id=hero_id, latest_patch_time=latest_patch_time)
    if(hero_stats != None):
        hero_wins = hero_stats["wins"]
        hero_losses = hero_stats["losses"]
        hero_win_rate = (hero_wins/(hero_wins + hero_losses)) * 100

        split_win_rate = str(hero_win_rate).split(".")
        string_hero_win_rate = split_win_rate[0] + "." + split_win_rate[1][:2]
        
        return string_hero_win_rate
    else:
        return "An error ocurred while getting the hero stats", 500

@app.route("/hero-win-rate/current-patch/all", methods=["GET"])
def get_all_hero_win_rates_current_patch():
    all_hero_win_rates = {}

    latest_patch_time = utils.getLatestPatchTime()
    if(latest_patch_time == -1):
        return "An error ocurred while getting the latest patch time", 500
    
    all_hero_stat_json = utils.getAllHeroStats(latest_patch_time=latest_patch_time)
    for hero in all_hero_stat_json:
        hero_name = requests.get(BaseUrl.BASE_ASSETS + "/v2/heroes/" + str(hero["hero_id"])).json()["name"]
        hero_win_rate = (hero["wins"]/(hero["losses"] + hero["wins"])) * 100
        
        all_hero_win_rates[hero_name] = hero_win_rate
    
    return all_hero_win_rates
