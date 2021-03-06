from django.urls import path
from . views import(
    PostListView,
    PostDetailView
)

app_name = 'posts'

urlpatterns = [
    path('', PostListView.as_view(), name = 'list'),
    path('<slug>', PostDetailView.as_view(), name = 'detail'),
]
