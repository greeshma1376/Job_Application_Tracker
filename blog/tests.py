from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import Post

class PostAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.post1 = Post.objects.create(
            title="Internship Opportunity",
            content="New internship opportunities are available for students."
        )
        self.post2 = Post.objects.create(
            title="Job Application Update",
            content="New job application information is available."
        )

    def test_list_posts(self):
        url = reverse('post-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['title'], "Internship Opportunity")

    def test_retrieve_post(self):
        url = reverse('post-detail', kwargs={'pk': self.post1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Internship Opportunity")
        self.assertEqual(response.data['content'], "New internship opportunities are available for students.")

    def test_create_post(self):
        url = reverse('post-list')
        data = {'title': 'New Exam Alert', 'content': 'Exam dates announced.'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Post.objects.filter(title='New Exam Alert').exists())

    def test_update_post(self):
        url = reverse('post-detail', kwargs={'pk': self.post1.id})
        data = {'title': 'Updated Internship', 'content': 'Updated content.'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.post1.refresh_from_db()
        self.assertEqual(self.post1.title, 'Updated Internship')

    def test_delete_post(self):
        url = reverse('post-detail', kwargs={'pk': self.post1.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Post.objects.filter(id=self.post1.id).exists())
