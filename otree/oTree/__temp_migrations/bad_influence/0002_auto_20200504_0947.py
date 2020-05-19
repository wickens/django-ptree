# Generated by Django 2.2.4 on 2020-05-04 09:47

from django.db import migrations, models
import django.db.models.deletion
import otree.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('bad_influence', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='chat_id',
            field=otree.db.models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='message',
            name='group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='bad_influence.Group'),
        ),
        migrations.AlterField(
            model_name='message',
            name='content',
            field=otree.db.models.LongStringField(null=True),
        ),
        migrations.AlterField(
            model_name='message',
            name='player',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='bad_influence.Player'),
        ),
        migrations.AlterModelTable(
            name='message',
            table='bad_influence_message',
        ),
    ]
