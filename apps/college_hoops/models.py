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
            return ScheduleNCAAB.objects.get(api_id_key=api_id_key.lower())
        except:
            return ScheduleNCAAB.objects.create(api_id_key.lower(),away_team,home_team,match_time)

class ScheduleNCAAB(models.Model):
    api_id_key=models.CharField(max_length=255)
    away_rot=models.IntegerField()
    away_team=models.CharField(max_length=25)
    home_rot=models.IntegerField()
    home_team=models.CharField(max_length=25)
    match_time=models.DateTimeField(blank = False)

class OddsNCAAB(models.Model):
    draw_line = models.IntegerField(null=True)
    entity_id = models.CharField(max_length = 255)
    schedule = models.ForeignKey(ScheduleNCAAB, related_name = 'odds', null= True, blank=True,  on_delete = models.CASCADE)
    last_updated=models.DateTimeField(blank=False)
    money_line_away=models.IntegerField()
    money_line_home=models.IntegerField()
    odd_type=models.CharField(max_length=25)
    over_line=models.IntegerField()
    point_spread_away=models.DecimalField(decimal_places=3,max_digits=7)
    point_spread_away_line=models.IntegerField()
    point_spread_home=models.DecimalField(decimal_places=3,max_digits=7)
    point_spread_home_line=models.IntegerField()
    site_id = models.IntegerField()
    total_number=models.DecimalField(decimal_places=3,max_digits=7)
    under_line=models.IntegerField()
