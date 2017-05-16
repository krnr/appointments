from django.core.urlresolvers import resolve
from django.test import TestCase

from .views import main_view


class MainViewTest(TestCase):
    """docstring for MainViewTest"""
    def test_index_resolve_correct_view(self):
        view = resolve('/')
        self.assertEqual(view.func, main_view)

    def test_index_renders_correct_html(self):
        resp = self.client.get('/')
        self.assertIn(b'JINJA', resp.content)
