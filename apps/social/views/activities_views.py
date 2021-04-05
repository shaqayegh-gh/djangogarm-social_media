from django.shortcuts import render
from django.views.generic.base import View

from apps.social.models import Profile
from .common_views import get_currentuser, get_currentuser_profile
from ..models.profile import FollowRequest


class LikesList(View):
    def get(self, request):
        likes = Profile.objects.likes_list(user=get_currentuser(request))[:50]
        return render(request, 'social/like_activity.html', {"likes": likes})


class CommentsList(View):
    def get(self, request):
        comments = Profile.objects.comments_list(user=get_currentuser(request))[:50]
        return render(request, 'social/comment_activity.html', {"comments": comments})



class FollowRequestList(View):
    def get(self, request):
        follow_requests = FollowRequest.objects.get_follow_requests(profile=get_currentuser_profile(request))
        return render(request, 'social/follow_requests.html', {"follow_requests": follow_requests})

    def post(self, request):
        follow_requests = FollowRequest.objects.get_follow_requests(profile=get_currentuser_profile(request))
        accept_request = request.POST.get('accept_request')
        delete_request = request.POST.get('delete_request')
        if accept_request:
            FollowRequest.objects.accept_request(follow_request_id=accept_request)
            return render(request, 'social/follow_requests.html', {"follow_requests": follow_requests})
        elif delete_request:
            FollowRequest.objects.delete_follow_request(follow_request_id=delete_request)
            return render(request, 'social/follow_requests.html', {"follow_requests": follow_requests})
        return render(request, 'social/follow_requests.html', {"follow_requests": follow_requests})
