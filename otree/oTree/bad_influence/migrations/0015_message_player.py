# Generated by Django 2.2.4 on 2020-04-21 07:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('daytrader', '0014_remove_message_player'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='player',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='daytrader.Player'),
        ),
    ]
