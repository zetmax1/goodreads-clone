from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from books.models import Book, BookReview
from users.models import CustomUser


class BookReviewAPITestCase(APITestCase):

    def setUp(self):
        self.user = CustomUser.objects.create(username='Ali', first_name="Ali", last_name='Vali')
        self.user.set_password('!2345678')
        self.user.save()

        self.client.login(username='Ali', password='!2345678')


    def test_book_review_detail_api(self):
        book = Book.objects.create(title='sport', description='description1', isbn='123121')
        review = BookReview.objects.create(book=book, author=self.user, stars_given=5, comment='Nice book')

        response = self.client.get(reverse('api:reviews-detail', kwargs={'id': review.id}))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], review.id)
        self.assertEqual(response.data['stars_given'], 5)
        self.assertEqual(response.data['comment'], 'Nice book')
        self.assertEqual(response.data['book']['id'], review.book.id)
        self.assertEqual(response.data['book']['title'], 'sport')
        self.assertEqual(response.data['book']['description'], 'description1')
        self.assertEqual(response.data['book']['isbn'], '123121')

        self.assertEqual(response.data['author']['id'], review.author.id)
        self.assertEqual(response.data['author']['username'], 'Ali')
        self.assertEqual(response.data['author']['first_name'], 'Ali')


    def test_book_list_api(self):
        book1 = Book.objects.create(title='sport', description='description1', isbn='123121')
        review1 = BookReview.objects.create(book=book1, author=self.user, stars_given=5, comment='Nice book')

        book2 = Book.objects.create(title='apple', description='description2', isbn='99123121')
        review2 = BookReview.objects.create(book=book2, author=self.user, stars_given=3, comment='Not bad')

        response = self.client.get(reverse('api:reviews-list'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 2)
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)

        self.assertEqual(response.data['results'][0]['id'], review2.id)
        self.assertEqual(response.data['results'][0]['comment'], "Not bad")
        self.assertEqual(response.data['results'][1]['id'], review1.id)
        self.assertEqual(response.data['results'][1]['comment'], "Nice book")


    def test_review_delete(self):
        book = Book.objects.create(title='sport', description='description1', isbn='123121')
        review = BookReview.objects.create(book=book, author=self.user, stars_given=5, comment='Nice book')

        response = self.client.delete(reverse('api:reviews-detail', kwargs={'id': review.id}))
        all_reviews = book.bookreview_set.all()

        self.assertEqual(len(all_reviews), 0)
        self.assertEqual(response.status_code, 204)


    def test_review_update(self):
        book = Book.objects.create(title='sport', description='description1', isbn='123121')
        review = BookReview.objects.create(book=book, author=self.user, stars_given=5, comment='Nice book')

        response = self.client.patch(reverse('api:reviews-detail', kwargs={'id': review.id}),
                                     data={
                                         "stars_given": 4,
                                         'comment': 'I enjoyed reading this book'
                                     })

        review.refresh_from_db()


        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['comment'], 'I enjoyed reading this book')
        self.assertEqual(response.data['stars_given'], 4)


    def test_review_add(self):
        book = Book.objects.create(title='sport', description='description1', isbn='123121')
        book2 = Book.objects.create(title='apple', description='description2', isbn='99123121')


        response1 = self.client.post(reverse('api:reviews-list'), data={
            'stars_given': 3,
            'comment': 'great',
            'author_id': self.user.id,
            'book_id': book.id
        })

        response2 = self.client.post(reverse('api:reviews-list'), data={
            'stars_given': 5,
            'comment': 'excellent',
            'author_id': self.user.id,
            'book_id': book2.id
        })

        self.assertEqual(response1.data['stars_given'], 3)
        self.assertEqual(response1.status_code, 201)
        self.assertEqual(response1.data['comment'], 'great')
        self.assertEqual(response1.data['author']['id'], self.user.id)
        self.assertEqual(response1.data['book']['id'], book.id)

        self.assertNotEqual(response2.data['comment'], 'great')