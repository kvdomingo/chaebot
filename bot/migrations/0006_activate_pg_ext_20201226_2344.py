from django.db import migrations
from django.contrib.postgres.operations import TrigramExtension, UnaccentExtension


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0005_auto_20201225_2343'),
    ]

    operations = [
        TrigramExtension(),
        UnaccentExtension(),
    ]
