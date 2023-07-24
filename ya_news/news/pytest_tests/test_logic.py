import pytest
from django.urls import reverse
from news.models import Comment
from news.forms import BAD_WORDS, WARNING
from http import HTTPStatus


@pytest.mark.django_db
def test_anonymous_user_cant_create_comment(client, news, form_data):
    """
    Тест проверяет, что анонимный пользователь не может отправить комментарий.
    """
    url = reverse('news:detail', args=(news.id,))
    client.post(url, data=form_data)
    assert Comment.objects.count() == 0


@pytest.mark.django_db
def test_user_can_create_comment(client_loggin,
                                 client, news, author, form_data):
    """
    Авторизованный пользователь может отправить комментарий.
    """
    url = reverse('news:detail', args=(news.id,))
    response = client_loggin.post(url, data=form_data)
    assert response.status_code == 302
    assert response.url == f'{url}#comments'
    comments_count = Comment.objects.count()
    assert comments_count == 1
    comment = Comment.objects.first()
    assert comment.text == form_data['text']
    assert comment.news == news
    assert comment.author == author


@pytest.mark.django_db
def test_user_cant_use_bad_words(client_loggin, news):
    """Если комментарий содержит запрещённые слова,
    он не будет опубликован, а форма вернёт ошибку."""
    url = reverse('news:detail', args=(news.id,))
    form_data = {'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'}
    response = client_loggin.post(url, data=form_data)
    assert response.status_code == 200
    form = response.context['form']
    assert form.errors['text'] == [WARNING]
    assert Comment.objects.count() == 0


@pytest.mark.django_db
def test_user_can_edit_own_comment(client_loggin, news, comment):
    """Авторизованный пользователь может редактировать свои комментарии."""
    url = reverse('news:edit', args=(comment.id,))
    form_data = {'text': 'Обновленный текст комментария'}
    response = client_loggin.post(url, data=form_data)
    assert response.status_code == 302
    assert response.url == reverse(
        'news:detail', args=(news.id,)) + '#comments'
    comment.refresh_from_db()
    assert comment.text == form_data['text']


@pytest.mark.django_db
def test_user_can_delete_own_comment(client_loggin, news, comment):
    """Авторизованный пользователь может удалять свои комментарии."""
    url = reverse('news:delete', args=(comment.id,))
    response = client_loggin.delete(url)
    assert response.status_code == 302
    assert response.url == reverse(
        'news:detail', args=(news.id,)) + '#comments'
    assert Comment.objects.count() == 0


@pytest.mark.django_db
def test_user_cant_edit_comment_of_another_user(client, comment, reader):
    """Авторизованный пользователь не может редактировать чужой комментарий."""
    client.force_login(reader)
    url = reverse('news:edit', args=(comment.id,))
    form_data = {'text': 'Обновленный текст комментария'}
    response = client.post(url, data=form_data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment.refresh_from_db()
    assert comment.text != form_data['text']


@pytest.mark.django_db
def test_user_cant_delete_comment_of_another_user(client,
                                                  comment, reader):
    """Авторизованный пользователь не может удалить чужой комментарий."""
    client.force_login(reader)
    url = reverse('news:delete', args=(comment.id,))
    response = client.delete(url)
    assert response.status_code == HTTPStatus.NOT_FOUND
