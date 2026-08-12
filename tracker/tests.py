import datetime
from django.test import TestCase, Client
from django.urls import reverse
from .models import Task

class TaskModelTest(TestCase):
    def setUp(self):
        self.task = Task.objects.create(
            title="TCS - Software Developer",
            description="Software development opportunity",
            due_date=datetime.date(2026, 8, 20),
            is_completed=False
        )

    def test_task_creation(self):
        self.assertEqual(self.task.title, "TCS - Software Developer")
        self.assertEqual(self.task.description, "Software development opportunity")
        self.assertEqual(self.task.due_date, datetime.date(2026, 8, 20))
        self.assertFalse(self.task.is_completed)
        self.assertEqual(str(self.task), "TCS - Software Developer")

class TaskViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.task1 = Task.objects.create(
            title="TCS - Software Developer",
            description="Software development opportunity",
            due_date=datetime.date(2026, 8, 20),
            is_completed=False
        )
        self.task2 = Task.objects.create(
            title="Infosys - Systems Engineer",
            description="Graduate software engineering opportunity",
            due_date=datetime.date(2026, 8, 25),
            is_completed=True
        )

    def test_task_list_view(self):
        response = self.client.get(reverse('task_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tracker/task_list.html')
        self.assertContains(response, "TCS - Software Developer")
        self.assertContains(response, "Infosys - Systems Engineer")

    def test_add_task_view(self):
        response = self.client.post(reverse('add_task'), {
            'title': 'Wipro - Project Engineer',
            'description': 'Full time engineering role',
            'due_date': '2026-09-01'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(title='Wipro - Project Engineer').exists())

    def test_ajax_complete_task_view(self):
        url = reverse('complete_task', kwargs={'pk': self.task1.id})
        response = self.client.post(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.json_data = response.json()
        self.assertTrue(self.json_data['success'])
        self.assertEqual(self.json_data['status'], 'Completed')
        
        self.task1.refresh_from_db()
        self.assertTrue(self.task1.is_completed)

    def test_ajax_delete_task_view(self):
        url = reverse('delete_task', kwargs={'pk': self.task1.id})
        response = self.client.post(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.json_data = response.json()
        self.assertTrue(self.json_data['success'])
        
        self.assertFalse(Task.objects.filter(id=self.task1.id).exists())
