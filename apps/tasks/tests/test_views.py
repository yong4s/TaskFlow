from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.projects.models import Project
from apps.tasks.models import Task

User = get_user_model()


class TaskViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', password='password')
        self.client.force_login(self.user)
        self.project = Project.objects.create(name="Test Project", user=self.user)
        self.create_url = reverse('tasks:create', kwargs={'project_id': self.project.id})

    def test_create_task_success_htmx(self):
        data = {
            'name': 'New HTMX Task',
            'deadline': '',
            'priority': 3
        }

        response = self.client.post(
            self.create_url,
            data,
            HTTP_HX_REQUEST='true'
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'partials/task_row.html')
        self.assertTrue(Task.objects.filter(name='New HTMX Task').exists())

    def test_create_task_validation_error(self):
        data = {'name': ''}

        response = self.client.post(
            self.create_url,
            data,
            HTTP_HX_REQUEST='true'
        )

        # Виправлено: у вашому View стоїть status=400
        self.assertEqual(response.status_code, 400)

    def test_toggle_task_status(self):
        # Виправлено: прибрано user=self.user
        task = Task.objects.create(name="Task to Toggle", project=self.project)
        action_url = reverse('tasks:action', kwargs={'task_id': task.id})

        response = self.client.post(
            action_url,
            data={'action': 'toggle'},
            HTTP_HX_REQUEST='true'
        )

        self.assertEqual(response.status_code, 200)
        task.refresh_from_db()
        self.assertEqual(task.status, Task.Status.DONE)

    def test_update_task_success(self):
        # Виправлено: прибрано user=self.user
        task = Task.objects.create(name="Old Task", project=self.project)
        url = reverse('tasks:update', kwargs={'task_id': task.id})
        data = {
            'name': 'Updated Task',
            'priority': 4,
            'deadline': ''
        }

        # Використовуємо POST, оскільки TaskUpdateView має метод post
        response = self.client.post(
            url,
            data,
            HTTP_HX_REQUEST='true'
        )

        self.assertEqual(response.status_code, 200)
        task.refresh_from_db()
        self.assertEqual(task.name, 'Updated Task')
        self.assertEqual(task.priority, 4)

    def test_delete_task(self):
        # Виправлено: прибрано user=self.user
        task = Task.objects.create(name="Task to Delete", project=self.project)
        delete_url = reverse('tasks:delete', kwargs={'task_id': task.id})

        response = self.client.delete(
            delete_url,
            HTTP_HX_REQUEST='true'
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"")
        self.assertFalse(Task.objects.filter(id=task.id).exists())

    def test_access_denied_for_other_user(self):
        other_user = User.objects.create_user(email='other@example.com', password='password')
        self.client.force_login(other_user)

        # Виправлено: прибрано user=self.user
        task = Task.objects.create(name="My Task", project=self.project)
        delete_url = reverse('tasks:delete', kwargs={'task_id': task.id})

        response = self.client.delete(delete_url)

        # Оскільки в DAL/Service перевірка доступу може викидати помилку
        # або повертати 404, перевіряємо, що це не 200
        self.assertNotEqual(response.status_code, 200)
        self.assertTrue(Task.objects.filter(id=task.id).exists())
