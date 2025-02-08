from django.contrib import admin
from .models import Candidate, Category, Question, Option,  CategorySuggestion, CategoryResult

admin.site.register(Candidate)
admin.site.register(Category)
admin.site.register(Question)
admin.site.register(Option)
admin.site.register(CategorySuggestion) 
admin.site.register(CategoryResult)  # Register the new model