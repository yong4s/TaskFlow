from django.urls import path

from apps.projects import views

app_name = 'projects'

urlpatterns = [
    path('', views.ProjectListView.as_view(), name='list'),
    path('create/', views.ProjectCreateView.as_view(), name='create'),
    path('<int:project_id>/', views.ProjectDetailView.as_view(), name='detail'),
    path('<int:project_id>/update/', views.ProjectUpdateView.as_view(), name='update'),
    path('<int:project_id>/delete/', views.ProjectDeleteView.as_view(), name='delete'),
]
