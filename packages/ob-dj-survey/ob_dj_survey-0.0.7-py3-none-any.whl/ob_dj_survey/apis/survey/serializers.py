import logging
import typing

from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from ob_dj_survey.apis.user.serializers import UserSerializer
from ob_dj_survey.core.survey.models import (
    Survey,
    SurveyAnswers,
    SurveyCategory,
    SurveyChoice,
    SurveyQuestion,
    SurveyResponse,
    SurveySection,
)

logger = logging.getLogger(__name__)


class SurveyCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyCategory
        fields = ("id", "name", "created_at")


class SurveySectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveySection
        fields = ("id", "name", "description", "category", "created_at")

    def to_representation(self, instance) -> typing.Dict:
        data = super().to_representation(instance)
        data["category"] = SurveyCategorySerializer(instance.category).data
        return data


class SurveySerializer(serializers.ModelSerializer):
    questions = serializers.SerializerMethodField()

    class Meta:
        model = Survey
        fields = (
            "id",
            "name",
            "section",
            "questions",
            "created_at",
        )

    def to_representation(self, instance) -> typing.Dict:
        data = super().to_representation(instance)
        data["section"] = SurveySectionSerializer(instance.section).data
        return data

    def get_questions(self, obj):
        return SurveyQuestionSerializer(
            obj.questions.all().order_by("created_at"), many=True
        ).data


class SurveyChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyChoice
        fields = ("id", "title", "created_at")


class AnswersSerializer(serializers.Serializer):
    """
        * Serializer for Submitting Answers

    - Answers Example :
        "answers": [{"question": question_1.pk, "choices": [ab_choice.pk},
                    {"question": question_2.pk, "choices": [fish_choice.pk, "Gluten"]},
                    {"question": question_3.pk, "choices": ["13"},
    """

    question = serializers.PrimaryKeyRelatedField(queryset=SurveyQuestion.objects.all())
    choices = serializers.PrimaryKeyRelatedField(
        queryset=SurveyChoice.objects.all(), many=True, required=False
    )
    values = serializers.ListField(required=False)

    def validate(self, attrs):
        if not attrs.get("choices") and not attrs.get("values"):
            raise serializers.ValidationError(_("No Answers Provided"))
        return attrs


class SurveyResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyResponse
        fields = (
            "id",
            "question",
            "choice",
            "value",
            "created_at",
            "updated_at",
        )

    def to_representation(self, instance) -> typing.Dict:
        data = super().to_representation(instance)
        data["question"] = SurveyQuestionSerializer(instance.question).data
        data["choice"] = SurveyChoiceSerializer(instance.choice).data
        return data

    def validate(self, data):
        # TODO: Validate Each type of Question by the choices sent within it.
        return data


class SurveyAnswersSerializer(serializers.ModelSerializer):
    answers = AnswersSerializer(many=True, write_only=True)

    class Meta:
        model = SurveyAnswers
        fields = (
            "id",
            "survey",
            "responses",
            "answers",
            "status",
            "created_by",
            "created_at",
            "updated_at",
        )
        extra_kwargs = {
            "created_by": {"read_only": True},
        }

    def to_representation(self, instance) -> typing.Dict:
        data = super().to_representation(instance)
        data["survey"] = SurveySerializer(instance.survey).data
        data["responses"] = SurveyResponseSerializer(
            instance.responses.all(), many=True
        ).data
        data["created_by"] = UserSerializer(instance.created_by).data
        return data

    def create(self, validated_data):
        validated_data["created_by"] = self.context["request"].user
        return SurveyAnswers.objects.create(**validated_data)


class SurveyQuestionSerializer(serializers.ModelSerializer):
    choices = serializers.SerializerMethodField()

    class Meta:
        model = SurveyQuestion
        fields = (
            "id",
            "title",
            "type",
            "is_active",
            "created_at",
            "choices",
        )

    def get_choices(self, obj):
        return SurveyChoiceSerializer(obj.choices.all(), many=True).data
