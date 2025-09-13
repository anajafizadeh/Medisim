from django.contrib import admin
from .models import Institution, User, Cohort, Enrollment, Case, Assignment, Run, Message, Order, Result, Evaluation

admin.site.register([Institution, User, Cohort, Enrollment, Case, Assignment, Run, Message, Order, Result, Evaluation])