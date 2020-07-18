import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.ext.declarative import declarative_base

from .mixins import BaseMixin

Base = declarative_base()


class Group(BaseMixin, Base):
    __table_args__ = (sa.UniqueConstraint('name'), )

    name = sa.Column(sa.String(64))
    vlive_channel_code = sa.Column(sa.String(255))
    vlive_channel_seq = sa.Column(sa.BigInteger)
    vlive_last_seq = sa.Column(sa.BigInteger)
    members = orm.relationship('Member', back_populates='group')
    twitter_channels = orm.relationship('TwitterChannel', back_populates='group')
    vlive_channels = orm.relationship('VliveChannel', back_populates='group')

    def __repr__(self):
        return f"<Group {self.id}: {self.name.upper()}>"

    def __str__(self):
        return self.name.upper()


class Member(BaseMixin, Base):
    stage_name = sa.Column(sa.String(64))
    given_name = sa.Column(sa.String(64))
    family_name = sa.Column(sa.String(64))
    group_id = sa.Column(sa.Integer, sa.ForeignKey('group.id'))
    group = orm.relationship('Group', back_populates='members')
    aliases = orm.relationship('Alias', back_populates='member')
    twitter_accounts = orm.relationship('TwitterAccount', back_populates='member')

    def __repr__(self):
        return f"<Member {self.id}: {self.family_name.capitalize()} {self.stage_name.capitalize()}>"

    def __str__(self):
        return f"{self.stage_name.capitalize()} of {self.group.name.upper()}"


class Alias(BaseMixin, Base):
    alias = sa.Column(sa.String(64))
    member_id = sa.Column(sa.Integer, sa.ForeignKey('member.id'))
    member = orm.relationship('Member', back_populates='aliases')

    def __repr__(self):
        return f"<Alias {self.id}: {self.alias}>"

    def __str__(self):
        return f"{self.alias} ({str(self.member).capitalize()})"


class TwitterAccount(BaseMixin, Base):
    account_name = sa.Column(sa.String(255))
    last_tweet_id = sa.Column(sa.BigInteger)
    member_id = sa.Column(sa.Integer, sa.ForeignKey('member.id'))
    member = orm.relationship('Member', back_populates='twitter_accounts')

    def __repr__(self):
        return f"<Twitter account {self.id}: {self.account_name}>"

    def __str__(self):
        return f"{self.account_name} ({str(self.member).capitalize()})"


class TwitterChannel(BaseMixin, Base):
    __table_args__ = (sa.UniqueConstraint('channel_id'), )
    channel_id = sa.Column(sa.BigInteger)
    group_id = sa.Column(sa.Integer, sa.ForeignKey('group.id'))
    group = orm.relationship('Group', back_populates='twitter_channels')

    def __repr__(self):
        return f"<Twitter channel {self.channel_id}>"

    def __str__(self):
        return f"{self.channel_id} ({str(self.group)})"


class VliveChannel(BaseMixin, Base):
    channel_id = sa.Column(sa.BigInteger)
    group_id = sa.Column(sa.Integer, sa.ForeignKey('group.id'))
    group = orm.relationship('Group', back_populates='vlive_channels')

    def __repr__(self):
        return f"<VLIVE channel {self.channel_id}>"

    def __str__(self):
        return f"{self.channel_id} ({str(self.group)})"
