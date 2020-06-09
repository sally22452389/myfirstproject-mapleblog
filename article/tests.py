from django.test import TestCase

import datetime
from django.utils import timezone
from article.models import ArticlePost
from django.contrib.auth.models import User
from time import sleep
from django.urls import reverse

# Create your tests here.

class ArticlePostModelTests(TestCase):

    def test_was_created_recently_with_future_article(self):
        # 若文章創建時間為未來，返回False 
        author = User(username='user', password='test_password')
        author.save()

        future_article = ArticlePost(
            author=author,
            title='test',
            body='test',
            created=timezone.now() + datetime.timedelta(days=30)
            )
        # 斷言肯定
        self.assertIs(future_article.was_created_recently(), False)

    def test_was_created_recently_with_seconds_before_article(self):
        # 若文章創建時間為1分鐘內，返回True 
        author = User(username='user1', password='test_password')
        author.save()
        seconds_before_article = ArticlePost(
            author=author,
            title='test1',
            body='test1',
            created=timezone.now() - datetime.timedelta(seconds=45)
            )
        self.assertIs(seconds_before_article.was_created_recently(), True)

    def test_was_created_recently_with_hours_before_article(self):
        # 若文章創建時間為幾小時前，返回False 
        author = User(username='user2', password='test_password')
        author.save()
        hours_before_article = ArticlePost(
            author=author,
            title='test2',
            body='test2',
            created=timezone.now() - datetime.timedelta(hours=3)
            )
        self.assertIs(hours_before_article.was_created_recently(), False)

    def test_was_created_recently_with_days_before_article(self):
        # 若文章創建時間為幾天前，返回False 
        author = User(username='user3', password='test_password')
        author.save()
        months_before_article = ArticlePost(
            author=author,
            title='test3',
            body='test3',
            created=timezone.now() - datetime.timedelta(days=5)
            )
        self.assertIs(months_before_article.was_created_recently(), False)


class ArtitclePostViewTests(TestCase):

    def test_increase_views(self):
        # 請求詳情視圖時，閱讀量+1 
        author = User(username='user4', password='test_password')
        author.save()
        article = ArticlePost(
            author=author,
            title='test4',
            body='test4',
            )
        article.save()
        self.assertIs(article.total_views, 0)

        url = reverse('article:article_detail', args=(article.id,))
        # 回應
        response = self.client.get(url)

        viewed_article = ArticlePost.objects.get(id=article.id)
        self.assertIs(viewed_article.total_views, 1)

    def test_increase_views_but_not_change_updated_field(self):
        # 請求詳情視圖時，不改變updated字段
        author = User(username='user5', password='test_password')
        author.save()
        article = ArticlePost(
            author=author,
            title='test5',
            body='test5',
            )
        article.save()

        sleep(0.5)

        url = reverse('article:article_detail', args=(article.id,))
        response = self.client.get(url)

        viewed_article = ArticlePost.objects.get(id=article.id)
        self.assertIs(viewed_article.updated - viewed_article.created < timezone.timedelta(seconds=0.1), True)