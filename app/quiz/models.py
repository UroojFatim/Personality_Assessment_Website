from django.db import models

# Candidate Model
class Candidate(models.Model):
    name = models.CharField(max_length=100)
    profession = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    unique_code = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name

# Category Model
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Question Model
class Question(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    text = models.TextField()
    marks = models.IntegerField()

    def __str__(self):
        return self.text

# Option Model
class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    text = models.CharField(max_length=255)
    marks = models.IntegerField()

    def __str__(self):
        return f"{self.text} ({self.marks} marks)"



    
    
class CategorySuggestion(models.Model):
    category = models.ForeignKey(Category, related_name='suggestions', on_delete=models.CASCADE)
    start_marks = models.IntegerField()
    end_marks = models.IntegerField()
    suggestion = models.TextField()

    def __str__(self):
        return f"{self.category.name}: {self.suggestion} ({self.start_marks}-{self.end_marks})"
    
class CategoryResult(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    total_marks = models.IntegerField()
    suggestion = models.TextField()

    def __str__(self):
        return f"{self.candidate.name} - {self.category.name}: {self.total_marks} marks"