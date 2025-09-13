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