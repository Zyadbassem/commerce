# Generated by Django 5.0.6 on 2024-07-18 22:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_itemupdated'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='itemId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.itemupdated'),
        ),
        migrations.DeleteModel(
            name='item',
        ),
    ]
