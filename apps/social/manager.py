from django.db import models


class FollowRequestManager(models.Manager):
    def send_request_to(self, target_profile, current_profile):
        follow = self.create(current_profile=current_profile, target_profile=target_profile)
        follow.save()

    def accept_request(self, follow_request_id):
        follow_request = self.get(id=follow_request_id)
        follow_request.accepted = True
        follow_request.save()

    def get_follow_requests(self, profile):
        return self.filter(accepted=False, target_profile=profile)

    def delete_follow_request(self, follow_request_id):
        self.get(id=follow_request_id).delete()


class ProfileManager(models.Manager):
    def followers_list(self, profile_id):
        profile = super().get(pk=profile_id)
        followers_id_list = [pro.current_profile.id for pro in profile.get_followers()]
        return super().filter(pk__in=followers_id_list)

    def followings_list(self, profile_id):
        profile = super().get(pk=profile_id)
        following_id_list = [pro.target_profile.id for pro in profile.get_following()]
        return super().filter(pk__in=following_id_list)

    def likes_list(self, user):
        profile = super().get(user=user)
        posts = profile.posts.all()
        likes = []
        for post in posts:
            for like in post.likes.all():
                likes.append(like)
        return likes

    def comments_list(self, user):
        profile = super().get(user=user)
        posts = profile.posts.all()
        comments = []
        for post in posts:
            for comment in post.comments.all():
                comments.append(comment)
        return comments


class PostManager(models.Manager):
    def posts_count(self):
        return super().filter(is_deleted=False)

    def all(self):
        return super().filter(is_deleted=False)
