# Generated by Django 2.2.6 on 2020-01-13 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Subsystem', '0004_auto_20200113_1909'),
    ]

    operations = [
        migrations.AddField(
            model_name='biometricsystemmodel',
            name='needImage',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='biometricsystemmodel',
            name='needName',
            field=models.BooleanField(default=True),
        ),
    ]
