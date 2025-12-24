from django.urls import path

from apps.tasks import views

app_name = 'tasks'

urlpatterns = [
    path('<int:project_id>/create/', views.TaskCreateView.as_view(), name='create'),
    path('<int:task_id>/', views.TaskResourceView.as_view(), name='resource'),
    path('<int:task_id>/toggle/', views.TaskToggleView.as_view(), name='toggle'),
    path('<int:task_id>/edit-form/', views.TaskEditFormView.as_view(), name='edit_form'),
    path('<int:task_id>/cancel/', views.TaskCancelEditView.as_view(), name='cancel'),
]
