# Generated by Django 2.2.4 on 2020-04-24 12:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bad_influence', '0018_auto_20200422_1037'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='bad_influence.Group'),
        ),
    ]