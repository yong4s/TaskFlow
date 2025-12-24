from django.urls import path

from apps.tasks import views

app_name = 'tasks'

urlpatterns = [
    path('<int:project_id>/create/', views.TaskCreateView.as_view(), name='create'),
    path('<int:task_id>/update/', views.TaskUpdateView.as_view(), name='update'),
    path('<int:task_id>/delete/', views.TaskDeleteView.as_view(), name='delete'),
    path('<int:task_id>/toggle/', views.TaskToggleView.as_view(), name='toggle'),
    path('<int:task_id>/edit/', views.TaskEditFormView.as_view(), name='edit_form'),
    path('<int:task_id>/cancel/', views.TaskCancelEditView.as_view(), name='cancel_edit'),
]
