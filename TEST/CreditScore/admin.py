from django.contrib import admin
from .models import Question, Option, UserProfile, UserResponse, CreditScore

# Inline option to allow adding options while editing a question
class OptionInline(admin.TabularInline):
    model = Option
    extra = 4  # Number of options to display for input

# Custom admin for the Question model
class QuestionAdmin(admin.ModelAdmin):
    inlines = [OptionInline]

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'company_name') 
    search_fields = ('user__username', 'email', 'company_name')

@admin.register(UserResponse)
class UserResponseAdmin(admin.ModelAdmin):
    list_display = ('user_profile', 'question', 'selected_option')
    search_fields = ('user_profile__user__username', 'question__question_text')
    list_filter = ('question', 'selected_option')

# Register the CreditScore model
@admin.register(CreditScore)
class CreditScoreAdmin(admin.ModelAdmin):
    list_display = ('user_profile', 'score', 'timestamp')
    search_fields = ('user_profile__user__username',)
    list_filter = ('score',)

# Register the models
admin.site.register(Question, QuestionAdmin)
admin.site.register(Option)
