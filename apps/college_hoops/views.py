from django.shortcuts import render, reverse, redirect, HttpResponse
from . models import *
import requests
import json, ast
from django.contrib import messages
from django.http import JsonResponse
import time
from datetime import datetime
from datetime import date
from datetime import timedelta
from django.utils import timezone

# Create your views here.

def ncaab_hoop_index(request):
    # code below gets rid of "naive datetime warning but still does not solve timezone problem"
    today = timezone.now()
    tomorrow= today + timedelta(1)
######todays_sched filters expired games out of schedule########
    todays_sched = ScheduleNCAAB.objects.filter(match_time__date__gte=datetime.date(today))

    context={
        'schedule':ScheduleNCAAB.objects.all(),
        'odds':OddsNCAAB.objects.all(),
        'todays_sched': todays_sched,
    }
    # print context['todays_sched']
    schedules_filter = {}
    unique_schedules= []

#######This for loop filters games so games displayed in html are unique and not repeated####
    for schedules in todays_sched:
        key = schedules.api_id_key
        if key not in schedules_filter and len(key.strip()) > 0:
            schedules_filter[key] = True
            unique_schedules.append(schedules)

    context['schedule']=unique_schedules
    return render(request, 'college_hoops/ncaab_hoop_index.html', context)


def show_ncaab_hoop_odds(request,id):
    game=ScheduleNCAAB.objects.get(id=id)
    game_odds=OddsNCAAB.objects.filter(schedule_id= game.id)
    half_odds=OddsNCAAB.objects.filter()

    context = {
        'games': game,
        'game_odds': game_odds,
        'away_team':ScheduleNCAAB.objects.get(id=id),
        'home_team':ScheduleNCAAB.objects.get(id=id),
        'match_time':ScheduleNCAAB.objects.get(id=id),
    }

    return render(request, 'college_hoops/ncaab_hoop_odds.html', context)
