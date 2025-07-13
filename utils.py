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
