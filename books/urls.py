from django.urls import path

from .views import BookListView, BookDetailView, AddReviewView, EditReviewView, ConfirmDeleteReviewView, DeleteReviewView

app_name = 'books'
urlpatterns = [
    path('', BookListView.as_view(), name='list'),
    path('<int:id>/', BookDetailView.as_view(), name='detail'),
    path('<int:id>/review/', AddReviewView.as_view(), name='add_review'),
    path('<int:book_id>/book/<int:review_id>/review/edit/', EditReviewView.as_view(), name='edit_review'),
    path('<int:book_id>/book/<int:review_id>/review/confirm/delete.', ConfirmDeleteReviewView.as_view(), name='confirm_delete_review'),
    path('<int:book_id>/book/<int:review_id>/review/delete/', DeleteReviewView.as_view(),
         name='delete_review'),

]