from django.urls import path, re_path

from . views import(baseball_index, show_baseball_odds)

app_name = "baseball"

urlpatterns = [
    path( '', baseball_index , name = "mlb_schedule"),
    re_path(r'^show_baseball_odds/(?P<id>\d+)$', show_baseball_odds, name="show_baseball_odds"),

]
