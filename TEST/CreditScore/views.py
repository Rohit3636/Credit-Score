from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import UserProfile, UserResponse, Option, CreditScore, Question
import json
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages

def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home') 
        else:
            messages.error(request, "Invalid Username or Password!")
            return redirect('login')

    return render(request, 'CreditScore/login.html')

@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def home(request):
    questions = Question.objects.prefetch_related('option_set').all()
    questions_data = [
        {
            'id': question.id,
            'text': question.question_text,
            'options': [{'id': option.id, 'text': option.option_text} for option in question.option_set.all()]
        }
        for question in questions
    ]

    # Fetching all credit scores for the logged-in user and sorting them by the latest timestamp
    user_profile = UserProfile.objects.get(user=request.user)
    credit_scores = CreditScore.objects.filter(user_profile=user_profile).order_by('-timestamp')

    context = {
        'questions_data': json.dumps(questions_data),
        'credit_scores': credit_scores  
    }
    return render(request, 'CreditScore/dashboard.html', context)


@login_required(login_url='login')
@csrf_protect
def submit_responses(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        responses = data.get('responses')

        # Get the authenticated user's UserProfile
        user_profile = UserProfile.objects.get(user=request.user)

        if not responses:
            return JsonResponse({'success': False, 'error': 'No responses provided'})

        total_score = 0

        # Save each response and calculate the total score
        for question_id, option_text in responses.items():
            try:
                option = Option.objects.get(question_id=question_id, option_text=option_text)
                UserResponse.objects.create(
                    user_profile=user_profile,
                    question_id=question_id,
                    selected_option=option
                )
                total_score += option.weightage
            except Option.DoesNotExist:
                return JsonResponse({'success': False, 'error': f'Option not found for question {question_id}'})

        # Cap the score at 900
        final_score = min(total_score, 900)

        # Create a new credit score entry for the user
        CreditScore.objects.create(
            user_profile=user_profile,
            score=final_score
        )

        return JsonResponse({'success': True, 'credit_score': final_score})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})



