from django.utils import timezone
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers

from .models import (User, Borrow, Book, SubCategory, Author, Category)


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'role']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class SigninSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class ProfileUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    profile_picture = serializers.ImageField(required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'profile_picture']

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()
        return instance


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'first_name', 'last_name',
                  'biography', 'date_of_birth', 'date_of_death']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['id', 'name', 'category']


class AdminBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'description', 'isbn', 'publication_date',
                  'author', 'category', 'subcategory', 'total_copies', 'available_copies']


class BookSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    category = serializers.StringRelatedField()
    subcategory = serializers.StringRelatedField()

    class Meta:
        model = Book
        fields = ['id', 'title', 'description', 'isbn', 'publication_date',
                  'author', 'category', 'subcategory', 'total_copies', 'available_copies']


class BorrowSerializer(serializers.ModelSerializer):
    book = serializers.StringRelatedField()
    is_overdue = serializers.SerializerMethodField()

    class Meta:
        model = Borrow
        fields = ['id', 'book', 'borrow_date', 'due_date', 'return_date',
                  'returned', 'is_overdue']

    def get_is_overdue(self, obj):
        return not obj.returned and obj.due_date < timezone.now().date()

