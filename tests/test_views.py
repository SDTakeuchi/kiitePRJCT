from django.test import TestCase, Client
from django.urls import reverse
from km.views import homeView, newView
from km.models import Post
import json

class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.home_url = reverse('home')
        self.login_url = reverse('login')
        self.new_post_url = reverse('postNew')
        self.post1 = Post.objects.create(
            title='Help meeee',
            tag='その他',
            body='Hold on a sec'
        )

    def test_home_view_GET(self):
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_login_POST(self):
        response = self.client.get(self.login_url)
        response = Client().post('/login', {'username': 'takeuchidouglas@gmail.com', 'password': 'shuheitakeuchi'})
        self.assertEqual(response.status_code, 301)

    def test_new_post_POST(self):
        self.client.login(username='takeuchidouglas@gmail.com', password='shuheitakeuchi')
        # self.client.force_login(user, backend=None)
        response = self.client.post(self.new_post_url, {
            'title': 'Help me',
            'Tag':'その他',
            'body':'助けて'
        })

        self.assertEqual(response.status_code,302)
        self.assertEqual(self.post1.title, 'Help meee')