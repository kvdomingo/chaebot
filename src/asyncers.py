from .models import *
from . import Session


async def sta_get_alias(group, member):
    sess = Session()
    mem = sess.query(Member)
        .filter(Member.group.has(name=group.lower()))
        .filter(Member.stage_name==member.capitalize())
        .first()
    aliases = mem.aliases.all()
    aliases = [alias.alias for alias in aliases]
    sess.close()
    return f"Aliases for {group.upper()} {member.capitalize()}: `{', '.join(aliases)}`"


async def sta_add_alias(group, member, aliases):
    sess = Session()
    mem = sess.query(Member)
        .filter(Member.group.has(name=group.lower()))
        .filter(Member.stage_name==member.capitalize())
        .first()
    for alias in aliases:
        obj = Alias(alias=alias, member_id=mem.id)
        sess.add(obj)
    sess.commit()
    alias = 'aliases' if len(aliases) > 1 else 'alias'
    aliases = ', '.join(aliases)
    sess.close()
    return f"Created {alias} `{aliases}` for `{member.capitalize()}`"
