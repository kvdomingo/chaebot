import os, sys
sys.path.append('.')

from dotenv import load_dotenv
load_dotenv()

import django
django.setup()

import json
from django.conf import settings
from backend.models import *


def update_group():
    with open(os.path.join(settings.BASE_DIR, 'backend/update_models/group.json'), 'r') as f:
        data = json.load(f)
    for dat in data:
        obj, created = Group.objects.update_or_create(pk=dat['pk'], defaults=dict(**dat['fields']))
        status = 'Created' if created else 'Updated'
        print(f'{status} entry for group {str(obj)}')

def update_member():
    with open(os.path.join(settings.BASE_DIR, 'backend/update_models/member.json'), 'r') as f:
        data = json.load(f)
    for dat in data:
        group = Group.objects.get(pk=dat['fields']['group'])
        dat['fields']['group'] = group
        obj, created = Member.objects.update_or_create(pk=dat['pk'], defaults=dict(**dat['fields']))
        status = 'Created' if created else 'Updated'
        print(f'{status} entry for member {str(obj)}')

def update_alias():
    with open(os.path.join(settings.BASE_DIR, 'backend/update_models/alias.json'), 'r') as f:
        data = json.load(f)
    for dat in data:
        member = Member.objects.get(pk=dat['fields']['member'])
        dat['fields']['member'] = member
        obj, created = Alias.objects.update_or_create(pk=dat['pk'], defaults=dict(**dat['fields']))
        status = 'Created' if created else 'Updated'
        print(f'{status} entry for alias {str(obj)}')

def update_account():
    with open(os.path.join(settings.BASE_DIR, 'backend/update_models/account.json'), 'r') as f:
        data = json.load(f)
    for dat in data:
        member = Member.objects.get(pk=dat['fields']['member'])
        dat['fields']['member'] = member
        obj, created = TwitterAccount.objects.update_or_create(pk=dat['pk'], defaults=dict(**dat['fields']))
        status = 'Created' if created else 'Updated'
        print(f'{status} entry for account {str(obj)}')

def update_channel():
    with open(os.path.join(settings.BASE_DIR, 'backend/update_models/channel.json'), 'r') as f:
        data = json.load(f)
    for dat in data:
        group = Group.objects.get(pk=dat['fields']['group'])
        dat['fields']['group'] = group
        obj, created = Channel.objects.update_or_create(pk=dat['pk'], defaults=dict(**dat['fields']))
        status = 'Created' if created else 'Updated'
        print(f'{status} entry for channel {str(obj)}')

def main():
    update_group()
    update_member()
    update_alias()
    update_account()
    update_channel()

if __name__ == '__main__':
    main()
