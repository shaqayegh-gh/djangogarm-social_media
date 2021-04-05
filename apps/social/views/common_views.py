from django.shortcuts import redirect

from apps.social.models import User
from apps.social.models.profile import Post, Profile, FollowRequest, Like, Comment


# find the user's profile based on session
def get_currentuser_profile(request):
    user_id = request.session.get('user_id')  # get the user's session user_id
    profile = Profile.objects.get(user__pk=user_id)  # find the user's profile
    return profile


# get the user based on session
def get_currentuser(request):
    if request.session.has_key("user_id"):
        user_id = request.session.get('user_id')  # get the user's session user_id
        user = User.objects.get(pk=user_id)
        return user
    return redirect('user_login')


def get_comment(request):
    # comment check
    post_id = request.POST.get('comment_post_id')  # define which post was liked
    content = request.POST.get("comment_text")
    if post_id:
        if content:
            user = get_currentuser(request)
            post = Post.objects.get(pk=post_id)
            Comment.objects.create(user=user,
                                   post=post,
                                   content=content)  # create an instance of comment class after click comment's button
            return True
        return False
    return False


def get_like(request):
    # like check
    post_id = request.POST.get('like_post_id')  # define which post was liked
    if post_id:
        user = get_currentuser(request)
        post = Post.objects.get(pk=post_id)
        try:
            Like.objects.create(user=user, post=post)  # create an instance of Like class after click like's button
        except:
            Like.objects.filter(user=user, post=post).delete()  # clear like when user click like's button again
        return True
    return False


def get_follow_request(request, target_profile):
    current_profile = get_currentuser_profile(request)
    # follow check
    follow = request.POST.get('follow')  # get the follow value from template
    if follow:
        try:  # make a follow request from current_profile to target_profile
            FollowRequest.objects.send_request_to(target_profile=target_profile, current_profile=current_profile)
        except:  # clear follow when user click follow button again
            FollowRequest.objects.get(target_profile=target_profile, current_profile=current_profile).delete()
        return True
    return False


def delete_comment(request):
    try:
        comment_id = request.POST.get('comment_id')
        comment = Comment.objects.get(pk=comment_id)
        comment.is_active = False  # deactivate the comment
        comment.save()
        return True
    except:
        return False


def delete_post(request):
    post_id = request.POST.get('deleted_post_id')
    if post_id:
        Post.objects.get(pk=post_id).delete()  # delete post object
        return True
    else:
        return False


def show_follower_list(request, profile):
    current_profile = get_currentuser_profile(request)
    if current_profile in Profile.objects.followers_list(profile_id=profile.id) or current_profile == profile:
        return Profile.objects.followers_list(profile_id=profile.id)
    else:
        return []


def show_following_list(request, profile):
    current_profile = get_currentuser_profile(request)
    if current_profile in Profile.objects.followers_list(profile_id=profile.id) or current_profile == profile:
        return Profile.objects.followings_list(profile_id=profile.id)
    else:
        return []


from kavenegar import *
from Djangogram.settings import Kavenegar_API
from random import randint

def get_random_otp():
    return randint(1000,9999)

def send_otp(mobile,otp):
    mobile = [mobile,]
    try:
        api = KavenegarAPI(Kavenegar_API)
        params = {
            'sender': '1000596446',  # optional
            'receptor': mobile,  # multiple mobile number, split by comma
            'message': 'Your code is {}'.format(otp),
        }
        response = api.sms_send(params)
        print('OTP : ', otp)
        print(response)
    except APIException as e:
        print(e)
    except HTTPException as e:
        print(e)
