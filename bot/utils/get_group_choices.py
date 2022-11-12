from discord.app_commands import Choice

from bot.api.internal import Api


def get_group_choices():
    return [Choice(name=g["name"], value=g["name"]) for g in (Api.sync_groups() or [])]
