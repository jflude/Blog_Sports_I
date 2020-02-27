from django.contrib import admin

# Register your models here.
from .models import DailyPick


class DailyPickAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'status','created_on')
    list_filter = ("status",)
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(DailyPick, DailyPickAdmin)
