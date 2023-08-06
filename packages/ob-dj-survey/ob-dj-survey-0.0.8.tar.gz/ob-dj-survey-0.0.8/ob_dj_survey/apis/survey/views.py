import logging

from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response

from ob_dj_survey.apis.survey.serializers import (
    SurveyAnswersSerializer,
    SurveySerializer,
)
from ob_dj_survey.core.survey.models import Survey, SurveyAnswers

logger = logging.getLogger(__name__)


@method_decorator(
    name="create",
    decorator=swagger_auto_schema(
        operation_summary="Create Survey",
        operation_description="""
        Write a Description
        """,
        tags=["Survey",],
    ),
)
@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        operation_summary="List Survey",
        operation_description="""
        Write a Description
        """,
        tags=["Survey",],
    ),
)
@method_decorator(
    name="retrieve",
    decorator=swagger_auto_schema(
        operation_summary="Retrieve Survey",
        operation_description="""
        Write a Description
        """,
        tags=["Survey",],
    ),
)
@method_decorator(
    name="destroy",
    decorator=swagger_auto_schema(
        operation_summary="Delete Survey",
        operation_description="""
        Write a Description
        """,
        tags=["Survey",],
    ),
)
@method_decorator(
    name="partial_update",
    decorator=swagger_auto_schema(
        operation_summary="Update Survey",
        operation_description="""
        Write a Description
        """,
        tags=["Survey",],
    ),
)
@method_decorator(
    name="update", decorator=swagger_auto_schema(auto_schema=None),
)
class SurveyView(viewsets.ModelViewSet):
    model = Survey
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SurveySerializer

    def get_queryset(self):
        return Survey.objects.active()


@method_decorator(
    name="create",
    decorator=swagger_auto_schema(
        operation_summary="Survey Answer",
        operation_description="""
        Write a Description
        """,
        tags=["Survey",],
    ),
)
class SurveyAnswersView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SurveyAnswersSerializer

    def get_queryset(self):
        return SurveyAnswers.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
