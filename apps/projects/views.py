from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse, QueryDict
from django.shortcuts import render
from django.views import View

from apps.projects.forms import ProjectCreateForm, ProjectUpdateForm
from apps.projects.services import ProjectService


class BaseProjectView(LoginRequiredMixin, View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = ProjectService()


class ProjectListView(BaseProjectView):
    def get(self, request: HttpRequest) -> HttpResponse:
        projects = self.service.get_user_projects_with_tasks(request.user)
        create_form = ProjectCreateForm()
        return render(request, 'home.html', {
            'projects': projects,
            'create_form': create_form
        })


class ProjectCreateView(BaseProjectView):
    def get(self, request: HttpRequest) -> HttpResponse:
        form = ProjectCreateForm()
        return render(request, 'partials/project_create_form.html', {'form': form})

    def post(self, request: HttpRequest) -> HttpResponse:
        form = ProjectCreateForm(request.POST)
        if form.is_valid():
            project = self.service.create_project(
                user=request.user,
                name=form.cleaned_data['name']
            )
            return render(request, 'partials/project_card.html', {'project': project})

        return render(
            request,
            'partials/project_create_form.html',
            {'form': form},
            status=422
        )


class ProjectResourceView(BaseProjectView):
    def get(self, request: HttpRequest, project_id: int) -> HttpResponse:
        project = self.service.get_user_project(request.user, project_id)
        return render(request, 'partials/project_card.html', {'project': project})

    def patch(self, request: HttpRequest, project_id: int) -> HttpResponse:
        if request.content_type == 'application/x-www-form-urlencoded' and request.body:
            data = QueryDict(request.body)
        else:
            data = request.POST

        form = ProjectUpdateForm(data)
        if form.is_valid():
            project = self.service.update_project(
                user=request.user,
                project_id=project_id,
                name=form.cleaned_data['name']
            )
            return render(request, 'partials/project_card.html', {'project': project})

        project = self.service.get_user_project(request.user, project_id)
        return render(
            request,
            'partials/project_card.html',
            {'project': project, 'form_errors': form.errors, 'editing_mode': True},
            status=422,
        )

    def delete(self, request: HttpRequest, project_id: int) -> HttpResponse:
        self.service.delete_project(request.user, project_id)
        return HttpResponse('')


class ProjectEditFormView(BaseProjectView):
    def get(self, request: HttpRequest, project_id: int) -> HttpResponse:
        project = self.service.get_user_project(request.user, project_id)
        return render(request, 'partials/project_card.html', {
            'project': project,
            'editing_mode': True
        })
