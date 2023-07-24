from django.contrib.auth import get_user_model
from news.models import News, Comment
import pytest

User = get_user_model()


@pytest.fixture
def client_loggin(client, author):
    client.force_login(author)
    return client


@pytest.fixture
def form_data():
    return {'text': 'Текст комментария'}


@pytest.fixture
def news():
    return News.objects.create(title='Заголовок', text='Текст')


@pytest.fixture
def author():
    return User.objects.create(username='Автор')


@pytest.fixture
def reader():
    return User.objects.create(username='Читатель простой')


@pytest.fixture
def comment(news, author):
    return Comment.objects.create(
        news=news,
        author=author,
        text='Текст комментария'
    )


@pytest.fixture
def second_news():
    return [
        News.objects.create(title=f'Заголовок {i}', text=f'Текст {i}')
        for i in range(3)
    ]


@pytest.fixture
def second_comments(second_news, author):
    return [
        Comment.objects.create(
            news=second_news[0],
            author=author,
            text=f'Текст комментария {i}'
        )
        for i in range(3)
    ]
