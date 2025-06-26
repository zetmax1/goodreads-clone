from django.test import TestCase
from django.shortcuts import reverse

from users.models import CustomUser
from .models import Book, Author, BookAuthor, BookReview


class BookListTest(TestCase):
    def test_no_book_found(self):
         response = self.client.get(reverse('books:list'))

         self.assertContains(response, 'No books found.', status_code=200)

    def test_book_list(self):
        book1 = Book.objects.create(title='Book1', description='description1', isbn='123121')
        book2 = Book.objects.create(title='Book2', description='description2', isbn='123121464')
        book3 = Book.objects.create(title='Book3', description='description3', isbn='1231215')

        response = self.client.get(reverse('books:list') + '?page_size=2')


        for book in [book1, book2]:
            self.assertContains(response, book.title)
        self.assertNotContains(response, book3.title)

        response = self.client.get(reverse('books:list') + '?page=2&page_size=2')
        self.assertContains(response, book3.title)

    def test_book_detail(self):
        book = Book.objects.create(title='Book1', description='description1', isbn='123121')
        response = self.client.get(reverse('books:detail', kwargs={'id':book.id}))

        self.assertContains(response, book.title)
        self.assertContains(response, book.description)


    def test_search_books(self):
        book1 = Book.objects.create(title='sport', description='description1', isbn='123121')
        book2 = Book.objects.create(title='fear', description='description2', isbn='123121464')
        book3 = Book.objects.create(title='one day', description='description3', isbn='1231215')

        response = self.client.get(reverse('books:list') + '?q=sport')
        self.assertContains(response, book1.title)
        self.assertNotContains(response, book2.title)
        self.assertNotContains(response, book3.title)

        response = self.client.get(reverse('books:list') + '?q=fear')
        self.assertContains(response, book2.title)
        self.assertNotContains(response, book1.title)
        self.assertNotContains(response, book3.title)

        response = self.client.get(reverse('books:list') + '?q=one')
        self.assertContains(response, book3.title)
        self.assertNotContains(response, book2.title)
        self.assertNotContains(response, book1.title)


class BookReviewTestCase(TestCase):

    def test_add_review(self):
        book = Book.objects.create(title='sport', description='description1', isbn='123121')

        user = CustomUser.objects.create(username='aliy', first_name='Aliy', last_name='Abdullayev', email='ali@gmail.com')
        user.set_password('!2345678')
        user.save()

        self.client.login(username='aliy', password='!2345678')

        self.client.post(reverse('books:add_review', kwargs={'id': book.id}),
                         data={
                             'stars_given':5,
                             'comment': 'Nice book'
                         })
        book_reviews = book.bookreview_set.all()

        self.assertEqual(book_reviews.count(), 1)
        self.assertEqual(book_reviews[0].stars_given, 5)
        self.assertEqual(book_reviews[0].comment, 'Nice book')
        self.assertEqual(book_reviews[0].author, user)
        self.assertEqual(book_reviews[0].book, book)


    def test_book_author(self):
        book1 = Book.objects.create(title='sport', description='description1', isbn='123121')
        book2 = Book.objects.create(title='star', description='description2', isbn='12312199')
        author1 = Author.objects.create(first_name='Mark', last_name='Tim', bio='10 years with writing books', email='Mark@gmail.com')
        author2 = Author.objects.create(first_name='Aziz', last_name='Aliyev', bio='point', email='aziz@gmail.com')
        author3 = Author.objects.create(first_name='Qosim', last_name='Umarov', bio='good author', email='qwerty@gmail.com')


        book_author1 = BookAuthor.objects.create(book=book1, author=author1)
        book_author2 = BookAuthor.objects.create(book=book1, author=author2)
        book_author3 = BookAuthor.objects.create(book=book2, author=author3)

        response = self.client.get(reverse('books:detail', kwargs={'id': book1.id}))

        self.assertContains(response, book_author1.author.first_name)
        self.assertContains(response, book_author2.author.full_name())
        self.assertNotContains(response, book_author3.author.full_name())


    def test_book_delete(self):
        book = Book.objects.create(title='sport', description='description1', isbn='123121')
        user = CustomUser.objects.create(username='aliy', first_name='Aliy', last_name='Abdullayev',
                                         email='ali@gmail.com')

        user.set_password('!2345678')
        user.save()

        self.client.login(username='aliy', password='!2345678')
        self.client.post(reverse('books:add_review', kwargs={'id': book.id}),
                         data={
                             'stars_given': 5,
                             'comment': 'Nice book'
                         })
        review = book.bookreview_set.first()
        review_id = review.id
        response = self.client.get(reverse('books:delete_review', kwargs={'book_id': book.id, 'review_id': review_id}))

        remaining_reviews = BookReview.objects.filter(id=review_id).exists()
        self.assertFalse(remaining_reviews)

        self.assertEqual(response.status_code, 302)
