# Generated by Django 4.2.7 on 2023-11-09 18:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('EduRequest', '0001_initial'),
        ('EduTerm', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentrequest',
            name='course_term',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='student_requests', to='EduTerm.courseterm', verbose_name='درس ترمی'),
        ),
    ]