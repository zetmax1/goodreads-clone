from django.test import TestCase
from django.urls import reverse

from books.models import Book, BookReview
from users.models import CustomUser


class HomePageTestCase(TestCase):

    def test_paginated_list(self):
        book = Book.objects.create(title='sport', description='description1', isbn='123121')

        user = CustomUser.objects.create(username='aliy', first_name='Aliy', last_name='Abdullayev',
                                         email='ali@gmail.com')
        user.set_password('!2345678')
        user.save()

        review1 = BookReview.objects.create(book=book, author=user, stars_given=5, comment='Nice book')
        review2 = BookReview.objects.create(book=book, author=user, stars_given=2, comment='not worth to price')
        review3 = BookReview.objects.create(book=book, author=user, stars_given=4, comment='Useful')

        response = self.client.get(
            reverse('home') + '?page_size=2'
        )

        self.assertContains(response, review3.comment)
        self.assertContains(response, review2.comment)
        self.assertNotContains(response, review1.comment)
