import re
import random
from asgiref.sync import sync_to_async
from ..models import Group


@sync_to_async
def group_name_matcher(name):
    group_names = {
        group.name: [alias.alias for alias in group.aliases.all()]
        for group in Group.objects.all()
    }
    for key, value in group_names.items():
        search_params = [
            re.search(name, key, re.I),
            re.search(key, name, re.I),
        ]
        search_params.extend([re.search(name, val, re.I) for val in value])
        search_params.extend([re.search(val, name, re.I) for val in value])
        if any(search_params):
            print(f'Group query matched: {key}.')
            return key
    group = random.choice(list(group_names.keys()))
    print(f'No group query matched, choosing random.')
    return group
