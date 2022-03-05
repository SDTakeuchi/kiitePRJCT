from django.test import TestCase
from km.models import Tag

class PostModelTests(TestCase):

    def test_is_empty(self):
        """初期状態かチェック"""  
        saved_posts = Tag.objects.all()
        self.assertEqual(saved_posts.count(), 0)

    def test_is_count_one(self):
        """1つレコードを適当に作成すると、レコードが1つだけカウントされることをテスト"""
        current_tags = Tag.objects.all()
        tag = Tag(
            name='name',
            ordering_number=1,
        )
        tag.save()
        incred_tags = Tag.objects.all()
        self.assertEqual(incred_tags.count(), 1)

    def test_saving_and_retrieving_tag(self):
        """内容を指定してデータを保存し、すぐに取り出した時に保存した時と同じ値が返されることをテスト"""
        tag = Tag()

        name="tag"
        ordering_number = 1

        tag.name = name
        tag.ordering_number = ordering_number

        tag.save()

        saevd_tag = Tag.objects.all()[0]

        self.assertEqual(saevd_tag.name, name)
        self.assertEqual(saevd_tag.ordering_number, ordering_number)
