from dotenv import load_dotenv
load_dotenv()

import django
django.setup()

import json
from src import BASE_DIR
from bot.models import *


def main():
    with open(BASE_DIR / 'scripts' / 'data' / 'group.json', 'r') as f:
        groups = json.load(f)
    for group in groups:
        obj, created = Group.objects.update_or_create(
            pk=group['id'],
            defaults={k: v for k, v in group.items() if k != 'id'}
        )
        status = 'Created' if created else 'Updated'
        print(f'{status} group entry {str(obj)}')

    with open(BASE_DIR / 'scripts' / 'data' / 'member.json', 'r') as f:
        members = json.load(f)
    for member in members:
        member['group'] = Group.objects.get(pk=member['group_id'])
        del member['group_id']
        obj, created = Member.objects.update_or_create(
            pk=member['id'],
            defaults={k: v for k, v in member.items() if k != 'id'}
        )
        status = 'Created' if created else 'Updated'
        print(f'{status} member entry {str(obj)}')

    with open(BASE_DIR / 'scripts' / 'data' / 'alias.json', 'r') as f:
        aliases = json.load(f)
    for alias in aliases:
        alias['member'] = Member.objects.get(pk=alias['member_id'])
        del alias['member_id']
        obj, created = MemberAlias.objects.update_or_create(
            pk=alias['id'],
            defaults={k: v for k, v in alias.items() if k != 'id'}
        )
        status = 'Created' if created else 'Updated'
        print(f'{status} member alias entry {str(obj)}')

    with open(BASE_DIR / 'scripts' / 'data' / 'twitteraccount.json', 'r') as f:
        accounts = json.load(f)
    for account in accounts:
        account['member'] = Member.objects.get(pk=account['member_id'])
        del account['member_id']
        obj, created = TwitterMediaSource.objects.update_or_create(
            pk=account['id'],
            defaults={k: v for k, v in account.items() if k != 'id'}
        )
        status = 'Created' if created else 'Updated'
        print(f'{status} twitter media source account entry {str(obj)}')

    with open(BASE_DIR / 'scripts' / 'data' / 'twitterchannel.json', 'r') as f:
        channels = json.load(f)
    for channel in channels:
        channel['group'] = Group.objects.get(pk=channel['group_id'])
        del channel['group_id']
        obj, created = TwitterMediaSubscribedChannel.objects.update_or_create(
            pk=channel['id'],
            defaults={k: v for k, v in channel.items() if k != 'id'}
        )
        status = 'Created' if created else 'Updated'
        print(f'{status} twitter media subscribed channel entry {str(obj)}')

    with open(BASE_DIR / 'scripts' / 'data' / 'vlivechannel.json', 'r') as f:
        channels = json.load(f)
    for channel in channels:
        channel['group'] = Group.objects.get(pk=channel['group_id'])
        del channel['group_id']
        obj, created = VliveSubscribedChannel.objects.update_or_create(
            pk=channel['id'],
            defaults={k: v for k, v in channel.items() if k != 'id'}
        )
        status = 'Created' if created else 'Updated'
        print(f'{status} vlive subscribed channel entry {str(obj)}')


if __name__ == '__main__':
    main()
