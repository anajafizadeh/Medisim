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

    @action(detail=True, methods=['get', 'post'])
    def messages(self, request, pk=None):
        run = self.get_object()

        if request.method.lower() == 'get':
            # Return all messages for this run
            msgs = Message.objects.filter(run=run).order_by('created_at')
            return Response(MessageSerializer(msgs, many=True).data)

        # Handle POST (student sends a message)
        case = parse_case_yaml(run.case.yaml_blob)

        student_text = request.data.get('text', '')
        tags = classify_intents(student_text)
        student_msg = Message.objects.create(
            run=run, sender='student', text=student_text, tags_json=tags
        )

        # Construct patient reply by mapping tags → reveals (simple MVP)
        replies = []
        for t in tags:
            if t in case.reveals:
                replies.append(case.reveals[t])
        if not replies:
            replies = ["I'm not sure what you mean. Could you clarify?"]
        patient_text = ' '.join(replies)
        patient_msg = Message.objects.create(
            run=run, sender='patient', text=patient_text, tags_json=[]
        )

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
