from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Candidate, Question, Option,  Category,  CategorySuggestion, CategoryResult
from collections import defaultdict

# Base Page (Login)
def base(request):
    return render(request, 'quiz/base.html')

# Home Page

def home(request):
    # Retrieve the candidate ID from the session
    candidate_id = request.session.get('candidate_id')
    if not candidate_id:
        return redirect('base')  # Redirect to the base page if not logged in

    # Fetch the candidate object
    candidate = Candidate.objects.get(id=candidate_id)

    # Check if the candidate's result exists in CategoryResult
    result_exists = CategoryResult.objects.filter(candidate=candidate).exists()

    # Pass the result_exists flag to the template
    return render(request, 'quiz/home.html', {
        'candidate': candidate,
        'result_exists': result_exists,
    })

# Quiz Page
def quiz(request):
    candidate_id = request.session.get('candidate_id')
    if not candidate_id:
        return redirect('base')

    candidate = Candidate.objects.get(id=candidate_id)
    questions = Question.objects.all()

    if request.method == 'POST':
        category_marks = defaultdict(int)  # To store total marks per category

        # Calculate marks for each category
        for question in questions:
            selected_option = request.POST.get(str(question.id))  # Get the selected option ID for the question
            if selected_option:
                try:
                    option = Option.objects.get(id=selected_option)
                    category_marks[question.category.id] += option.marks  # Add marks to the respective category
                except Option.DoesNotExist:
                    messages.error(request, f"Option with ID {selected_option} does not exist.")
                    return redirect('quiz')

        # Save results for each category
        for category_id, marks in category_marks.items():
            category = Category.objects.get(id=category_id)
            suggestion = get_category_suggestion(category, marks)

            # Save category result
            CategoryResult.objects.create(
                candidate=candidate,
                category=category,
                total_marks=marks,
                suggestion=suggestion
            )

        # Redirect to the dashboard or results page
        return redirect('dashboard')

    return render(request, 'quiz/quiz.html', {'questions': questions})

# Dashboard Page
def dashboard(request):
    candidate_id = request.session.get('candidate_id')
    if not candidate_id:
        return redirect('base')

    # Fetch the logged-in candidate
    candidate = Candidate.objects.get(id=candidate_id)

    # Retrieve category-wise results for the candidate
    category_results = CategoryResult.objects.filter(candidate=candidate)

    # Prepare results in the format required by the template
    result_details = [
        {
            "category": result.category.name,
            "total_marks": result.total_marks,
            "suggestion": result.suggestion
        }
        for result in category_results
    ]

    return render(request, 'quiz/dashboard.html', {
        'candidate': candidate,
        'result_details': result_details,
    })




# Saved Reports Page
def saved_reports(request):
    candidate_id = request.session.get('candidate_id')
    if not candidate_id:
        return redirect('base')

    candidate = Candidate.objects.get(id=candidate_id)
    category_results = CategoryResult.objects.filter(candidate=candidate)  # Retrieve category-wise results

    return render(request, 'quiz/saved_reports.html', {
        'candidate': candidate,
        'category_results': category_results,
    })

# Login Page
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        code = request.POST.get('code')
        try:
            candidate = Candidate.objects.get(email=email, unique_code=code)
            request.session['candidate_id'] = candidate.id
            return redirect('home')
        except Candidate.DoesNotExist:
            messages.error(request, 'Invalid email or code')
    return render(request, 'quiz/Login.html')

# Contact Page
def contact_view(request):
    return render(request, 'quiz/contact.html')

def get_category_suggestion(category, category_marks):
    # Fetch all suggestions for the category
    suggestions = CategorySuggestion.objects.filter(category=category)
    
    for suggestion in suggestions:
        # If the category marks are within the range, return the suggestion
        if suggestion.start_marks <= category_marks <= suggestion.end_marks:
            return suggestion.suggestion
    
    # Default suggestion if no range is matched
    return "No suggestion available for this score."


def calculate_results(request):
    # Get the candidate (assuming candidate is logged in and stored in session)
    candidate_id = request.session.get('candidate_id')
    if not candidate_id:
        return render(request, 'error.html', {"message": "Candidate not logged in!"})

    candidate = Candidate.objects.get(id=candidate_id)

    # Get POST data (selected options)
    responses = request.POST
    print("Responses:", responses)  # Debugging: Print submitted data

    # Initialize results
    category_results = []

    # Iterate through all categories
    categories = Category.objects.all()
    for category in categories:
        category_questions = Question.objects.filter(category=category)
        total_marks = 0

        # Calculate total marks for the category
        for question in category_questions:
            selected_option_id = responses.get(f'question_{question.id}')
            print(f"Question {question.id} selected option ID: {selected_option_id}")  # Debugging

            if selected_option_id:
                try:
                    selected_option = Option.objects.get(id=selected_option_id)
                    total_marks += selected_option.marks
                except Option.DoesNotExist:
                    print(f"Option with ID {selected_option_id} does not exist.")  # Debugging

        # Fetch the appropriate suggestion based on total marks
        suggestion_obj = CategorySuggestion.objects.filter(
            category=category,
            start_marks__lte=total_marks,
            end_marks__gte=total_marks
        ).first()

        suggestion = suggestion_obj.suggestion if suggestion_obj else "No suggestion available"
        print(f"Category: {category.name}, Total Marks: {total_marks}, Suggestion: {suggestion}")  # Debugging

        # Append result for the category
        category_results.append({
            "category_name": category.name,
            "total_marks": total_marks,
            "suggestion": suggestion
        })

   
def get_category_suggestion(category, category_marks):
    suggestions = CategorySuggestion.objects.filter(category=category)
    print(f"Category: {category.name}, Marks: {category_marks}, Suggestions: {suggestions}")

    for suggestion in suggestions:
        if suggestion.start_marks <= category_marks <= suggestion.end_marks:
            print(f"Matched Suggestion: {suggestion.suggestion}")
            return suggestion.suggestion

    print("No matching suggestion found.")
    return "No suggestion available for this score."


def about_us(request):
    return render(request, 'quiz/AboutUs.html')