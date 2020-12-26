from django.urls import path
from . import views


urlpatterns = [
    path('group/<str:group_query>', views.GroupApi.as_view()),
    path('groups', views.GroupApi.as_view()),
    path('member/<str:member_query>', views.MemberApi.as_view()),
    path('members', views.MemberApi.as_view()),
]
