# Generated by Django 2.1.5 on 2019-04-23 02:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_auto_20190423_0622'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='is_active_comment',
            field=models.BooleanField(),
        ),
    ]
