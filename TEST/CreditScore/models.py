from django.db import models
from django.contrib.auth.models import User

# User model extension
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    email = models.EmailField(max_length=255)
    company_name = models.CharField(max_length=255)

    def __str__(self):
        return self.user.username if self.user else 'Anonymous User'

# Question model
class Question(models.Model):
    question_text = models.CharField(max_length=255)

    def __str__(self):
        return self.question_text

# Option model to link options to questions with specific weightage
class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    option_text = models.CharField(max_length=255)
    weightage = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.option_text} ({self.weightage} points)"

# User response model to track answers
class UserResponse(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.ForeignKey(Option, on_delete=models.CASCADE)

    def __str__(self):
        return f"Response by {self.user_profile} for {self.question}"

# Credit Score model
class CreditScore(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    score = models.PositiveIntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_profile} - Score: {self.score}"

