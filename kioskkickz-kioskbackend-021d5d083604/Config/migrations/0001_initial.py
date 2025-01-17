# Generated by Django 2.2.6 on 2020-02-09 22:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('API', '0010_delete_biometricsystemmodel'),
        ('Subsystem', '0001_initial'),
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Config',
            fields=[
                ('headerTitle', models.CharField(default='Biometric Kiosk', max_length=255, null=True)),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('maxTrialTime', models.IntegerField()),
                ('biometricSystem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Subsystem.BiometricSystemModel')),
            ],
        ),
        migrations.CreateModel(
            name='UseType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='HomePageImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('config', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, to='Config.Config')),
                ('image', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, to='API.ImageModel')),
            ],
        ),
        migrations.AddField(
            model_name='config',
            name='useType',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Config.UseType'),
        ),
    ]
