from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter(trailing_slash=False)
router.register("scheduleSubscriberFromGuild", views.ScheduleSubscriberFromGuildView)
router.register("scheduleSubscribers", views.ScheduleSubscriberView)

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
    *router.urls,
]
