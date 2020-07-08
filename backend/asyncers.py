from dotenv import load_dotenv
from asgiref.sync import sync_to_async
from backend.models import *


load_dotenv()


@sync_to_async
def sta_get_alias(group, member):
    mem = Group.objects.get(name=group.lower()).members.filter(stage_name=member.capitalize()).first()
    aliases = mem.aliases.all()
    aliases = [alias.alias for alias in aliases]
    return f"Aliases for {group.upper()} {member.capitalize()}: `{', '.join(aliases)}`"


@sync_to_async
def sta_add_alias(group, member, aliases):
    mem = Group.objects.get(name=group.lower()).members.filter(stage_name=member.capitalize()).first()
    for alias in aliases:
        obj = Alias.objects.create(alias=alias, member=mem)
    alias = 'aliases' if len(aliases) > 1 else 'alias'
    aliases = ', '.join(aliases)
    return f"Created {alias} `{aliases}` for `{member.capitalize()}`"
