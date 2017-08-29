from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string

from welcome_page.views import welcome_page


class WelcomePageTest(TestCase):

    def test_root_urls_resolves_to_welcome_page_view(self):
        found = resolve('/')
        assert found.func == welcome_page

    def test_welcome_page_returns_correct_html(self):
        request = HttpRequest()
        response = welcome_page(request)
        expected_html = render_to_string('home.html')
        assert response.content.decode() == expected_html
