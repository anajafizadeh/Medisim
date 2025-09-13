# Project: medisim_backend
# Minimal Django + DRF starter implementing the MVP backend skeleton
# ├─ manage.py
# ├─ medisim_backend/
# │  ├─ __init__.py
# │  ├─ settings.py
# │  ├─ urls.py
# │  └─ asgi.py / wsgi.py
# ├─ core/
# │  ├─ __init__.py
# │  ├─ admin.py
# │  ├─ apps.py
# │  ├─ models.py
# │  ├─ serializers.py
# │  ├─ views.py
# │  ├─ urls.py
# │  ├─ permissions.py
# │  └─ migrations/
# ├─ engine/                # AI-related helpers (intent, evaluator)
# │  ├─ __init__.py
# │  ├─ intent.py
# │  ├─ evaluator.py
# │  └─ case_loader.py
# ├─ management/
# │  └─ commands/
# │     └─ load_case.py
# ├─ requirements.txt
# └─ .env.example

# =============================
# requirements.txt
# =============================
Django>=5.0
psycopg2-binary>=2.9
 djangorestframework>=3.15
 djangorestframework-simplejwt>=5.3
 PyYAML>=6.0
 python-dateutil>=2.9

# =============================
# .env.example
# =============================
DJANGO_SECRET_KEY=replace-me
DJANGO_DEBUG=True
DATABASE_URL=psql://postgres:postgres@localhost:5432/medisim
ALLOWED_HOSTS=localhost,127.0.0.1

# =============================
# medisim_backend/settings.py (essentials only)
# =============================
from pathlib import Path
import os
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'dev-secret')
DEBUG = os.getenv('DJANGO_DEBUG', 'True') == 'True'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'medisim_backend.urls'
TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [],
    'APP_DIRS': True,
    'OPTIONS': {
        'context_processors': [
            'django.template.context_processors.debug',
            'django.template.context_processors.request',
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages',
        ],
    },
}]
WSGI_APPLICATION = 'medisim_backend.wsgi.application'

# Database: prefer DATABASE_URL if present
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB', 'medisim'),
        'USER': os.getenv('POSTGRES_USER', 'postgres'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', 'postgres'),
        'HOST': os.getenv('POSTGRES_HOST', 'localhost'),
        'PORT': os.getenv('POSTGRES_PORT', '5432'),
    }
}

AUTH_USER_MODEL = 'core.User'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=6),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# =============================
# medisim_backend/urls.py
# =============================
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include('core.urls')),
]

# =============================
# core/models.py
# =============================
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

# =============================
# core/serializers.py
# =============================
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Institution, Cohort, Enrollment, Case, Assignment, Run, Message, Order, Result, Evaluation

User = get_user_model()

class CaseListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Case
        fields = ['id','title','specialty','difficulty','created_at']

class CaseDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Case
        fields = ['id','title','specialty','difficulty','yaml_blob','rubric_id','created_at']

class RunSerializer(serializers.ModelSerializer):
    class Meta:
        model = Run
        fields = ['id','user','case','started_at','submitted_at','status']
        read_only_fields = ['user','started_at']

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id','run','sender','text','tags_json','created_at']
        read_only_fields = ['sender','tags_json','created_at']

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id','run','test_name','created_at']
        read_only_fields = ['created_at']

class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = ['id','order','result_text']

class EvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evaluation
        fields = ['id','run','rubric_id','scores_json','feedback_json','overall']

# =============================
# core/permissions.py (simple role helpers)
# =============================
from rest_framework.permissions import BasePermission

class IsInstructor(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'instructor')

# =============================
# engine/case_loader.py (YAML parsing + helpers)
# =============================
import yaml
from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class ParsedCase:
    meta: Dict[str, Any]
    reveals: Dict[str, str]
    orders_allowed: list
    order_results: Dict[str, str]
    expected: Dict[str, Any]


def parse_case_yaml(blob: str) -> ParsedCase:
    data = yaml.safe_load(blob)
    reveals = data.get('qa_reveals', {})
    orders = data.get('orders', {})
    return ParsedCase(
        meta={k: data.get(k) for k in ['id','title','specialty','difficulty','objectives','patient']},
        reveals=reveals,
        orders_allowed=orders.get('allowed', []),
        order_results=orders.get('results', {}),
        expected=data.get('expected', {}),
    )

# =============================
# engine/intent.py (very stubby intent tagger)
# =============================
from typing import List

# Simple keyword → tag mapping for MVP; replace with LLM classification later
KEYWORD_TAGS = [
    ('when', 'hx_onset'),
    ('start', 'hx_onset'),
    ('burn', 'hx_quality'),
    ('discharge', 'hx_discharge'),
    ('flank', 'hx_flank_pain'),
    ('pregnan', 'hx_pregnancy'),
]

