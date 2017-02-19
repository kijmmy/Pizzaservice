# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-19 16:28
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import order.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Meal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('recipie', models.TextField()),
                ('description', models.TextField()),
            ],
            options={
                'permissions': (('view_recipie', "Can see everything we put in our 'food'."),),
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=1023)),
                ('state', models.CharField(choices=[('R', 'RECIEVED'), ('B', 'BAKING'), ('T', 'TRAVEL'), ('D', 'DONE'), ('E', 'ABBORTED')], default='R', max_length=1)),
            ],
            options={
                'permissions': (('change_state', "Can change what's happening with the food!"),),
            },
        ),
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(choices=[('s', 'XSMALL'), ('S', 'SMALL'), ('M', 'MEDIUM'), ('L', 'LARGE'), ('X', 'XLARGE')], max_length=1)),
                ('value', models.DecimalField(decimal_places=2, max_digits=10)),
                ('meal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.Meal')),
            ],
        ),
        migrations.CreateModel(
            name='Topping',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('toppings', order.models.MultiSelectField(choices=[('MU', 'MUSHROOMS'), ('CE', 'CHEESE'), ('HM', 'HAM'), ('PP', 'PEPPERONI'), ('BL', 'BELLPEPPER'), ('PA', 'PINAPPLE'), ('MZ', 'MOZARELLA'), ('TN', 'TUNA'), ('ON', 'ONIONS'), ('SC', 'SAUCE'), ('MT', 'MEAT'), ('TO', 'TOMATOES')], max_length=35)),
                ('meal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.Price')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.Order')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='meals',
            field=models.ManyToManyField(through='order.Topping', to='order.Price'),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
