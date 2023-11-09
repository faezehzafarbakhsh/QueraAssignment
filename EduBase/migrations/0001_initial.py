# Generated by Django 4.2.7 on 2023-11-09 18:59

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='College',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='نام دانشکده')),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='نام درس')),
                ('unit_count', models.IntegerField(verbose_name='تعداد واحد درس')),
                ('course_type', models.IntegerField(choices=[(1, 'عمومی'), (2, 'تخصصی'), (3, 'پایه'), (4, 'اختیاری')], verbose_name='نوع درس')),
                ('college', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='courses', to='EduBase.college', verbose_name='دانشکده ارائه دهنده')),
            ],
        ),
        migrations.CreateModel(
            name='EduField',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='نام رشته')),
                ('edu_group', models.CharField(max_length=64, verbose_name='گروه تخصصی')),
                ('unit_count', models.IntegerField(default=1, validators=[django.core.validators.MaxValueValidator(999), django.core.validators.MinValueValidator(1)], verbose_name='تعداد واحد')),
                ('edu_grade', models.IntegerField(choices=[(1, 'کاردانی'), (2, 'کارشناسی'), (3, 'کارشناسی ارشد'), (4, 'دکتری')], verbose_name='مقطع تحصیلی')),
            ],
        ),
        migrations.CreateModel(
            name='CourseRelation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('relation_type', models.IntegerField(choices=[(1, 'هم نیاز'), (2, 'پیش نیاز')], verbose_name='نوع رابطه')),
                ('primary_course', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='course_relation_primary_courses', to='EduBase.course', verbose_name='درس پایه')),
                ('secondary_course', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='course_relation_secondary_courses', to='EduBase.course', verbose_name='درس رابطه')),
            ],
        ),
    ]
