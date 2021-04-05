from django.contrib.auth import views
from django.urls import path, include
from .views.activities_views import LikesList, CommentsList, FollowRequestList
from .views.homepage_views import FollowingsPostsList
from .views.newpost_views import NewPostView
from .views.profile_views import ProfileView, PostDetail, OthersProfile, ProfileUpdate, PostUpdate
from .views.register_views import SignUpView, login_user, logout_user, login_redirct,sms_verify
from .views.explorer_views import ExplorerPosts, UserList

urlpatterns = [
    # password urls
    path('password_change/', views.PasswordChangeView.as_view(template_name='social/change_password.html',
        success_url='/djangogram/index/profile/'),name='password_change'),
    # path('password_change/', views.PasswordChangeView.as_view(),name='password_change'),
    path('password_change/done/', views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password_reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # registration urls
    path('', login_redirct, name='login_redirect'),
    path('logout/', logout_user, name='user_logout'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', login_user, name='user_login'),
    path('sms-verification/',sms_verify,name='sms_verify'),

    # homepage urls
    path('index/', include([
        path('home/', FollowingsPostsList.as_view(), name='home'),
        path('new_post/', NewPostView.as_view(), name='new_post'),
        path('users_list/', UserList.as_view(), name='users_list'),
        path('explorer/', ExplorerPosts.as_view(), name='explorer'),
        path('profile/', include([
            path('', ProfileView.as_view(), name='profile'),
            # path('<username>/update/',ProfileUpdate.as_view(),name='profile_update'),
            path('<username>/update/', include([
                path('', ProfileUpdate.as_view(), name='profile_update'),
                # path('password_change/', views.PasswordChangeView.as_view(template_name='social/change_password.html'),
                #      name='password_change'),
            ])),
            path('post/<post_id>/update/', PostUpdate.as_view(), name='post_update'),
            path('<username>/', OthersProfile.as_view(), name='others_profile'),
            path('post_detail/<post_id>/', PostDetail.as_view(), name='post_detail'),

        ])),
        path('likes/', LikesList.as_view(), name='likes'),
        path('comments/', CommentsList.as_view(), name='comments'),
        path('requests/', FollowRequestList.as_view(), name='requests'),

    ])),

]
