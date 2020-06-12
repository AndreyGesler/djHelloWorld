from django.contrib import admin
from .models import Question, Choice, Review, ReviewStatus


# Register your models here.


class ReviewStatusAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_by', 'changed_by', 'created_at', 'changed_at')
    list_filter = ['name', 'created_by', 'changed_by', 'created_at', 'changed_at']
    fieldsets = [
        ('Specific information', {'fields': ['name']}),
        ('System information', {'fields': ['created_by', 'changed_by', 'created_at', 'changed_at']}),
    ]


admin.site.register(ReviewStatus, ReviewStatusAdmin)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('text', 'plus_votes', 'minus_votes', 'created_by', 'changed_by', 'created_at', 'changed_at')
    list_filter = ['text', 'plus_votes', 'minus_votes', 'created_by', 'changed_by', 'created_at', 'changed_at']
    fieldsets = [
        ('Specific information', {'fields': ['text', 'plus_votes', 'minus_votes']}),
        ('System information', {'fields': ['created_by', 'changed_by', 'created_at', 'changed_at']}),
    ]


admin.site.register(Review, ReviewAdmin)


# class ChoiceInline(admin.StackedInline):
class ChoiceInline(admin.TabularInline):
    model = Choice
    # extra = 3


class QuestionAdmin(admin.ModelAdmin):
    # fields = ['pub_date', 'question_text']
    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date']}),
    ]
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    inlines = [ChoiceInline]


admin.site.register(Question, QuestionAdmin)
# admin.site.register(Choice)


