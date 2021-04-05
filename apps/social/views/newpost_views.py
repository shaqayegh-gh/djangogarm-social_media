from django.shortcuts import render, redirect
from django.views.generic.base import View

from apps.social.forms import NewPostForm
from apps.social.models import Profile


class NewPostView(View):

    def get(self, request):
        new_post_form = NewPostForm()
        return render(request, 'social/new_post.html', {"form": new_post_form})

    def post(self, request):
        new_post_form = NewPostForm(request.POST, request.FILES)
        if new_post_form.is_valid():
            profile = Profile.objects.get(user__pk=request.session.get('user_id'))
            new_post_form.instance.profile = profile  # add to profile field the user's profile
            new_post_form.save()
            return redirect('profile')
        return render(request, 'social/new_post.html', {'message': 'something went wrong, try again'})
