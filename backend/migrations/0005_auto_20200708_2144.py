# Generated by Django 3.0.7 on 2020-07-08 13:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0004_channel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alias',
            name='member',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='aliases', to='backend.Member'),
        ),
        migrations.AlterField(
            model_name='channel',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='channels', to='backend.Group'),
        ),
        migrations.AlterField(
            model_name='member',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='members', to='backend.Group'),
        ),
        migrations.AlterField(
            model_name='twitteraccount',
            name='member',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='twitter_accounts', to='backend.Member'),
        ),
    ]
