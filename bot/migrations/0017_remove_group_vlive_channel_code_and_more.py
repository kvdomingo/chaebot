# Generated by Django 4.0.4 on 2023-01-01 08:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0016_alter_group_vlive_channel_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='vlive_channel_code',
        ),
        migrations.RemoveField(
            model_name='group',
            name='vlive_channel_seq',
        ),
        migrations.RemoveField(
            model_name='group',
            name='vlive_last_seq',
        ),
        migrations.DeleteModel(
            name='VliveSubscribedChannel',
        ),
    ]
