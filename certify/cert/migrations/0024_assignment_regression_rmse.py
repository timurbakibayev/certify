# Generated by Django 2.2 on 2019-04-20 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cert', '0023_assignment_regression_tries_left'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='regression_rmse',
            field=models.IntegerField(default=-1),
        ),
    ]
