from django.urls import path
from . import views

app_name = 'jobs'

urlpatterns = [
    path('', views.job_list, name='list'),
    path('<int:pk>/', views.job_detail, name='detail'),
    path('<int:pk>/edit/', views.JobUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', views.JobDeleteView.as_view(), name='delete'),
    path('apply/<int:job_id>/', views.apply_view, name='apply'),
]
