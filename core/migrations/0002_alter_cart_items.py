# Generated by Django 4.2.3 on 2024-04-28 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='items',
            field=models.ManyToManyField(related_name='carts', through='core.CartItem', to='core.product'),
        ),
    ]
