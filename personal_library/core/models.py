from datetime import datetime, timedelta
from enum import StrEnum

from django.contrib.auth.models import User
from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=200)
    biography = models.TextField(blank=True, null=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    def to_dict(self):
        return {"id": self.id, "name": self.name, "biography": self.biography}


class Publisher(models.Model):
    name = models.CharField(max_length=200)
    country = models.CharField(max_length=100, blank=True, null=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    def to_dict(self):
        return {"id": self.id, "name": self.name, "country": self.country}


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    publisher = models.ForeignKey(
        Publisher, on_delete=models.SET_NULL, blank=True, null=True
    )
    synopsis = models.TextField()
    publication_date = models.DateField()
    cover_image = models.ImageField(upload_to="book_covers/", blank=True, null=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author.to_dict() if self.author else None,
            "publisher": self.publisher.to_dict() if self.publisher else None,
            "synopsis": self.synopsis,
            "publication_date": self.publication_date,
            "cover_image": self.cover_image.url if self.cover_image else None,
        }


class RentalStatus(StrEnum):
    RENTED = "RENTED"
    ON_TIME = "ON_TIME"
    LATE = "LATE"


class Rental(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    book = models.ForeignKey(Book, on_delete=models.RESTRICT, null=False, blank=False)
    rented_at = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    expected_return_date = models.DateTimeField(
        blank=True, null=True, default=datetime.now() + timedelta(days=14)
    )
    returned_at = models.DateTimeField(blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=[(status.value, status.value) for status in RentalStatus],
    )

    def to_dict(self):
        return {
            "id": self.id,
            "book": self.book.to_dict() if self.book else None,
            "rented_at": self.rented_at,
            "returned_at": self.returned_at,
            "status": self.status,
            "user": self.user.username if self.user else None,
        }
