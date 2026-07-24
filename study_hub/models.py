from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    pass

class Topics(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    summary = models.TextField()
    theory = models.TextField()
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.slug}"

class Questions(models.Model):
    topic = models.ForeignKey(Topics, on_delete=models.CASCADE, related_name="questions")
    statement = models.TextField()
    explanation = models.TextField()

    def __str__(self):
        return self.statement[:50]
    
class Choices(models.Model):
    question = models.ForeignKey(Questions, on_delete=models.CASCADE, related_name="choice")
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text
    
class UserAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Questions, on_delete=models.CASCADE)
    selected_choice = models.ForeignKey(Choices, on_delete=models.CASCADE)
    is_correct = models.BooleanField()
    answered_at = models.DateField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "question"],
                name="unique_user_question_answer"
            )
        ]

class PracticeExercise(models.Model):
    topic = models.ForeignKey(Topics, on_delete=models.CASCADE, related_name="practices")
    title = models.CharField(max_length=100)
    instructions = models.TextField()
    expected_query = models.TextField()
    dataset = models.JSONField()


class PracticeSubmission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    practice = models.ForeignKey(PracticeExercise, on_delete=models.CASCADE)
    submitted_query = models.TextField()
    is_correct = models.BooleanField()
    submitted_at = models.DateTimeField(auto_now_add=True)

