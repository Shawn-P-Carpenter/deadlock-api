import requests
from dateutil.parser import isoparse
from base_urls import BaseUrl

def getLatestPatchTime():
    latest_patch = []
    latest_patch_time = 0

    patch_day_response = requests.get(BaseUrl.BASE_API + "/v1/patches")
    if(patch_day_response.ok):
        latest_patch = patch_day_response.json()[0]
        latest_patch_time = int(isoparse(latest_patch["pub_date"]).timestamp())
        return latest_patch_time
    else:
        return -1
    
def getAllTimeHeroStats(hero_id):
    hero_stat_data = requests.get(BaseUrl.BASE_API + "/v1/analytics/hero-stats")
    if(hero_stat_data.ok):
        all_hero_stat_json = hero_stat_data.json()
        for entry in all_hero_stat_json:
            if(entry["hero_id"] == hero_id):
                hero_stats = entry
    else:
            return None
    return hero_stats
    
def getHeroStats(hero_id, latest_patch_time):
    hero_stat_data = requests.get(BaseUrl.BASE_API + "/v1/analytics/hero-stats?min_unix_timestamp=" + str(latest_patch_time))
    if(hero_stat_data.ok):
        all_hero_stat_json = hero_stat_data.json()
        for entry in all_hero_stat_json:
            if(entry["hero_id"] == hero_id):
                hero_stats = entry
    else:
            return None
    return hero_stats

def getAllHeroStats(latest_patch_time):
    hero_stat_data = requests.get(BaseUrl.BASE_API + "/v1/analytics/hero-stats?min_unix_timestamp=" + str(latest_patch_time))
    if(hero_stat_data.ok):
        return hero_stat_data.json()
    else:
            return None

def get_items_sorted_by_hero(hero_id, latest_patch_time, reversed_sort, number_to_return):
    top_five_win_rates = {}
    item_win_rate_dict = {}
    items_by_hero = requests.get(BaseUrl.BASE_API + "/v1/analytics/item-stats?hero_ids=" + str(hero_id) + "&min_unix_timestamp=" + str(latest_patch_time)).json()
    
    for item in items_by_hero:
        # Calculate the win rate for each item and add it to an unsorted dictionary
        item_win_rate = (item["wins"])/(item["wins"] + item["losses"])
        item_win_rate_dict[item["item_id"]] = item_win_rate

    # Sort the dictionary based on the win rate value in descending order
    sorted_top_five_items = {k: v for k,v in sorted(item_win_rate_dict.items(), key=lambda item: item[1], reverse=reversed_sort)}

    top_five_item_ids = list(sorted_top_five_items.keys())[:number_to_return]

    for item in top_five_item_ids:
        # For each of the top five win rate items, get its name from the assets api and add that to our final returned dictionary
        item_asset = requests.get(BaseUrl.BASE_ASSETS + "/v2/items/" + str(item)).json()
        item_name = item_asset["name"]
        
        print(item)

        top_five_win_rates[item_name] = sorted_top_five_items.get(item)


    return top_five_win_rates

def get_items_sorted_by_hero_and_item_type(hero_id, latest_patch_time, reversed_sort, number_to_return, item_type):
    top_five_win_rates = {}
    item_win_rate_dict = {}
    items_by_hero = requests.get(BaseUrl.BASE_API + "/v1/analytics/item-stats?hero_ids=" + str(hero_id) + "&min_unix_timestamp=" + str(latest_patch_time)).json()
    
    for item in items_by_hero:
        # Calculate the win rate for each item and add it to an unsorted dictionary
        item_win_rate = (item["wins"])/(item["wins"] + item["losses"])
        item_win_rate_dict[item["item_id"]] = item_win_rate

    # Sort the dictionary based on the win rate value in descending order
    sorted_top_five_items = {k: v for k,v in sorted(item_win_rate_dict.items(), key=lambda item: item[1], reverse=reversed_sort)}

    top_five_item_ids = list(sorted_top_five_items.keys())

    number_added_to_list = 0
    for item in top_five_item_ids:
        # For each item in order of the sorted win rates, if the item is the correct type add it to our returned list and increment the iterator
        item_asset = requests.get(BaseUrl.BASE_ASSETS + "/v2/items/" + str(item)).json()
        item_name = item_asset["name"]
        curr_item_type = item_asset["item_slot_type"]

        if(curr_item_type.lower() == item_type):
            top_five_win_rates[item_name] = sorted_top_five_items.get(item)
            number_added_to_list = number_added_to_list + 1


        if(number_added_to_list >= number_to_return):
             break


    return top_five_win_rates