import json, requests
from pprint import pprint
import django
from apps.college_hoops.models import *
import sqlite3
from django.utils import timezone
import os
from dotenv import load_dotenv
...
load_dotenv()


API_BASE = "https://jsonodds.com/api/"
API_KEY = os.getenv("API_KEY")


#DEFAULT_HEADER = {'JsonOdds-API-Key': API_KEY}
DEFAULT_HEADER = {'x-api-key': API_KEY}
ENDPOINT_SCHEDULE="odds/{}"
ENDPOINT_ODDTYPE = "oddtype/{}"
ENDPOINT_ODDS_BYGAMES = "odds/bygames"
ENDPOINT_RESULTS_BYLEAGUE = "results/{}"
ENDPOINTS_RESULTS_GETBYEVENTID = "results/getbyeventid/{}"



def get_data(url):
    response = requests.get(url, headers=DEFAULT_HEADER)
    return json.loads(response.text)

def post_data(url, payload):
    response = requests.post(url, headers=DEFAULT_HEADER, json = payload)
    return json.loads(response.text)


def get_schedule(sport):
    return get_data(API_BASE + ENDPOINT_SCHEDULE.format(sport))


def post_odds(game_id, sport, oddtype):
    payload= {'GameIDs': [game_id], 'Sport': sport, 'OddType':oddtype}
    print("I'm in post_odds!!")
    return post_data(API_BASE + ENDPOINT_ODDS_BYGAMES , payload)

def get_results_byid(game_id):
    return get_data(API_BASE + ENDPOINTS_RESULTS_GETBYEVENTID.format(game_id))

def get_results_sport(sport):
    return get_data(API_BASE + ENDPOINT_RESULTS_BYLEAGUE.format(sport))

def get_results_oddtype(oddtype):
    return get_data(API_BASE + ENDPOINT_ODDTYPE.format(oddtype))

def print_sport(sport):
    for schedule in get_schedule(sport):
        schedule_ncaab = ScheduleNCAAB()
        schedule_ncaab.api_id_key = schedule['ID']
        schedule_ncaab.away_rot = int(schedule['AwayROT'])
        schedule_ncaab.away_team = schedule['AwayTeam']
        schedule_ncaab.home_rot = int(schedule['HomeROT'])
        schedule_ncaab.home_team = schedule['HomeTeam']
        schedule_ncaab.match_time = schedule['MatchTime']
        schedule_ncaab.save()
        for odds in schedule['Odds']:
            #print('type odds for event_id ')
            #print(odds['EventID'])
            odds_list = post_odds(odds['EventID'], sport, odds['OddType'])
            #print('this oddslist is a dictionary')
            #print(type(odds_list))
            print(odds_list)
            for item in odds_list:

                for event_odd in item['Odds']:
                    #print("HELLO"*50)
                    #print('ID:', event_odd['ID'])
                    #print('EventID:', event_odd['EventID'])
                    #print('SiteID:', event_odd['SiteID'])
                    #print('MoneyLineAway:', event_odd['MoneyLineAway'])
                    #print('MoneyLineHome:', event_odd['MoneyLineHome'])
                    #print('OddType:', event_odd['OddType'])
                    #print('OverLine:', event_odd['OverLine'])
                    #print('PointSpreadAway:', event_odd['PointSpreadAway'])
                    #print('PointSpreadAwayLine:', event_odd['PointSpreadAwayLine'])
                    #print('PointSpreadHome:', event_odd['PointSpreadHome'])
                    #print('PointSpreadHomeLine:', event_odd['PointSpreadHomeLine'])
                    #print('TotalNumber:', event_odd['TotalNumber'])
                    #print('UnderLine:', event_odd['UnderLine'])
                    #print('LastUpdated:', event_odd['LastUpdated'])

                    game_odd = OddsNCAAB()
                    game_odd.drawline = event_odd['DrawLine']
                    game_odd.entity_id = event_odd['ID']
                    game_odd.api_event_key = event_odd['EventID']
                    game_odd.money_line_home = int(event_odd['MoneyLineHome'])
                    game_odd.money_line_away = int(event_odd['MoneyLineAway'])
                    game_odd.odd_type = (event_odd['OddType'])
                    game_odd.over_line = int(event_odd['OverLine'])
                    game_odd.under_line = int(event_odd['UnderLine'])
                    game_odd.point_spread_away =  float(event_odd['PointSpreadAway'])
                    game_odd.point_spread_away_line =  int(event_odd['PointSpreadAwayLine'])
                    game_odd.point_spread_home = float(event_odd['PointSpreadHome'])
                    game_odd.point_spread_home_line = int(event_odd['PointSpreadHomeLine'])
                    game_odd.site_id = int(event_odd['SiteID'])
                    game_odd.total_number = float(event_odd['TotalNumber'])
                    game_odd.last_updated = (event_odd['LastUpdated'])
                    game_odd.schedule = schedule_ncaab
                    game_odd.save()

                print(":-)" *80)

print_sport('NCAAB')
#pprint(get_schedule("NCAAB"))
