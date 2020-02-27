from django.shortcuts import render, redirect, reverse, HttpResponse, HttpResponseRedirect
from .models import DailyPick
from django.views.generic import ListView, DetailView, View
from apps.memberships.models import UserMembership, Membership, Subscription

class DailyPickListView(ListView):
    model = DailyPick

class DailyPickDetailView(View):

    def get (self, request, slug, *args, **kwargs):
        daily_pick_qs = DailyPick.objects.filter(slug = slug)
        print(daily_pick_qs)
        if daily_pick_qs.exists():
            daily_pick = daily_pick_qs.first()

        user_membership = UserMembership.objects.filter(user = request.user).first()
        user_membership_type = user_membership.membership.membership_type
        print(user_membership_type)
        daily_pick_allowed_mem_types = daily_pick.allowed_memberships.all()
        print(daily_pick_allowed_mem_types)
        context = {
            'object':None
        }

        if daily_pick_allowed_mem_types.filter(membership_type = user_membership_type).exists():
                context = {
                    'object':daily_pick
                }
        print(context)

        return render(request, 'daily_pick/dailypick_detail.html', context)
