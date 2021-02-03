# Generated by Django 3.1.4 on 2021-01-28 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_note_task'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listfield',
            name='field_type',
            field=models.CharField(choices=[('text', 'Text'), ('long-text', 'Long Text'), ('number', 'Number'), ('url', 'Url'), ('choose-from-list', 'Choose from List'), ('date', 'Date')], default='text', max_length=250),
        ),
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('active', 'Active'), ('archived', 'Archived'), ('deleted', 'Deleted'), ('complete', 'Complete')], default='active', max_length=25),
        ),
    ]
