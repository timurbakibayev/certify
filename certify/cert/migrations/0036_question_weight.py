# Generated by Django 2.2 on 2020-04-25 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cert', '0035_auto_20200425_1908'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='weight',
            field=models.IntegerField(default=1),
        ),
    ]
