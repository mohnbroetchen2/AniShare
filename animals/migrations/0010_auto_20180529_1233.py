# Generated by Django 2.0.4 on 2018-05-29 10:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('animals', '0009_auto_20180514_1102'),
    ]

    operations = [
        migrations.AddField(
            model_name='animal',
            name='added_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='animal',
            name='organ_type',
            field=models.CharField(choices=[('bladder', 'bladder'), ('bone marrow', 'bone marrow'), ('brain', 'brain'), ('genitals', 'genitals'), ('heart', 'heart'), ('intestine', 'intestine'), ('kidney', 'kidney'), ('liver', 'liver'), ('lungs', 'lungs'), ('spleen', 'spleen'), ('stomach', 'stomach'), ('other', 'other'), ('whole animal', 'whole animal')], default='whole animal', max_length=100),
        ),
    ]
