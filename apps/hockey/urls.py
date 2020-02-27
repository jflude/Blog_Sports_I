from django.urls import path, re_path

from . views import(hockey_index, show_hockey_odds)

app_name = "hockey"

urlpatterns = [
    path( '', hockey_index , name = "schedule"),
    re_path(r'^show_hockey_odds/(?P<id>\d+)$', show_hockey_odds, name="show_hockey_odds"),

]
