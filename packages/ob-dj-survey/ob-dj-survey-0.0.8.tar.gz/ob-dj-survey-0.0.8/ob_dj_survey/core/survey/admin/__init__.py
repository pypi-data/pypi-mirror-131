from django.contrib import admin

from ob_dj_survey.core.survey.models import (
    Survey,
    SurveyAnswers,
    SurveyChoice,
    SurveyQuestion,
    SurveyResponse,
    SurveySection,
)


class SurveyQuestionInlineAdmin(admin.TabularInline):
    model = SurveyQuestion
    extra = 0


class SurveySectionInlineAdmin(admin.TabularInline):
    model = SurveySection
    extra = 0


class SurveyInlineAdmin(admin.TabularInline):
    model = Survey
    extra = 0


class SurveyChoiceInlineAdmin(admin.TabularInline):
    model = SurveyChoice
    extra = 0


class SurveyResponseInlineAdmin(admin.TabularInline):
    model = SurveyResponse
    extra = 0


class SurveyAnswersInlineAdmin(admin.TabularInline):
    model = SurveyAnswers
    extra = 0


class SurveyResponsesAnswersInline(admin.TabularInline):
    model = SurveyAnswers.responses.through


@admin.register(SurveySection)
class SurveySectionAdmin(admin.ModelAdmin,):
    list_display = ["name", "description", "created_at"]
    fieldsets = ((None, {"fields": ("name", "description",)},),)
    inlines = [SurveyInlineAdmin, SurveyQuestionInlineAdmin]


@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin,):
    fieldsets = ((None, {"fields": ("name", "section",)},),)
    list_display = ["name", "section", "created_at"]
    inlines = [SurveyAnswersInlineAdmin, SurveyQuestionInlineAdmin]


@admin.register(SurveyChoice)
class SurveyChoiceAdmin(admin.ModelAdmin,):
    fieldsets = ((None, {"fields": ("title", "question")},),)
    list_display = ["title", "created_at"]
    inlines = [SurveyResponseInlineAdmin]


@admin.register(SurveyQuestion)
class SurveyQuestionAdmin(admin.ModelAdmin,):
    fieldsets = (
        (None, {"fields": ("title", "type", "survey", "section", "is_active")},),
    )
    list_display = ["title", "type", "is_active", "section", "created_at"]
    inlines = [SurveyChoiceInlineAdmin, SurveyResponseInlineAdmin]


@admin.register(SurveyResponse)
class SurveyResponseAdmin(admin.ModelAdmin,):
    list_display = ["value", "updated_at", "created_at"]
    fieldsets = ((None, {"fields": ("question", "choice", "value",)},),)


@admin.register(SurveyAnswers)
class SurveyAnswersAdmin(admin.ModelAdmin,):
    list_display = ["status", "updated_at", "created_at"]
    fieldsets = ((None, {"fields": ("survey", "responses", "created_by", "status",)},),)
    inlines = [
        SurveyResponsesAnswersInline,
    ]
