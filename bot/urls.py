from django.urls import path

from . import views

urlpatterns = [
    path("group/<int:pk>/aliases", views.GroupAliasView.as_view()),
    path("group/<int:pk>/members", views.GroupMembersView.as_view()),
    path("group/<int:pk>/twitterMediaSubscribedChannels", views.GroupTwitterSubscribedChannelsView.as_view()),
    path("group/<int:pk>", views.GroupView.as_view()),
    path("groups", views.GroupView.as_view()),
    path("member/<int:pk>/aliases", views.MemberAliasView.as_view()),
    path("member/<int:pk>/twitterMediaSources", views.TwitterMediaSourceView.as_view()),
    path("member/<int:pk>", views.MemberView.as_view()),
    path("members", views.MemberView.as_view()),
    path("twitterMediaSource/<int:pk>", views.TwitterMediaSourceView.as_view()),
    path("twitterMediaSources", views.TwitterMediaSourceView.as_view()),
    path("twitterMediaSubscribedChannel/<int:pk>", views.TwitterMediaSubscribedChannelView.as_view()),
    path("twitterMediaSubscribedChannels", views.TwitterMediaSubscribedChannelView.as_view()),
    path("scheduleSubscriberFromGuild/<int:guild_id>", views.ScheduleSubscriberFromGuildView.as_view()),
    path("scheduleSubscribers/<int:pk>", views.ScheduleSubscriberView.as_view()),
    path("scheduleSubscribers", views.ScheduleSubscriberView.as_view()),
]
