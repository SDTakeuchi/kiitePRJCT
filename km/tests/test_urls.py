from django.test import TestCase
from django.urls import reverse, resolve
from km.views import homeView

class TestUrls(TestCase):

    """index ページへのURLでアクセスする時のリダイレクトをテスト"""
    def test_post_index_url(self):
        url = reverse('home')
        self.assertEqual(resolve(url).func, homeView)