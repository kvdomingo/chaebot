from django.db.models import CharField
from django.db.models.functions import Lower

from .group import Group, GroupAlias
from .member import Member, MemberAlias
from .twitter import TwitterMediaSource, TwitterMediaSubscribedChannel
from .vlive import VliveSubscribedChannel

CharField.register_lookup(Lower)
