# Generated by Django 2.2.4 on 2020-05-05 14:29

from django.db import migrations
import otree.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('daytrader', '0007_auto_20200505_1429'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='choice_of_trade',
            field=otree.db.models.IntegerField(choices=[[-1, 'gør ingenting'], [True, 'køb (long)'], [False, 'lån og sælg (short)']], default=-1, null=True),
        ),
    ]
