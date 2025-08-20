from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView

from books.forms import AddReviewForm
from books.models import Book, BookReview, Author, BookAuthor, Genre


# class BookListView(ListView):
#     template_name = 'books/list.html'
#     queryset = Book.objects.all()
#     context_object_name = 'books'
#     paginate_by = 2

class BookListView(View):
    def get(self, request):
        books = Book.objects.all().order_by('id')
        search_query = request.GET.get('q')
        if search_query:
            books = books.filter(title__icontains=search_query)

        page_size = request.GET.get('page_size', 2)
        paginator = Paginator(books, page_size)
        page_num = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_num)

        return render(
            request,
            'books/list.html',
            {'page_obj': page_obj, 'search_query': search_query}
        )


# class BookDetailView(DetailView):
#     template_name = 'books/detail.html'
#     model = Book
#     pk_url_kwarg = 'id'


class BookDetailView(View):

    def get(self, request, id):
        book = Book.objects.get(id=id)
        review_form = AddReviewForm()
        return render(request, 'books/detail.html', {'book': book, 'review_form': review_form})


class AddReviewView(View):

    def post(self, request, id):
        book = Book.objects.get(id=id)
        review_form = AddReviewForm(data=request.POST)

        if review_form.is_valid():
            BookReview.objects.create(
                book=book,
                author=request.user,
                stars_given=review_form.cleaned_data['stars_given'],
                comment=review_form.cleaned_data['comment']
            )

            return redirect(reverse("books:detail", kwargs={'id': book.id}))

        return render(request, 'books/detail.html', {'book': book, 'review_form': review_form})


class EditReviewView(View, LoginRequiredMixin):

    def get(self, request, book_id, review_id):
        book = Book.objects.get(id=book_id)
        review = book.bookreview_set.get(id=review_id)
        review_form = AddReviewForm(instance=review)

        return render(request, 'books/edit_review.html', {'review_form': review_form, 'book': book, 'review': review})

    def post(self, request, book_id, review_id):
        book = Book.objects.get(id=book_id)
        review = book.bookreview_set.get(id=review_id)
        review_form = AddReviewForm(instance=review, data=request.POST)

        if review_form.is_valid():
            review_form.save()

            return redirect(reverse("books:detail", kwargs={'id': book.id}))

        return render(request, 'books/edit_review.html', {'review_form': review_form, 'book': book, 'review': review})


class ConfirmDeleteReviewView(View, LoginRequiredMixin):

    def get(self, request, book_id, review_id):
        book = Book.objects.get(id=book_id)
        review = book.bookreview_set.get(id=review_id)

        return render(request, 'books/confirm_review_delete.html', {'book': book, 'review': review})


class DeleteReviewView(LoginRequiredMixin, View):

    def get(self, request, book_id, review_id):
        book = Book.objects.get(id=book_id)
        review = book.bookreview_set.get(id=review_id)

        review.delete()
        messages.success(request, "You've successfully deleted review")

        return redirect(reverse("books:detail", kwargs={'id': book.id}))


class GetAuthorView(View):
    def get(self, request, id):
        author = get_object_or_404(Author, id=id)
        book_authors = author.book_author.all()
        books = [book_author.book for book_author in book_authors]
        context = {
            'author': author,
            'books': books
        }

        return render(request, 'books/book_authors.html', context)


class GetAllAuthorsView(ListView):
    model = Author
    context_object_name = 'authors'
    template_name = 'books/authors.html'

    def get_queryset(self):
        return Author.objects.prefetch_related('genre').all()


class GetGenreView(View):
    def get(self, request, id):
        genre = get_object_or_404(Genre, id=id)

        books = genre.books.prefetch_related('book')

        authors_by_book = {}
        for book in books:
            authors = [i.author for i in book.book.all()]
            authors_by_book[book.id] = authors

        context = {
            'books': books,
            'genre': genre,
            'authors_by_book': authors_by_book,
        }
        print('authors:  ', authors_by_book)

        return render(request, 'books/book_genre.html', context)
