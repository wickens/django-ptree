# Generated by Django 2.2.4 on 2020-04-21 08:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('daytrader', '0016_auto_20200421_0928'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='player',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='daytrader.Player'),
        ),
    ]
