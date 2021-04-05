from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import UpdateView
from django.views.generic.base import View

from apps.social.models.profile import Post, Profile
from .common_views import get_comment, get_like, get_follow_request, get_currentuser_profile, delete_comment, \
    delete_post, show_follower_list, show_following_list


class ProfileView(LoginRequiredMixin, View):
    """this is a view of the account's profile for the authenticated user"""

    def get(self, request, *args, **kwargs):
        profile = get_currentuser_profile(request)
        user_posts = profile.posts.all()  # get all user's posts

        following_list = show_following_list(request, profile=profile)
        follower_list = show_follower_list(request, profile=profile)

        return render(request, 'social/profile.html',
                      {'user_posts': user_posts, 'profile': profile, 'following_list': following_list,
                       'follower_list': follower_list})

    def post(self, request):
        profile = get_currentuser_profile(request)
        user_posts = profile.posts.all()
        # like check
        if get_like(request):
            return render(request, 'social/profile.html',
                          {'user_posts': user_posts, 'profile': profile, 'message': 'liked'})
        # comment check
        if get_comment(request):
            return render(request, 'social/profile.html',
                          {'user_posts': user_posts, 'profile': profile, 'message': 'sent'})
        # delete comment
        if delete_comment(request):
            return render(request, 'social/profile.html', {'user_posts': user_posts, 'profile': profile})

        # delete post
        if delete_post(request):
            return render(request, 'social/profile.html', {'user_posts': user_posts, 'profile': profile})

        return render(request, 'social/profile.html',
                      {'user_posts': user_posts, 'profile': profile})


class OthersProfile(LoginRequiredMixin, View):
    """this is a view of the other user's profile for the authenticated user"""

    def get(self, request, username):
        profile = Profile.objects.get(user__username=username)
        # check if the user has permission to see the another user's posts
        if get_currentuser_profile(request) in Profile.objects.followers_list(profile_id=profile.id):
            user_posts = profile.posts.all()
        else:
            user_posts = []

        following_list = show_following_list(request, profile=profile)
        follower_list = show_follower_list(request, profile=profile)

        return render(request, 'social/others_profile.html',
                      {'user_posts': user_posts, 'profile': profile, 'following_list': following_list,
                       'follower_list': follower_list})

    def post(self, request, username):
        profile = Profile.objects.get(user__username=username)  # get the profile of the user based on username
        if get_currentuser_profile(request) in Profile.objects.followers_list(profile_id=profile.id):
            user_posts = profile.posts.all()
        else:
            user_posts = []

        # follow check
        if get_follow_request(request, target_profile=profile):
            return render(request, 'social/others_profile.html',
                          {'user_posts': user_posts, 'profile': profile, 'message': 'followed'})
        # like check
        if get_like(request):
            return render(request, 'social/others_profile.html',
                          {'user_posts': user_posts, 'profile': profile, 'message': 'liked'})
        # comment check
        if get_comment(request):
            return render(request, 'social/others_profile.html',
                          {'user_posts': user_posts, 'profile': profile, 'cmt_message': 'comment sent'})

        return render(request, 'social/others_profile.html', {'user_posts': user_posts, 'profile': profile})


class PostDetail(LoginRequiredMixin, View):
    """this view return the post details"""

    def get(self, request, post_id):
        profile = get_currentuser_profile(request)
        post = Post.objects.get(pk=post_id)
        return render(request, 'social/post_detail.html', {"post": post, 'profile': profile})

    def post(self, request, post_id):  # for deleting the comments
        profile = get_currentuser_profile(request)
        post = Post.objects.get(pk=post_id)

        # like check
        if get_like(request):
            return render(request, 'social/post_detail.html',
                          {"post": post, 'profile': profile, 'message': 'liked'})
        # comment check
        if get_comment(request):
            return render(request, 'social/post_detail.html',
                          {"post": post, 'profile': profile, 'cmt_message': 'comment sent'})

        if delete_comment(request):
            return render(request, 'social/post_detail.html', {"post": post, 'profile': profile})

        return render(request, 'social/post_detail.html', {"post": post, 'profile': profile})


class ProfileUpdate(LoginRequiredMixin, UpdateView):
    """this view is for updating profile data"""
    model = Profile
    fields = ['bio', 'profile_photo', 'gender', 'country', 'address', "birthday"]
    template_name = 'social/profile_update.html'

    def get_object(self, queryset=None):
        """the detail view ProfileUpdate must be called with either an object pk or a slug in the URLconf.
        changing the get_object methode help to call the view with username"""
        return self.model.objects.get(user__username=self.kwargs.get("username"))

    def get_success_url(self):
        return reverse('profile')


class PostUpdate(LoginRequiredMixin, UpdateView):
    """this view is for updating a post's caption"""
    model = Post
    fields = ['caption']
    template_name = 'social/post_update.html'

    def get_object(self, queryset=None):
        return self.model.objects.get(pk=self.kwargs.get('post_id'))

    def get_success_url(self):
        return reverse('profile')
