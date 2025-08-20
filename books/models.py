from django.core.validators import MinValueValidator, MaxValueValidator, FileExtensionValidator
from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.utils.text import  slugify
from users.models import CustomUser


class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250)
    description = models.TextField()
    isbn = models.CharField(max_length=20)
    cover_picture = models.ImageField(default='default_book_pic.jpeg', upload_to='books/')
    genre = models.ManyToManyField(Genre, related_name='books')

    def __str__(self):
        return self.title

    # def save(self, *args, **kwargs):
    #     if not self.slug:
    #         self.slug = slugify(self.title)
    #     super().save(*args, **kwargs)
    #
    #
    # def get_absolute_url(self):
    #     return reverse('news_detail', args=[self.slug])


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    bio = models.TextField()
    genre = models.ManyToManyField(Genre, related_name='authors')
    image = models.ImageField(default='default_profile_pic.png', upload_to='authors', validators=[FileExtensionValidator(
        allowed_extensions=['png', 'jpeg', 'jpg', 'heic', 'webp'])])

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class BookAuthor(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='book')
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='book_author')

    def __str__(self):
        return f'{self.book.title} by {self.author.first_name} {self.author.last_name}'


class BookReview(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='book_review')
    comment = models.TextField()
    stars_given = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.comment} by {self.author.first_name} {self.author.last_name}'

