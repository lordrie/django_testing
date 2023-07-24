from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from notes.models import Note


class TestContent(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create_user(username='author',
                                              password='testpass')
        cls.note = Note.objects.create(title='Test Note', text='Test Text',
                                       author=cls.author)
        cls.other_user = User.objects.create_user(username='other_user',
                                                  password='testpass')
        cls.other_note = Note.objects.create(title='Other Test Note',
                                             text='Other Test Text',
                                             author=cls.other_user)

    def setUp(self):
        self.client.login(username='author', password='testpass')

    def test_note_in_object_list(self):
        """Тестирование наличия заметки в списке object_list"""
        response = self.client.get(reverse('notes:list'))
        notes = response.context['object_list']
        self.assertIn(self.note, notes)

    def test_other_user_notes_not_in_list(self):
        """Тестирование отсутствия заметок другого пользователя"""
        response = self.client.get(reverse('notes:list'))
        notes = response.context['object_list']
        self.assertIn(self.note, notes)
        self.assertNotIn(self.other_note, notes)

    def test_page_has_form(self):
        """На страницы создания и редактирования заметки передаются формы."""
        urls = [reverse('notes:add'),
                reverse('notes:edit', args=[self.note.slug])]
        for url in urls:
            response = self.client.get(url)
            self.assertIn('form', response.context)
