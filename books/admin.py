from django.contrib import admin
from .models import Book, Author, BookAuthor, BookReview

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'isbn', 'description', )
    search_fields = ('title', 'isbn', )


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', )
    search_fields = ('first_name', 'last_name', 'email', )


class BookAuthorAdmin(admin.ModelAdmin):
    list_display = ('book', 'author', )
    list_filter = ('author', )
    search_fields = ('book', 'author', )


class BookReviewAdmin(admin.ModelAdmin):
    list_display = ('author', 'comment')
    search_fields = ('author', 'comment')
    list_filter = ('author', )


admin.site.register(Book, BookAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(BookAuthor, BookAuthorAdmin)
admin.site.register(BookReview, BookReviewAdmin)

