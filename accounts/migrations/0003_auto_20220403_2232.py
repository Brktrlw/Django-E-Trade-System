# Generated by Django 3.1 on 2022-04-03 22:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20220403_1419'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermodel',
            name='phone_number',
            field=models.CharField(help_text='Phone Number', max_length=15, verbose_name='Phone Number'),
        ),
        migrations.AlterField(
            model_name='userprofilemodel',
            name='address_title',
            field=models.CharField(max_length=100, verbose_name='Address Title'),
        ),
        migrations.AlterField(
            model_name='userprofilemodel',
            name='avatar',
            field=models.ImageField(blank=True, default='default/user.jpg', upload_to='userprofile/', verbose_name='Photo'),
        ),
        migrations.AlterField(
            model_name='userprofilemodel',
            name='city',
            field=models.CharField(max_length=100, verbose_name='City'),
        ),
        migrations.AlterField(
            model_name='userprofilemodel',
            name='clear_address',
            field=models.TextField(max_length=250, verbose_name='Clear Address'),
        ),
        migrations.AlterField(
            model_name='userprofilemodel',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
    ]
