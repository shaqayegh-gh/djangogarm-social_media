from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic.base import View
from apps.social.models import User
from apps.social.models.profile import Post
from .common_views import get_currentuser_profile


class UserList(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        object_list = User.objects.exclude(pk=request.session.get('user_id'))  # list of other users
        return render(request, 'social/user_list.html', {'object_list': object_list})

    def post(self, request):  # search for a user by post method
        username = self.request.POST.get('username')
        results = User.objects.filter(username=username)  # result of search
        return render(request, 'social/user_list.html', {'search_results': results})


class ExplorerPosts(LoginRequiredMixin, View):
    def get(self, request):
        users_list = User.objects.exclude(pk=request.session.get('user_id'))  # list of other users
        posts = Post.objects.exclude(
            profile=get_currentuser_profile(request))  # show all posts excluding the user's post
        return render(request, 'social/explorer.html', {"posts": posts,"users_list":users_list})

    def post(self,request):
        users_list = User.objects.exclude(pk=request.session.get('user_id'))  # list of other users
        posts = Post.objects.exclude(
            profile=get_currentuser_profile(request))  # show all posts excluding the user's post
        username = self.request.POST.get('search')
        results = User.objects.filter(username=username)  # result of search
        return render(request, 'social/explorer.html', {"posts": posts, "users_list": users_list,'search_results': results})