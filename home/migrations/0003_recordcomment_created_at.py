# Generated by Django 3.1.4 on 2021-02-05 16:45

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_auto_20210205_1729'),
    ]

    operations = [
        migrations.AddField(
            model_name='recordcomment',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2021, 2, 5, 22, 15, 56, 218493)),
            preserve_default=False,
        ),
    ]