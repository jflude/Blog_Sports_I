from django.urls import path
from . views import(
    DailyPickListView,
    DailyPickDetailView
)

app_name = 'daily_pick'

urlpatterns = [
    path('', DailyPickListView.as_view(), name = 'picklist'),
    path('<slug>', DailyPickDetailView.as_view(), name = 'pickdetail'),
]
