from django.contrib.auth import get_user_model
from django.urls import reverse
from news.models import News, Comment
import pytest

User = get_user_model()
NEWS_COUNT = 15
COMMENTS_COUNT = 3
SECOND_NEWS_COUNT = 3


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
        for i in range(SECOND_NEWS_COUNT)
    ]


@pytest.fixture
def second_comments(second_news, author):
    return [
        Comment.objects.create(
            news=second_news[0],
            author=author,
            text=f'Текст комментария {i}'
        )
        for i in range(COMMENTS_COUNT)
    ]


@pytest.fixture
def home_url():
    return reverse('news:home')


@pytest.fixture
def сomments_url():
    return reverse('news:detail', args=(news.id,))


@pytest.fixture
def news_detail_url(news):
    return reverse('news:detail', args=(news.id,))
