# Generated by Django 2.2 on 2019-04-12 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cert', '0012_auto_20190412_1714'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignedquestion',
            name='answered',
            field=models.BooleanField(default=False),
        ),
    ]