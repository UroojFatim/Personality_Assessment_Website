from django.urls import path
from . import views

urlpatterns = [
    path('', views.base, name='base'),  # Base page (Login)
    path('home/', views.home, name='home'),  # Home page (after login)
    path('login/', views.login_view, name='login'), 
    path('contact/', views.contact_view, name='contact'), 
    path('about-us/', views.about_us, name='about_us'), 
    path('quiz/', views.quiz, name='quiz'),  # Quiz page
    path('dashboard/', views.dashboard, name='dashboard'),  # Dashboard (results and details)
    path('reports/', views.saved_reports, name='saved_reports'),
]