def classify_intents(message: str) -> List[str]:
    text = message.lower()
    tags = set()
    for kw, tag in KEYWORD_TAGS:
        if kw in text:
            tags.add(tag)
    return list(tags) or ['misc']

# =============================
# engine/evaluator.py (rubric-based dummy evaluator)
# =============================
from typing import Dict, Any

def evaluate_transcript(case: dict, messages: list, differential: list, final_dx: str, tests: list) -> Dict[str, Any]:
    # Minimal heuristic scorer for MVP
    expected = case.get('expected', {})
    must_dx = expected.get('differentials', {}).get('should_include', [])
    good_tests = case.get('orders', {}).get('allowed', [])

    asked_tags = set()
    for m in messages:
        for t in m.get('tags_json', []):
            asked_tags.add(t)

    hist_score = 2 if all(k in asked_tags for k in ['hx_onset','hx_discharge','hx_flank_pain','hx_pregnancy']) else (1 if any(k in asked_tags for k in ['hx_onset','hx_discharge']) else 0)
    diff_score = 2 if any(dx in must_dx for dx in differential+[final_dx]) else 1 if differential else 0
    test_score = 2 if any(t in good_tests for t in tests) else 0
    comm_score = 1  # placeholder

    scores = {
        'history_coverage': hist_score,
        'differential_quality': diff_score,
        'test_selection': test_score,
        'communication': comm_score,
    }
    overall = round((hist_score+diff_score+test_score+comm_score)/4, 2)

    feedback = {
        'history_coverage': 'Consider asking about pregnancy status and flank pain.' if hist_score<2 else 'Thorough history-taking.',
        'differential_quality': 'Include the most likely dx in your top 3.' if diff_score<2 else 'Good differential.',
        'test_selection': 'Urinalysis and pregnancy test are appropriate first-line tests.' if test_score<2 else 'Appropriate initial testing.',
        'communication': 'Try summarizing before moving on.'
    }
    return {'scores': scores, 'feedback': feedback, 'overall': overall}

# =============================
# core/views.py
# =============================
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from .models import Case, Run, Message, Order, Result, Evaluation
from .serializers import (
    CaseListSerializer, CaseDetailSerializer, RunSerializer,
    MessageSerializer, OrderSerializer, ResultSerializer, EvaluationSerializer
)
from engine.case_loader import parse_case_yaml
from engine.intent import classify_intents
from engine.evaluator import evaluate_transcript
import yaml

User = get_user_model()

class CaseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Case.objects.all().order_by('-created_at')
    def get_serializer_class(self):
        return CaseDetailSerializer if self.action == 'retrieve' else CaseListSerializer

