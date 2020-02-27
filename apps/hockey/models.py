from django.db import models
from datetime import datetime
import re
from django.contrib import messages
from django.contrib.auth.models import User
from django.urls import reverse
from apps.memberships.models import Membership, UserMembership, Subscription

class ScheduleManager(models.Manager):
    def get_or_create(self, api_id_key,home_team,away_team, match_time):
        try:
            return ScheduleNHL.objects.get(api_id_key=api_id_key.lower())
        except:
            return ScheduleNHL.objects.create(api_id_key.lower(),away_team,home_team,match_time)

class ScheduleNHL(models.Model):
    api_id_key=models.CharField(max_length=255)
    away_rot=models.IntegerField()
    away_team=models.CharField(max_length=25)
    home_rot=models.IntegerField()
    home_team=models.CharField(max_length=25)
    match_time=models.DateTimeField(blank = False)

class OddsNHL(models.Model):
    entity_id = models.CharField(max_length = 255)
    schedule = models.ForeignKey(ScheduleNHL, related_name = 'odds', null= True, blank=True,  on_delete = models.CASCADE)
    money_line_away=models.IntegerField()
    money_line_home=models.IntegerField()
    odd_type=models.CharField(max_length=25)
    over_line=models.IntegerField()
    total_number=models.DecimalField(decimal_places=3,max_digits=5)
    under_line=models.IntegerField()
    point_spread_away=models.DecimalField(decimal_places=3,max_digits=5)
    point_spread_home=models.DecimalField(decimal_places=3,max_digits=5)
    point_spread_away_line=models.IntegerField()
    point_spread_home_line=models.IntegerField()
    draw_line = models.IntegerField(null=True)
    site_id = models.IntegerField()
    last_updated=models.DateTimeField(blank=False)

class BetSlip(models.Model):
    schedule_event = models.ForeignKey(ScheduleNHL, related_name = 'event', null= True, blank=True,  on_delete = models.CASCADE)
    event_odds = models.ForeignKey(OddsNHL, related_name = 'event_odds',  on_delete = models.CASCADE)
    user=models.ForeignKey(User, related_name="betslips" , on_delete = models.CASCADE )
    money_line_away=models.IntegerField()
    money_line_home=models.IntegerField()
    point_spread_away_line=models.IntegerField()
    point_spread_home_line=models.IntegerField()
    over_line=models.IntegerField()
    under_line=models.IntegerField()
    amount = models.IntegerField()
    remaining_amnt = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class BetTaker(models.Model):
    betslip = models.ForeignKey(BetSlip, related_name= "betslip_bettakers", on_delete = models.CASCADE)
    user=models.ForeignKey(User, related_name="user_bettakers", on_delete = models.CASCADE)
    schedule_event = models.ForeignKey(ScheduleNHL, related_name = 'bettaker_event', null= True, blank=False, on_delete = models.CASCADE)
    event_odds = models.ForeignKey(OddsNHL, related_name = 'bettaker_event_odds', on_delete = models.CASCADE)
    money_line_away=models.IntegerField()
    money_line_home=models.IntegerField()
    point_spread_away_line=models.IntegerField()
    point_spread_home_line=models.IntegerField()
    over_line=models.IntegerField()
    under_line=models.IntegerField()
    amount = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
