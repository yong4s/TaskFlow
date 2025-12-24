from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.projects.models import Project

User = get_user_model()


class ProjectViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', password='testpass123')
        self.client.force_login(self.user)
        self.create_url = reverse('projects:create')
        self.dashboard_url = reverse('projects:list')

    def test_project_list_view(self):
        Project.objects.create(name='Project A', user=self.user)
        Project.objects.create(name='Project B', user=self.user)

        response = self.client.get(self.dashboard_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertEqual(len(response.context['projects']), 2)

    def test_create_project_htmx_success(self):
        data = {'name': 'New Project'}

        response = self.client.post(
            self.create_url,
            data,
            HTTP_HX_REQUEST='true'
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'partials/project_card.html')
        self.assertTrue(Project.objects.filter(name='New Project', user=self.user).exists())

    def test_create_project_validation_error(self):
        data = {'name': ''}

        response = self.client.post(
            self.create_url,
            data,
            HTTP_HX_REQUEST='true'
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'partials/project_create_form.html')
        self.assertContains(response, 'is-invalid')
        self.assertFalse(Project.objects.filter(name='').exists())

    def test_update_project_success(self):
        project = Project.objects.create(name='Old Name', user=self.user)
        url = reverse('projects:update', kwargs={'project_id': project.id})
        data = {'name': 'New Name'}

        response = self.client.patch(
            url,
            data,
            content_type='application/x-www-form-urlencoded',
            HTTP_HX_REQUEST='true'
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'partials/project_card.html')
        project.refresh_from_db()
        self.assertEqual(project.name, 'New Name')

    def test_delete_project_success(self):
        project = Project.objects.create(name='To Delete', user=self.user)
        url = reverse('projects:delete', kwargs={'project_id': project.id})

        response = self.client.delete(
            url,
            HTTP_HX_REQUEST='true'
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'')
        self.assertFalse(Project.objects.filter(id=project.id).exists())
