from django.urls import path, re_path

from . views import(ncaab_hoop_index, show_ncaab_hoop_odds)

app_name = "college_hoops"

urlpatterns = [
    path( '', ncaab_hoop_index , name = "ncaab_schedule"),
    re_path(r'^show_ncaab_hoop_odds/(?P<id>\d+)$', show_ncaab_hoop_odds, name="show_ncaab_hoop_odds"),

]
