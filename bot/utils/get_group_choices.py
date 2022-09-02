from discord.app_commands import Choice
from django.core.cache import cache


def get_group_choices():
    return [Choice(name=g["name"], value=g["name"]) for g in (cache.get("groups") or [])]
