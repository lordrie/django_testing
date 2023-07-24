from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from notes.models import Note
from pytils.translit import slugify

User = get_user_model()


class TestLogic(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser',
                                             password='testpass')
        self.note_data = {'title': 'Test Note', 'text': 'Test Text'}

    def test_logged_in_user_can_create_note(self):
        """Залогиненный пользователь может создать заметку"""
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('notes:add'), self.note_data)
        self.assertRedirects(response, reverse('notes:success'))
        self.assertEqual(Note.objects.count(), 1)

    def test_anonymous_user_cannot_create_note(self):
        """Анонимный пользователь не может создать заметку"""
        response = self.client.post(reverse('notes:add'), self.note_data)
        login_url = reverse('users:login')
        add_url = reverse('notes:add')
        expected_url = f'{login_url}?next={add_url}'
        self.assertRedirects(response, expected_url)
        self.assertEqual(Note.objects.count(), 0)

    def test_cannot_create_two_notes_with_same_slug(self):
        """Невозможно создать две заметки с одинаковым slug"""
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('notes:add'), self.note_data)
        self.assertRedirects(response, reverse('notes:success'))
        self.assertEqual(Note.objects.count(), 1)
        # Попытка создать вторую заметку с тем же заголовком
        response = self.client.post(reverse('notes:add'), self.note_data)
        # Проверка, что вторая заметка не была создана
        self.assertEqual(Note.objects.count(), 1)

    def test_slug_is_generated_automatically(self):
        """Если при создании заметки не заполнен slug,
        то он формируется автоматически"""
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('notes:add'), self.note_data)
        self.assertRedirects(response, reverse('notes:success'))
        note = Note.objects.first()
        expected_slug = slugify(self.note_data['title'])
        self.assertEqual(note.slug, expected_slug)

    def test_user_can_edit_and_delete_own_notes(self):
        """Пользователь может редактировать и удалять свои заметки"""
        self.client.login(username='testuser', password='testpass')
        # Создание заметки
        response = self.client.post(reverse('notes:add'), self.note_data)
        self.assertRedirects(response, reverse('notes:success'))
        note = Note.objects.first()
        # Редактирование заметки
        edit_data = {'title': 'Updated Title', 'text': 'Updated Text'}
        edit_url = reverse('notes:edit', args=[note.slug])
        response = self.client.post(edit_url, edit_data)
        self.assertRedirects(response, reverse('notes:success'))
        note.refresh_from_db()
        self.assertEqual(note.title, edit_data['title'])
        self.assertEqual(note.text, edit_data['text'])
        # Удаление заметки
        delete_url = reverse('notes:delete', args=[note.slug])
        response = self.client.post(delete_url)
        self.assertRedirects(response, reverse('notes:success'))
        self.assertEqual(Note.objects.count(), 0)

    def test_user_cannot_edit_or_delete_other_users_notes(self):
        """Пользователь не может редактировать или удалять чужие заметки"""
        # Создание заметки другим пользователем
        other_user = User.objects.create_user(username='otheruser',
                                              password='testpass')
        other_note = Note.objects.create(title='Other Note', text='Other Text',
                                         author=other_user)
        self.client.login(username='testuser', password='testpass')
        # Попытка редактирования чужой заметки
        edit_data = {'title': 'Updated Title', 'text': 'Updated Text'}
        edit_url = reverse('notes:edit', args=[other_note.slug])
        response = self.client.post(edit_url, edit_data)
        self.assertEqual(response.status_code, 404)
        other_note.refresh_from_db()
        self.assertEqual(other_note.title, 'Other Note')
        self.assertEqual(other_note.text, 'Other Text')
        # Попытка удаления чужой заметки
        delete_url = reverse('notes:delete', args=[other_note.slug])
        response = self.client.post(delete_url)
        self.assertEqual(response.status_code, 404)
