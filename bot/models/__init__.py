from django.db.models import CharField
from django.db.models.functions import Lower

from .group import Group, GroupAlias
from .member import Member, MemberAlias
from .schedule import ScheduleSubscriber
from .twitter import TwitterMediaSource, TwitterMediaSubscribedChannel

CharField.register_lookup(Lower)
