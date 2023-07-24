from django.urls import reverse
import pytest
from news.models import News


@pytest.mark.django_db
def test_news_count_on_home_page(client):
    """
    Количество новостей на главной странице — не более 10.
    """
    News.objects.bulk_create([
        News(title=f'Заголовок {i}', text=f'Текст {i}')
        for i in range(15)
    ])
    url = reverse('news:home')
    response = client.get(url)
    assert len(response.context['news_list']) <= 10


@pytest.mark.django_db
def test_news_order_on_home_page(client):
    """
    Новости отсортированы от самой свежей к самой старой.
    Свежие новости в начале списка.
    """
    news = [
        News.objects.create(title=f'Заголовок {i}', text=f'Текст {i}')
        for i in range(3)
    ]
    url = reverse('news:home')
    response = client.get(url)
    news_list = response.context['news_list']
    assert list(news_list) == news


@pytest.mark.django_db
def test_comments_order_on_news_page(client, second_news, second_comments):
    """
    Комментарии на странице отдельной новости отсортированы:
    старые в начале списка, новые — в конце.
    """
    url = reverse('news:detail', args=(second_news[0].id,))
    response = client.get(url)
    comments_list = response.context['news'].comment_set.all()
    assert list(comments_list) == second_comments


@pytest.mark.django_db
def test_comment_form_availability(client, reader, news):
    """
    Анонимному пользователю недоступна форма для
    отправки комментария на странице отдельной новости,
    а авторизованному доступна.
    """
    url = reverse('news:detail', args=(news.id,))
    response = client.get(url)
    assert 'form' not in response.context
    client.force_login(reader)
    response = client.get(url)
    assert 'form' in response.context
