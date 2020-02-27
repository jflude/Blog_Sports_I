from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse
from django.views.generic import ListView
from .models import Membership, UserMembership, Subscription
from apps.daily_pick.models import DailyPick
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime
import stripe
from django.contrib import auth
from django.contrib.auth.models import User


def get_user_membership(request):
    user_membership_qs = UserMembership.objects.filter(user = request.user)
    print("*" *50)
    if user_membership_qs.exists():
        return user_membership_qs.first()
    return None

def get_user_subscription(request):
    user_subscription_qs = Subscription.objects.filter(
        user_membership = get_user_membership(request))
    if user_subscription_qs.exists():
        user_subscription = user_subscription_qs.first()
        return user_subscription
    return None

def get_selected_membership(request):
    membership_type = request.session['selected_membership_type']
    selected_membership_qs = Membership.objects.filter(
        membership_type = membership_type)
    if selected_membership_qs.exists():
        return selected_membership_qs.first()
    return None

def get_daily_pick(request):
    daily_pick_qs = DailyPick.objects.all()
    print(daily_pick_qs)
    if daily_pick_qs.exists():
        daily_pick = daily_pick_qs.first()
        #print(daily_pick)
    context = {
            'object':daily_pick
    }
    #print(context)
    return(context)



class MembershipSelectView(ListView):
    model = Membership

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        current_membership = get_user_membership(self.request)
        print(current_membership)
        context['current_membership'] = str(current_membership.membership)
        return context

    def post(self, request, **kwargs):
        selected_membership_type = request.POST.get('membership_type')
        user_membership = get_user_membership(request)
        user_subscription = get_user_subscription(request)

        selected_membership_qs = Membership.objects.filter(
            membership_type = selected_membership_type)
        if selected_membership_qs.exists():
            selected_membership = selected_membership_qs.first()


        if user_membership.membership == selected_membership:
            if user_subscription is not None:
                messages.info(request, "You already have this membership.")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        #assign to session
        request.session['selected_membership_type'] = selected_membership.membership_type

        return HttpResponseRedirect(reverse('memberships:payment'))

def PaymentView(request):
    user_membership = get_user_membership(request)
    selected_membership = get_selected_membership(request)
    publishKey = settings.STRIPE_PUBLISHABLE_KEY
    if request.method == "POST":
        try:
            token = request.POST['stripeToken']
            customer = stripe.Customer.retrieve(user_membership.stripe_customer_id)
            customer.source = token # 4242424242424242
            customer.save()
            print("Saved HowdyDoody")

            subscription = stripe.Subscription.create(
                customer= user_membership.stripe_customer_id,
                items=[
                {
                    'plan': selected_membership.stripe_plan_id,
                },
            ],
            #source = token
            #expand=['latest_invoice.payment_intent'],
            )
            print(token)
            return redirect(reverse('memberships:update-transactions',
                        kwargs={
                                'subscription_id': subscription.id
                            }))

        except stripe.error.CardError as e:
            messages.info(request, "Your card has been declined!")


    context = {
    'publishKey': publishKey,
    'selected_membership': selected_membership
    }

    return render(request, "memberships/membership_payment.html", context)

def updateTransactions(request, subscription_id):
    user_membership = get_user_membership(request)
    selected_membership = get_selected_membership(request)
    user_membership.membership = selected_membership
    user_membership.save()

    sub, created = Subscription.objects.get_or_create(user_membership = user_membership)
    sub.stripe_subscription_id = subscription_id
    sub.active = True
    sub.save()
    try:
        del request.session['selected_membership_type']
    except:
        pass

    messages.info(request, "Successfully created {} membership".format(selected_membership))
    return redirect(reverse('memberships:select'))
    #return redirect('memberships/')

@login_required
def profile_view(request):
    user_membership = get_user_membership(request)
    user_subscription = get_user_subscription(request)
    daily_pick_content = get_daily_pick(request)
    context = {
        'user_membership': user_membership,
        'user_subscription': user_subscription,
        'daily_pick_content': daily_pick_content
    }
    #print(context)

    return render(request, "memberships/profile.html", context)

@login_required
def cancelSubscription(request):
    user_sub = get_user_subscription(request)
    user_membership = get_user_membership(request)

    if user_sub.active is False:
        messages.info(request, "You dont have an active membership")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    sub = stripe.Subscription.retrieve(user_sub.stripe_subscription_id)
    sub.delete()

    user_sub.active = False
    user_sub.save()

    free_membership = Membership.objects.get(membership_type = 'Free')
    user_membership = get_user_membership(request)
    user_membership.membership = free_membership
    user_membership.save()


    messages.info(
        request, "Successfully cancelled membership. We have sent an email")
    # sending an email here

    return redirect(reverse('memberships:select'))
