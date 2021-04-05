from apps.social.models import Profile


def get_user_profile(request):
    user_id = request.session.get('user_id')  # get the user's session user_id
    profile = Profile.objects.get(user__pk=user_id)  # find the user's profile
    return profile