from django.db import models
from django.contrib.auth.models import AbstractUser

class Institution(models.Model):
    name = models.CharField(max_length=255, unique=True)
    def __str__(self):
        return self.name

class User(AbstractUser):
    STUDENT = 'student'
    INSTRUCTOR = 'instructor'
    ROLES = [(STUDENT, 'Student'), (INSTRUCTOR, 'Instructor')]
    role = models.CharField(max_length=20, choices=ROLES, default=STUDENT)
    institution = models.ForeignKey(Institution, null=True, blank=True, on_delete=models.SET_NULL)

class Cohort(models.Model):
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

class Enrollment(models.Model):
    cohort = models.ForeignKey(Cohort, on_delete=models.CASCADE)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    class Meta:
        unique_together = ('cohort', 'user')

class Case(models.Model):
    title = models.CharField(max_length=255)
    specialty = models.CharField(max_length=255, blank=True)
    difficulty = models.CharField(max_length=50, blank=True)
    yaml_blob = models.TextField()
    rubric_id = models.CharField(max_length=255)
    created_by = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
class Assignment(models.Model):
    cohort = models.ForeignKey(Cohort, on_delete=models.CASCADE)
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    due_at = models.DateTimeField(null=True, blank=True)

class Run(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    started_at = models.DateTimeField(auto_now_add=True)
    submitted_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, default='in_progress')

class Message(models.Model):
    run = models.ForeignKey(Run, on_delete=models.CASCADE, related_name='messages')
    sender = models.CharField(max_length=20, choices=[('student','student'),('patient','patient')])
    text = models.TextField()
    tags_json = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Order(models.Model):
    run = models.ForeignKey(Run, on_delete=models.CASCADE)
    test_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

class Result(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='result')
    result_text = models.TextField()

class Evaluation(models.Model):
    run = models.OneToOneField(Run, on_delete=models.CASCADE, related_name='evaluation')
    rubric_id = models.CharField(max_length=255)
    scores_json = models.JSONField(default=dict)
    feedback_json = models.JSONField(default=dict)
    overall = models.FloatField(default=0.0)
