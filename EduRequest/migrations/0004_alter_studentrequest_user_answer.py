# Generated by Django 4.2.7 on 2023-11-17 09:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('EduRequest', '0003_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentrequest',
            name='user_answer',
            field=models.ForeignKey(blank=True, limit_choices_to=models.Q(('is_teacher', True), ('is_chancellor', True), _connector='OR'), null=True, on_delete=django.db.models.deletion.PROTECT, related_name='student_request_answers', to=settings.AUTH_USER_MODEL, verbose_name='توضیحات معاون آموزشی'),
        ),
    ]
