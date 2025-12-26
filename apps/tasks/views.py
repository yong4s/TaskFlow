from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse, QueryDict
from django.shortcuts import render
from django.views import View

from apps.tasks.forms import TaskCreateForm, TaskUpdateForm
from apps.tasks.services import TaskService


class BaseTaskView(LoginRequiredMixin, View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = TaskService()


class TaskCreateView(BaseTaskView):
    def post(self, request: HttpRequest, project_id: int) -> HttpResponse:
        form = TaskCreateForm(request.POST)
        if form.is_valid():
            task = self.service.create_task(
                user=request.user,
                project_id=project_id,
                title=form.cleaned_data['name'],
                deadline=form.cleaned_data.get('deadline'),
            )
            return render(request, 'partials/task_row.html', {'task': task})

        return render(
            request,
            'partials/task_create_form.html',
            {'form': form, 'project_id': project_id},
            status=422
        )


class TaskResourceView(BaseTaskView):
    def patch(self, request: HttpRequest, task_id: int) -> HttpResponse:
        if request.content_type == 'application/x-www-form-urlencoded' and request.body:
            data = QueryDict(request.body)
        else:
            data = request.POST

        form = TaskUpdateForm(data)
        if form.is_valid():
            update_data = {'title': form.cleaned_data['name']}
            if form.cleaned_data.get('priority'):
                update_data['priority'] = form.cleaned_data['priority']
            if form.cleaned_data.get('deadline'):
                update_data['deadline'] = form.cleaned_data['deadline']

            task = self.service.update_task(user=request.user, task_id=task_id, **update_data)
            tasks = self.service.get_project_tasks_sorted(request.user, task.project.id)
            return render(request, 'partials/task_list.html', {'tasks': tasks, 'project_id': task.project.id})

        task = self.service.get_user_task(request.user, task_id)
        return render(request, 'partials/task_edit_form.html', {'task': task, 'form_errors': form.errors}, status=422)

    def delete(self, request: HttpRequest, task_id: int) -> HttpResponse:
        self.service.delete_task(request.user, task_id)
        return HttpResponse('')


class TaskToggleView(BaseTaskView):
    def post(self, request: HttpRequest, task_id: int) -> HttpResponse:
        task = self.service.toggle_task_status(request.user, task_id)
        tasks = self.service.get_project_tasks_sorted(request.user, task.project.id)
        return render(request, 'partials/task_list.html', {'tasks': tasks, 'project_id': task.project.id})



class TaskEditFormView(BaseTaskView):
    def get(self, request: HttpRequest, task_id: int) -> HttpResponse:
        task = self.service.get_user_task(request.user, task_id)
        return render(request, 'partials/task_edit_form.html', {'task': task})


class TaskCancelEditView(BaseTaskView):
    def get(self, request: HttpRequest, task_id: int) -> HttpResponse:
        task = self.service.get_user_task(request.user, task_id)
        return render(request, 'partials/task_row.html', {'task': task})
