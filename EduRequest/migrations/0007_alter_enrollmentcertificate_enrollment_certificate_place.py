# Generated by Django 4.2.7 on 2023-11-22 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EduRequest', '0006_enrollmentcertificate_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enrollmentcertificate',
            name='enrollment_certificate_place',
            field=models.CharField(max_length=128, null=True, verbose_name='محل صدور گواهی'),
        ),
    ]