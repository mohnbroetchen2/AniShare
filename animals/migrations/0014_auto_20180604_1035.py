# Generated by Django 2.0.4 on 2018-06-04 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('animals', '0013_organ'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='organ',
            name='available_from',
        ),
        migrations.RemoveField(
            model_name='organ',
            name='available_to',
        ),
        migrations.AlterField(
            model_name='organ',
            name='killing_person',
            field=models.CharField(help_text='Email address of the person who is responsible for killing the animal', max_length=200),
        ),
    ]
