# Generated by Django 4.2.7 on 2023-11-14 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EduTerm', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='term',
            name='active_term',
            field=models.BooleanField(default=False, verbose_name='ترم فعال جاری'),
        ),
    ]
