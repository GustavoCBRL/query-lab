from django.contrib import admin
from .models import User, Topics, Questions, Choices, UserAnswer, PracticeExercise, PracticeSubmission
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')

class TopicsAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')

class ChoicesAdmin(admin.ModelAdmin):
    list_display = ('text')

class QuestionsAdmin(admin.ModelAdmin):
    list_display = ('statement')

class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ('is_correct')

class PracticesExerciseAdmin(admin.ModelAdmin):
    list_display = ('title')

class PracticeSubmissionAdmin(admin.ModelAdmin):
    list_display = ('submitted_query')

admin.site.register(User)
admin.site.register(Topics)
admin.site.register(Questions)
admin.site.register(Choices)
admin.site.register(UserAnswer)
admin.site.register(PracticeExercise)
admin.site.register(PracticeSubmission)