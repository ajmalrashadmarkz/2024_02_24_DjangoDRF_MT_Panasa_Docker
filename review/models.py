
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()


class Author(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    published_books = models.PositiveIntegerField(default = 0)
    total_rating = models.DecimalField(max_digits=5, decimal_places=2,  default=0.00)
    rating_sum = models.DecimalField(max_digits=5, decimal_places=2,  default=0.00)
    author_review_count = models.PositiveIntegerField(default = 0)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    total_rating = models.DecimalField(max_digits=10, decimal_places=2,  default=0.00)
    rating_sum = models.DecimalField(max_digits=10, decimal_places=2,  default=0.00)
    book_review_count = models.PositiveIntegerField(default = 0)

    def __str__(self):
        return self.title


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True, blank=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True, blank=True)
    review_content = models.TextField()
    content = models.TextField()
    rating = models.DecimalField(max_digits=5, decimal_places=2,  default=0.00)
    def __str__(self):
        return f"{self.user.username} - {self.rating}"