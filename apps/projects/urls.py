from django.urls import path

from apps.projects import views

app_name = 'projects'

urlpatterns = [
    path('', views.ProjectListView.as_view(), name='list'),
    path('create/', views.ProjectCreateView.as_view(), name='create'),
    path('<int:project_id>/', views.ProjectResourceView.as_view(), name='resource'),
]
