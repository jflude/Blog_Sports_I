from django.shortcuts import render, redirect, reverse, HttpResponse, HttpResponseRedirect
from .models import Post
from django.views.generic import ListView, DetailView, View
from apps.memberships.models import UserMembership, Membership, Subscription
from apps.daily_pick.models import DailyPick

class PostListView(ListView):
    model = Post


class PostDetailView(View):
    #model = Post
    def get (self, request, slug, *args, **kwargs):
        post_qs = Post.objects.filter(slug = slug)
        if post_qs.exists():
            post = post_qs.first()

        user_membership = UserMembership.objects.filter(user = request.user).first()
        user_membership_type = user_membership.membership.membership_type
        print(user_membership_type)
        post_allowed_mem_types = post.allowed_memberships.all()
        print(post_allowed_mem_types)
        context = {
            'object':None
        }

        if post_allowed_mem_types.filter(membership_type = user_membership_type).exists():
            context = {
                'object':post
            }


        return render(request, 'posts/post_detail.html', context)
