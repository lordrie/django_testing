from django.http import HttpResponse, HttpResponseNotFound
from django.test import TestCase, Client
from django.contrib.auth.models import User
from notes.models import Note


class TestRoutes(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser',
                                            password='testpass')
        cls.author = User.objects.create_user(username='author',
                                              password='testpass')
        cls.other_user = User.objects.create_user(username='other_user',
                                                  password='testpass')
        cls.note = Note.objects.create(title='Test Note', text='Test Text',
                                       author=cls.author)

    def test_homepage_available_to_anonymous_user(self):
        """Главная страница доступна анонимному пользователю."""
        client = Client()
        response = client.get('/')
        self.assertEqual(response.status_code, HttpResponse.status_code)

    def test_authenticated_user_access(self):
        """Доступность страниц для аутентифицированного пользователя"""
        self.client.login(username='testuser', password='testpass')
        urls = ('/notes/', '/done/', '/add/')
        for url in urls:
            with self.subTest(f'Доступность {url} для аут. пользователя'):
                response = self.client.get(url)
                self.assertEqual(response.status_code,
                                 HttpResponse.status_code)

    def test_note_pages_access(self):
        """Удаления и редактирования заметки доступны только автору,
        для других пользователей ошибка 404"""
        users = (('author', HttpResponse.status_code),
                 ('other_user', HttpResponseNotFound.status_code))
        for username, status_code in users:
            self.client.login(username=username, password='testpass')
            urls = (f'/note/{self.note.slug}/',
                    f'/edit/{self.note.slug}/',
                    f'/delete/{self.note.slug}/')
            for url in urls:
                with self.subTest(f'Доступ {url} для {username}'):
                    response = self.client.get(url)
                    self.assertEqual(response.status_code, status_code)
            self.client.logout()

    def test_anonymous_user_redirected_to_login(self):
        """Редирект анонимного пользователя на страницу логина"""
        urls = ('/notes/', '/done/', '/add/',
                f'/note/{self.note.slug}/',
                f'/edit/{self.note.slug}/',
                f'/delete/{self.note.slug}/')
        for url in urls:
            with self.subTest(f'Редирект {url} для анонима'):
                response = self.client.get(url)
                self.assertRedirects(response, f'/auth/login/?next={url}')

    def test_auth_pages_available_to_all_users(self):
        """Страницы регистрации, входа и выхода из неё доступны всем."""
        urls = ('/auth/signup/',
                '/auth/login/',
                '/auth/logout/')
        for url in urls:
            with self.subTest(f'Доступ {url} для всех'):
                response = self.client.get(url)
                self.assertEqual(response.status_code,
                                 HttpResponse.status_code)
