from django.contrib import admin
from .models import (User, Author, Book, Category, SubCategory, Borrow)


admin.site.register(User)
admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Borrow)
