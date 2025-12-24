from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.views import View

from apps.projects.forms import ProjectCreateForm
from apps.projects.forms import ProjectForm
from apps.projects.forms import ProjectUpdateForm
from apps.projects.services import ProjectService


class BaseProjectView(LoginRequiredMixin, View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = ProjectService()


class DashboardView(BaseProjectView):
    def get(self, request: HttpRequest) -> HttpResponse:
        projects = self.service.get_user_projects_with_tasks(request.user)
        return render(request, 'home.html', {'projects': projects})


class ProjectListView(BaseProjectView):
    def get(self, request: HttpRequest) -> HttpResponse:
        projects = self.service.get_user_projects_with_tasks(request.user)
        return render(request, 'home.html', {'projects': projects})


class ProjectCreateView(BaseProjectView):
    def get(self, request: HttpRequest) -> HttpResponse:
        form = ProjectCreateForm()
        return render(request, 'partials/project_create_form.html', {'form': form})

    def post(self, request: HttpRequest) -> HttpResponse:
        form = ProjectCreateForm(request.POST)
        if form.is_valid():
            project = self.service.create_project(user=request.user, name=form.cleaned_data['name'])
            return render(request, 'partials/project_card.html', {'project': project})

        return render(request, 'partials/project_create_form.html', {'form': form})


class ProjectUpdateView(BaseProjectView):
    def patch(self, request: HttpRequest, project_id: int) -> HttpResponse:
        from django.http import QueryDict

        if request.content_type == 'application/x-www-form-urlencoded' and request.body:
            data = QueryDict(request.body)
        else:
            data = request.POST

        form = ProjectUpdateForm(data)
        if form.is_valid():
            project = self.service.update_project(
                user=request.user, project_id=project_id, name=form.cleaned_data['name']
            )
            return render(request, 'partials/project_card.html', {'project': project})

        project = self.service.get_user_project(request.user, project_id)
        return render(
            request,
            'partials/project_card.html',
            {'project': project, 'form_errors': form.errors, 'editing_mode': True},
            status=422,
        )


class ProjectDeleteView(BaseProjectView):
    def delete(self, request: HttpRequest, project_id: int) -> HttpResponse:
        self.service.delete_project(request.user, project_id)
        return HttpResponse('')


class ProjectDetailView(BaseProjectView):
    def get(self, request: HttpRequest, project_id: int) -> HttpResponse:
        project = self.service.get_user_project(request.user, project_id)
        return render(request, 'partials/project_card.html', {'project': project})
