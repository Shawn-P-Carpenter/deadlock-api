from flask import Flask, request
import requests
from dateutil.parser import isoparse
import utils
from base_urls import BaseUrl
import numpy


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

@app.route("/hero-items/current-patch/<hero_name>", methods=["GET"])
def get_hero_items_in_current_patch_by_hero_name(hero_name):
    sort_order = request.args.get('sort')
    if(sort_order == None):
        return "You need to provide a sort as either top, or bottom", 400
    sort_order = sort_order.lower()
    if(sort_order != "top" and sort_order != "bottom"):
        return "You need to provide the sort as either TOP or BOTTOM"
    sort_order = (sort_order == "top")

    latest_patch_time = utils.getLatestPatchTime()
    if(latest_patch_time == -1):
        return "An error ocurred while getting the latest patch time", 500
    
    hero_asset = requests.get(BaseUrl.BASE_ASSETS + "/v2/heroes/by-name/" + hero_name)
    if(hero_asset.ok):
        hero_id = hero_asset.json()["id"]
    else:
        return "An error ocurred", 500
    
    return utils.get_items_sorted_by_hero(hero_id=hero_id, latest_patch_time=latest_patch_time, reversed_sort=sort_order, number_to_return=5)
    
    

@app.route("/hero-items/current-patch/<hero_name>/<item_type>", methods=["GET"])
def get_top_hero_items_in_current_patch_by_hero_name_and_item_type(hero_name, item_type):
    sort_order = request.args.get('sort')
    if(sort_order == None):
        return "You need to provide a sort as either top, or bottom", 400
    sort_order = sort_order.lower()
    if(sort_order != "top" and sort_order != "bottom"):
        return "You need to provide the sort as either TOP or BOTTOM"
    sort_order = (sort_order == "top")


    item_type = item_type.lower()
    if(item_type != "spirit" and item_type != "vitality" and item_type != "weapon"):
        return "Please enter a valid item type in your request, valid types are SPIRIT, WEAPON, AND VITALITY", 400

    latest_patch_time = utils.getLatestPatchTime()
    if(latest_patch_time == -1):
        return "An error ocurred while getting the latest patch time", 500
    
    hero_asset = requests.get(BaseUrl.BASE_ASSETS + "/v2/heroes/by-name/" + hero_name)
    if(hero_asset.ok):
        hero_id = hero_asset.json()["id"]
    else:
        return "An error ocurred", 500
    
    return utils.get_items_sorted_by_hero_and_item_type(hero_id=hero_id, latest_patch_time=latest_patch_time, reversed_sort=sort_order, number_to_return=5, item_type=item_type)
