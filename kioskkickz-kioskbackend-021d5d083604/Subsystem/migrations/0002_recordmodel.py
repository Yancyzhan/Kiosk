# Generated by Django 2.2.5 on 2019-11-17 06:30

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0010_delete_biometricsystemmodel'),
        ('Subsystem', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecordModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('result', models.CharField(blank=True, default='', max_length=255)),
                ('biometricSystem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Subsystem.BiometricSystemModel')),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='API.ImageModel')),
            ],
        ),
    ]
