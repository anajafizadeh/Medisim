from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Institution, Cohort, Enrollment, Case, Assignment, Run, Message, Order, Result, Evaluation
import uuid, yaml
from django.utils.text import slugify
from .models import Institution

User = get_user_model()

class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    institution_id = serializers.PrimaryKeyRelatedField(
        source="institution",
        queryset=Institution.objects.all(),
        required=False,
        allow_null=True
    )

    class Meta:
        model = User
        fields = ["id", "username", "password", "role", "institution_id"]

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

class CaseListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Case
        fields = ['id','title','specialty','difficulty','created_at']

class CaseDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Case
        fields = ['id','title','specialty','difficulty','yaml_blob','rubric_id','created_at']


# 🔹 Serializer for instructors to create/edit cases
class CaseCreateUpdateSerializer(serializers.ModelSerializer):
    # Optional structured fields
    case_id = serializers.CharField(required=False, allow_blank=True)
    objectives = serializers.ListField(child=serializers.CharField(), required=False)
    patient = serializers.DictField(required=False)
    qa_reveals = serializers.DictField(required=False)
    orders = serializers.DictField(required=False)
    expected = serializers.DictField(required=False)

    # Or provide raw YAML directly
    yaml_blob = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Case
        fields = [
            "id",
            "title",
            "specialty",
            "difficulty",
            "rubric_id",
            "yaml_blob",      # raw input option
            "case_id",
            "objectives",
            "patient",
            "qa_reveals",
            "orders",
            "expected"
        ]
        read_only_fields = ["id"]

    def _build_yaml_from_structured(self, data):
        title = data.get("title", "Untitled Case")
        specialty = data.get("specialty", "unknown")
        difficulty = data.get("difficulty", "unknown")
        rubric_id = data.get("rubric_id", "unknown")

        # Generate case_id if not provided
        provided_case_id = data.get("case_id", "").strip()
        final_case_id = provided_case_id or f"{slugify(title) or 'case'}_{uuid.uuid4().hex[:6]}"

        # Objectives
        objectives = data.get("objectives") or []

        # Patient
        patient = data.get("patient") or {}
        demographics = patient.get("demographics") or {}
        vitals = patient.get("baseline_vitals") or {}
        core_story = patient.get("core_story") or {}
        patient_obj = {
            "demographics": {
                "age": demographics.get("age", "unknown"),
                "sex": demographics.get("sex", "unknown"),
                # If you later add name support:
                **({"name": demographics["name"]} if "name" in demographics else {})
            },
            "personality": patient.get("personality", "unknown"),
            "baseline_vitals": {
                "temp_c": vitals.get("temp_c", "unknown"),
                "hr": vitals.get("hr", "unknown"),
                "rr": vitals.get("rr", "unknown"),
                "bp": vitals.get("bp", "unknown"),
            },
            "core_story": {
                "chief_complaint": core_story.get("chief_complaint", "unknown"),
                "hpi_summary": core_story.get("hpi_summary", ""),
            },
        }

        # QA reveals
        qa_reveals = data.get("qa_reveals") or {}

        # Orders
        orders = data.get("orders") or {}
        orders_allowed = orders.get("allowed") or []
        orders_results = orders.get("results") or {}

        # Expected findings
        expected = data.get("expected") or {}
        key_findings = expected.get("key_findings") or []
        differentials = expected.get("differentials") or {}
        final_dx = expected.get("final_dx", "unknown")
        initial_plan_high_level = expected.get("initial_plan_high_level") or []

        case_dict = {
            "id": final_case_id,
            "title": title,
            "specialty": specialty,
            "difficulty": difficulty,
            "objectives": objectives,
            "rubric_id": rubric_id,
            "patient": patient_obj,
            "qa_reveals": qa_reveals,
            "orders": {
                "allowed": orders_allowed,
                "results": orders_results,
            },
            "expected": {
                "key_findings": key_findings,
                "differentials": {
                    "should_include": differentials.get("should_include", []),
                    "reasonable_alternatives": differentials.get("reasonable_alternatives", []),
                },
                "final_dx": final_dx,
                "initial_plan_high_level": initial_plan_high_level,
            },
        }

        return yaml.safe_dump(case_dict, sort_keys=False)

    def validate(self, attrs):
        # If yaml_blob missing, construct one from structured JSON
        if not attrs.get("yaml_blob"):
            attrs["yaml_blob"] = self._build_yaml_from_structured(attrs)
        return attrs

    def create(self, validated_data):
        # Drop non-model-only fields
        for extra in ["case_id", "objectives", "patient", "qa_reveals", "orders", "expected"]:
            validated_data.pop(extra, None)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        for extra in ["case_id", "objectives", "patient", "qa_reveals", "orders", "expected"]:
            validated_data.pop(extra, None)
        return super().update(instance, validated_data)


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
