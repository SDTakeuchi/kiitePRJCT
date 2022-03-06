from django.test import TestCase, Client, tag
from django.urls import reverse
from km.views import homeView, newView
from km.models import Post, Tag
import json

class TestViews(TestCase):
    def setUp(self):
        self.home_url = reverse('home')
        self.login_url = reverse('login')
        self.new_post_url = reverse('postNew')
        self.tag = Tag(name="test_tag", ordering_number=100)
        self.tag.save()
        self.client = Client()
        self.post1 = Post.objects.create(
            title='Help meeee',
            tag=self.tag,
            body='Hold on a sec',
            is_public=True,
            user_is_anonymous=True
        )

    def test_home_view_GET(self):
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_login_POST(self):
        response1 = self.client.get(self.login_url)
        response2 = self.client.post(
            '/accounts/login',
            {'username': 'doug@email.com', 'password': 'strongpassword123123'}
        )
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response2.status_code, 301)

    def test_new_post_POST(self):
        self.client.login(username='doug@email.com', password='strongpassword123123')
        # self.client.force_login(user, backend=None)
        response = self.client.post(self.new_post_url, {
            'title': 'Help me',
            'Tag':self.tag,
            'body':'助けて'
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.post1.title, 'Help meeee')