# Generated by Django 3.1 on 2022-04-03 22:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_auto_20220403_2232'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitemmodel',
            name='cart',
            field=models.ForeignKey(help_text='Cart', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='cart.cartmodel', verbose_name='Cart'),
        ),
        migrations.AlterField(
            model_name='cartitemmodel',
            name='is_active',
            field=models.BooleanField(default=True, help_text='Active', verbose_name='Active'),
        ),
        migrations.AlterField(
            model_name='cartitemmodel',
            name='product',
            field=models.ForeignKey(help_text='Product', on_delete=django.db.models.deletion.CASCADE, to='store.productmodel', verbose_name='Product'),
        ),
        migrations.AlterField(
            model_name='cartitemmodel',
            name='quantity',
            field=models.PositiveIntegerField(help_text='Quantity', verbose_name='Quantity'),
        ),
        migrations.AlterField(
            model_name='cartitemmodel',
            name='user',
            field=models.ForeignKey(help_text='User', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
        migrations.AlterField(
            model_name='cartmodel',
            name='cart_id',
            field=models.CharField(blank=True, help_text='Cart ID', max_length=250, unique=True, verbose_name='Cart ID'),
        ),
        migrations.AlterField(
            model_name='cartmodel',
            name='date_added',
            field=models.DateField(auto_now_add=True, help_text='Created Date', verbose_name='Created Date'),
        ),
        migrations.AlterField(
            model_name='cartmodel',
            name='user',
            field=models.ForeignKey(help_text='User', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
    ]