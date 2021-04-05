# from mapbox_location_field.models import LocationField
from datetime import datetime

from django.db import models
from django_countries.fields import CountryField
from imagekit.models import ProcessedImageField
from pilkit.processors import ResizeToFit

from apps.social.common.validators import mobile_char_check
from apps.social.manager import FollowRequestManager, ProfileManager
from .user import User, BaseModel


class Profile(BaseModel):
    bio = models.TextField('Biography', max_length=300, blank=True, null=True)
    profile_photo = ProcessedImageField(verbose_name='Profile Photo', null=True, blank=True,
                                        upload_to="photos/",
                                        format="JPEG",
                                        options={"quality": 90},
                                        processors=[ResizeToFit(width=200, height=200)],
                                        )  # install Pillow
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthday = models.DateField('Birthday', blank=True, null=True)
    gender = models.CharField('Gender', max_length=1, choices=(('F', 'Female'), ('M', 'Male')), blank=True, null=True)
    address = models.CharField('Address', max_length=100, blank=True, null=True)
    country = CountryField('Country', blank=True, null=True)  # install django_countries
    # phone_number = models.CharField(
    #     'Phone number', blank=True, null=True,
    #     validators=[mobile_char_check], max_length=20,
    #     help_text='write your number like 989121133445')

    @classmethod
    def create_user_profile(cls, user):  # use in signup view; when a user signup,his profile will made automatically
        new_profile = cls.objects.create(user=user)
        new_profile.save()

    def get_following(self):  # get the followings list from FollowRequest class
        followings = FollowRequest.objects.filter(current_profile=self.id,accepted=True)
        return followings

    def get_followers(self):  # get the followers list from FollowRequest class
        followers = FollowRequest.objects.filter(target_profile=self.id,accepted=True)
        return followers

    def __str__(self):
        return f"{self.user.username}'s profile"

    objects = ProfileManager()


class FollowRequest(BaseModel):
    """current_profile is the profile which sends the follow request and target_profile
     receives the follow request. these two fields should be unique together handled in Meta class """

    current_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='current_user')
    target_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='target_user')
    date_created = models.DateTimeField(default=datetime.now())
    accepted = models.BooleanField(default=False)
    class Meta:
        unique_together = (("current_profile", "target_profile"),)
        ordering = ["-date_created"]

    objects = FollowRequestManager()


class Post(BaseModel):
    """Each post belongs to a profile that is a foreignkey in this model."""

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name="Created By", related_name="posts")
    caption = models.TextField('Caption', max_length=2000, blank=True, null=True)
    date_created = models.DateTimeField(default=datetime.now())
    # date_updated = models.DateTimeField(default=datetime.now())
    photo = ProcessedImageField(  # install django-imagekit
        upload_to="photos/",
        format="JPEG",
        options={"quality": 90},
        processors=[ResizeToFit(width=650, height=600)],
    )


    # location = LocationField(null=True,blank=True)

    @property
    def post_dn(self):  # return the duration of post
        time = self.date_created.replace(tzinfo=None)
        difference = datetime.now() - time
        if difference.total_seconds() < 3600:
            return 'A little while ago'
        elif 3600 <= difference.total_seconds() < 86400:
            if difference.total_seconds() // 3600 == 1:
                return f"{difference.total_seconds() // 3600} hour ago"
            else:
                return f"{difference.total_seconds() // 3600} hours ago"
        elif 86400 <= difference.total_seconds() and difference.days < 30:
            return f"{difference.days} days ago"
        elif 30 <= difference.days < 365:
            return difference.days // 30
        else:
            return f"{self.date_created.year}/{self.date_created.month}"

    def __str__(self):
        return f"{self.profile.user.username}'s Post on {self.date_created}"

    class Meta:
        ordering = ["-date_created"]

    def get_detail_absolute_url(self):
        return f'/accounts/post_detail/{self.id}/'


    @property  # return the number of likes for a post
    def likes_count(self):
        post = Post.objects.get(pk=self.id)
        return post.likes.all().count()

    @property
    def comments_count(self):  # return the number of comments for a post
        post = Post.objects.get(pk=self.id)
        return post.comments.filter(is_active=True).count()

    objects = ProfileManager()


class Like(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")  # the user who wants to like a post
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")  # the post which is liked
    date_created = models.DateTimeField(default=datetime.now())

    def __str__(self):
        return f"{self.user} Like"

    class Meta:
        unique_together = (("user", "post"),)  # the user can once likes e post
        ordering = ["-date_created"]


class Comment(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name="comments")  # the user who wants to give a comment
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")  # the post which is get a comment
    content = models.TextField(max_length=2000)
    date_created = models.DateTimeField(default=datetime.now())
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.content

    class Meta:
        ordering = ["-date_created"]
