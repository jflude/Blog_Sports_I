from django.urls import path, re_path

from . views import(hoop_index, show_hoop_odds)

app_name = "pro_hoops"

urlpatterns = [
    path( '', hoop_index , name = "nba_schedule"),
    re_path(r'^show_hoop_odds/(?P<id>\d+)$', show_hoop_odds, name="show_hoop_odds"),

]
