from django.db import models

class Enrollment(models.Model):
    """ 
    """
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    id = models.AutoField(primary_key=True, unique=True)
    term = models.ForeignKey('Term')
    student = models.ForeignKey('Student')
    teacher_assistant = models.ForeignKey('Teacher')
    status = models.CharField(choices=STATUS_CHOICES)
    teacher_assistant_description = models.TextField()
    taken_term_number = models.IntegerField()

class StudentCourse(models.Model):
    """درسی که دانشجو برداشته"""
    STATUS_CHOICES = (
        ('enrolled', 'Enrolled'),
        ('deleted', 'Deleted'),
        ('completed', 'Completed'),
    )
    id = models.AutoField(primary_key=True)
    course_term = models.ForeignKey('CourseTerm')
    student = models.ForeignKey("Student")
    status = models.CharField(choices=STATUS_CHOICES)
    score = models.FloatField()