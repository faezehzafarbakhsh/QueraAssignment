# Generated by Django 4.2.7 on 2023-11-28 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EduRequest', '0005_alter_studentrequest_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentrequest',
            name='status',
            field=models.IntegerField(choices=[(1, 'پذیرش'), (2, 'رد شده'), (3, 'در حال بررسی')], default='در حال بررسی', verbose_name='وضعیت'),
        ),
    ]
