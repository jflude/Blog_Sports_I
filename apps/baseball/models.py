from django.db import models
from datetime import datetime
import re
from django.contrib import messages
from django.contrib.auth.models import User
from django.urls import reverse
from apps.memberships.models import Membership, UserMembership, Subscription

class ScheduleManager(models.Manager):
    def get_or_create(self, away_pitcher,away_team,details, home_pitcher,home_team, api_id_key, match_time):
        try:
            return ScheduleMLB.objects.get(api_id_key=api_id_key.lower())
        except:
            return ScheduleMLB.objects.create(away_pitcher,away_team,details,home_pitcher,home_team,api_id_key.lower(),match_time)

class ScheduleMLB(models.Model):
    away_pitcher=models.CharField(max_length=25)
    away_rot=models.IntegerField()
    away_team=models.CharField(max_length=25)
    details=models.CharField(max_length = 25)
    home_pitcher=models.CharField(max_length=25)
    home_rot=models.IntegerField()
    home_team=models.CharField(max_length=25)
    api_id_key=models.CharField(max_length=255)
    match_time=models.DateTimeField(blank = False)

class OddsMLB(models.Model):
    entity_id = models.CharField(max_length = 255)
    schedule = models.ForeignKey(ScheduleMLB, related_name='odds', null = True, blank = False, on_delete = models.CASCADE)
    last_updated=models.DateTimeField(blank=False)
    money_line_away=models.IntegerField()
    money_line_home=models.IntegerField()
    odd_type=models.CharField(max_length=25)
    over_line=models.IntegerField()
    point_spread_away=models.DecimalField(decimal_places=3,max_digits=7)
    point_spread_away_line=models.IntegerField()
    point_spread_home=models.DecimalField(decimal_places=3,max_digits=7)
    point_spread_home_line=models.IntegerField()
    total_number=models.DecimalField(decimal_places=3,max_digits=7)
    under_line=models.IntegerField()
