# Generated by Django 3.2.5 on 2021-08-04 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0014_orderupdate'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='amount',
            field=models.IntegerField(default=0, max_length=100),
        ),
    ]