from django.urls import path
from . import views


urlpatterns = [
    path("group/<int:pk>/aliases", views.GroupAliasApi.as_view()),
    path("group/<int:pk>/members", views.GroupMembersApi.as_view()),
    path(
        "group/<int:pk>/twitterMediaSubscribedChannels",
        views.GroupTwitterSubscribedChannelsApi.as_view(),
    ),
    path(
        "group/<int:pk>/vliveSubscribedChannels",
        views.GroupVliveSubscribedChannelsApi.as_view(),
    ),
    path("group/<int:pk>", views.GroupApi.as_view()),
    path("groups", views.GroupApi.as_view()),
    path("member/<int:pk>/aliases", views.MemberAliasApi.as_view()),
    path("member/<int:pk>/twitterMediaSources", views.TwitterMediaSourceApi.as_view()),
    path("member/<int:pk>", views.MemberApi.as_view()),
    path("members", views.MemberApi.as_view()),
    path("twitterMediaSource/<int:pk>", views.TwitterMediaSourceApi.as_view()),
    path("twitterMediaSources", views.TwitterMediaSourceApi.as_view()),
    path(
        "twitterMediaSubscribedChannel/<int:pk>",
        views.TwitterMediaSubscribedChannelApi.as_view(),
    ),
    path(
        "twitterMediaSubscribedChannels",
        views.TwitterMediaSubscribedChannelApi.as_view(),
    ),
    path(
        "vliveSubscribedChannel/<int:channel_id>",
        views.VliveSubscribedChannelApi.as_view(),
    ),
    path("vliveSubscribedChannels", views.VliveSubscribedChannelApi.as_view()),
]
