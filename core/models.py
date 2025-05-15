from django.contrib.auth.models import AbstractUser

from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        MEMBER = 'member', 'Member'
        WORKER = 'worker', 'Worker'

    role = models.CharField(max_length=20, choices=Role.choices)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)

    def is_member(self):
        return self.role == self.Role.MEMBER

    def is_worker(self):
        return self.role == self.Role.WORKER

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    biography = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    date_of_death = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="subcategories")

    def __str__(self):
        return f"{self.name} ({self.category.name})"


class Book(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    isbn = models.CharField(max_length=13, unique=True)
    publication_date = models.DateField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True, blank=True)
    total_copies = models.PositiveIntegerField(default=1)
    available_copies = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.title


class Borrow(models.Model):
    member = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': User.Role.MEMBER})
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrow_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    returned = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.member.username} borrowed {self.book.title}"