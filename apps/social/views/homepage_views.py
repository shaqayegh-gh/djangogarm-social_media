from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic.base import View

from apps.social.models import User, Profile
from .common_views import get_comment, get_like,get_currentuser_profile


# class HomeView(LoginRequiredMixin, View):
#     """this is a view of index which return user's information"""
#
#     def get(self, request):
#         if request.session.has_key("user_id"):
#             user_id = request.session.get("user_id")
#             context = User.objects.get(pk=user_id)  # get all user's information based on user session
#             return render(request, "social/home.html", {'user': context})
#         return redirect('user_login')

# def index(request):
#     if request.method == 'GET':
#         profile = get_currentuser_profile(request)
#         return render(request,'social/index.html',{"current_profile":profile})


class FollowingsPostsList(LoginRequiredMixin, View):
    """this view return following's information and their last post will be shown in home template"""

    def get(self, request):
        user_id = request.session.get("user_id")  # get the user's session user_id
        followings = Profile.objects.get(user__pk=user_id).get_following()
        if followings != None:
            return render(request, 'social/home.html', {"followings": followings})
        else:
            return render(request, 'social/home.html', {})

    def post(self, request):
        user_id = request.session.get('user_id')  # get the user's session user_id
        followings = Profile.objects.get(user__pk=user_id).get_following()
        # like check
        if get_like(request):
            return render(request, 'social/home.html', {"followings": followings})

        # comment check
        if get_comment(request):
            return render(request, 'social/home.html', {"followings": followings})

        return render(request, 'social/home.html', {"followings": followings})