class RunViewSet(viewsets.ModelViewSet):
    queryset = Run.objects.all()
    serializer_class = RunSerializer

    def get_queryset(self):
        return Run.objects.filter(user=self.request.user).order_by('-started_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def messages(self, request, pk=None):
        run = self.get_object()
        case = parse_case_yaml(run.case.yaml_blob)

        student_text = request.data.get('text', '')
        tags = classify_intents(student_text)
        student_msg = Message.objects.create(run=run, sender='student', text=student_text, tags_json=tags)

        # Construct patient reply by mapping tags → reveals (simple concatenation for MVP)
        replies = []
        for t in tags:
            if t in case.reveals:
                replies.append(case.reveals[t])
        if not replies:
            replies = ["I'm not sure what you mean. Could you clarify?"]
        patient_text = ' '.join(replies)
        patient_msg = Message.objects.create(run=run, sender='patient', text=patient_text, tags_json=[])

        return Response({
            'student': MessageSerializer(student_msg).data,
            'patient': MessageSerializer(patient_msg).data
        })

    @action(detail=True, methods=['post'])
    def orders(self, request, pk=None):
        run = self.get_object()
        case = parse_case_yaml(run.case.yaml_blob)
        test_name = request.data.get('test_name')
        if test_name not in case.orders_allowed:
            return Response({'detail': 'Test not allowed for this case.'}, status=400)
        order = Order.objects.create(run=run, test_name=test_name)
        result_text = case.order_results.get(test_name, 'Pending')
        Result.objects.create(order=order, result_text=result_text)
        return Response({'order': OrderSerializer(order).data, 'result': ResultSerializer(order.result).data})

    @action(detail=True, methods=['get'])
    def results(self, request, pk=None):
        run = self.get_object()
        results = Result.objects.filter(order__run=run)
        return Response(ResultSerializer(results, many=True).data)

    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        run = self.get_object()
        case_data = yaml.safe_load(run.case.yaml_blob)
        differential = request.data.get('differential', [])
        final_dx = request.data.get('final_dx', '')
        plan = request.data.get('plan', [])

        tests = list(Order.objects.filter(run=run).values_list('test_name', flat=True))
        transcript = list(Message.objects.filter(run=run).values('sender','text','tags_json').order_by('created_at'))

        result = evaluate_transcript(case_data, transcript, differential, final_dx, tests)
        ev = Evaluation.objects.create(run=run, rubric_id=run.case.rubric_id, scores_json=result['scores'], feedback_json=result['feedback'], overall=result['overall'])
        run.status = 'submitted'
        from django.utils import timezone
        run.submitted_at = run.submitted_at or timezone.now()
        run.save(update_fields=['status','submitted_at'])
        return Response(EvaluationSerializer(ev).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'])
    def evaluation(self, request, pk=None):
        run = self.get_object()
        if not hasattr(run, 'evaluation'):
            return Response({'detail': 'Not evaluated yet.'}, status=404)
        return Response(EvaluationSerializer(run.evaluation).data)

# =============================
# core/urls.py
# =============================
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CaseViewSet, RunViewSet

router = DefaultRouter()
router.register(r'cases', CaseViewSet, basename='case')
router.register(r'runs', RunViewSet, basename='run')

urlpatterns = [
    path('', include(router.urls)),
]

# =============================
# management/commands/load_case.py
# =============================
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from core.models import Case
from pathlib import Path
import yaml

class Command(BaseCommand):
    help = 'Load a YAML case file into the database.'

    def add_arguments(self, parser):
        parser.add_argument('yaml_path', type=str)
        parser.add_argument('--creator-email', type=str, default=None)

    def handle(self, *args, **opts):
        p = Path(opts['yaml_path'])
        if not p.exists():
            raise CommandError(f"File not found: {p}")
        blob = p.read_text()
        data = yaml.safe_load(blob)
        title = data.get('title', p.stem)
        rubric_id = data.get('rubric_id', 'rubric_default')
        user_model = get_user_model()
        creator = None
        if opts['creator_email']:
            creator = user_model.objects.filter(email=opts['creator_email']).first()
        case = Case.objects.create(title=title, specialty=data.get('specialty',''), difficulty=data.get('difficulty',''), yaml_blob=blob, rubric_id=rubric_id, created_by=creator)
        self.stdout.write(self.style.SUCCESS(f"Loaded case '{case.title}' (id={case.id})"))

# =============================
# core/admin.py (optional quick admin wiring)
# =============================
from django.contrib import admin
from .models import Institution, User, Cohort, Enrollment, Case, Assignment, Run, Message, Order, Result, Evaluation

admin.site.register([Institution, User, Cohort, Enrollment, Case, Assignment, Run, Message, Order, Result, Evaluation])

# =============================
# Sample case file (save as cases/case_uti_001.yaml)
# =============================
# id: "case_uti_001"
# title: "Dysuria and frequency in a young adult"
# specialty: "Family Medicine"
# difficulty: "Easy"
# objectives:
#   - "Elicit key history for lower urinary tract symptoms"
# rubric_id: "rubric_uti_v1"
# patient:
#   demographics: { age: 24, sex: "female" }
#   personality: "cooperative"
#   baseline_vitals: { temp_c: 37.4, hr: 88, rr: 16, bp: "112/70" }
#   core_story:
#     chief_complaint: "Burning urination and frequency"
#     hpi_summary: |
#       Onset 3 days ago, dysuria and frequency, no flank pain, mild suprapubic discomfort.
#       No vaginal discharge. Sexually active, monogamous.
# qa_reveals:
#   hx_onset: "It started about three days ago."
#   hx_quality: "It burns when I pee."
#   hx_flank_pain: "No, the pain is more in the lower belly."
#   hx_discharge: "No discharge."
#   hx_pregnancy: "My last period was two weeks ago, and they're regular."
# orders:
#   allowed: ["Urinalysis", "Urine culture", "Pregnancy test"]
#   results:
#     "Urinalysis": |
#       Leukocyte esterase positive, nitrites positive, WBCs 10-20/hpf
#     "Urine culture": "Pending at 48 hours"
#     "Pregnancy test": "Negative"
# expected:
#   key_findings:
#     - "Dysuria and frequency without discharge"
#     - "No flank pain"
#     - "Positive nitrites/leukocyte esterase on UA"
#   differentials:
#     should_include: ["Acute uncomplicated cystitis"]
#     reasonable_alternatives: ["Vaginitis", "Urethritis"]
#   final_dx: "Acute uncomplicated cystitis"
#   initial_plan_high_level: ["Outpatient management", "Education and safety net"]
