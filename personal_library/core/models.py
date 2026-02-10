from django.db import models

# Create your models here.


class Author(models.Model):
    name = models.CharField(max_length=200)
    biography = models.TextField(blank=True, null=True)
    slug = models.SlugField(
        default="", blank=True, null=True, unique=False
    )  # TODO: Populate slugs and change `unique` to `True`

    def __str__(self):
        return self.name

    def to_dict(self):
        return {"id": self.id, "name": self.name, "biography": self.biography}


class Publisher(models.Model):
    name = models.CharField(max_length=200)
    country = models.CharField(max_length=100, blank=True, null=True)

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
