from django.urls import path
from .views import (WorkerSignupAPIView, MemberSignupAPIView,
                    WorkerSigninAPIView, MemberSigninAPIView, UserProfileAPIView, BorrowBookAPIView,
                    ReturnBookAPIView, MemberBorrowListAPIView, WorkerBorrowListAPIView, ProfileUpdateAPIView,
                    BookListAPIView, BookDetailAPIView, AuthorCreateAPIView, AuthorUpdateAPIView, AuthorDeleteAPIView,
                    CategoryCreateAPIView, CategoryUpdateAPIView, CategoryDeleteAPIView,
                    SubCategoryCreateAPIView, SubCategoryUpdateAPIView, SubCategoryDeleteAPIView,
                    BookCreateAPIView, BookUpdateAPIView, BookDeleteAPIView, AuthorListAPIView, CategoryListAPIView,
                    SubCategoryListAPIView)

urlpatterns = [
    path('member/signup/', MemberSignupAPIView.as_view(), name='member-signup'),
    path('admin/signup/', WorkerSignupAPIView.as_view(), name='admin-signup'),

    path('member/signin/', MemberSigninAPIView.as_view(), name='member-signin'),
    path('admin/signin/', WorkerSigninAPIView.as_view(), name='admin-signin'),

    path('profile/', UserProfileAPIView.as_view(), name='user-profile'),
    path('profile/update/', ProfileUpdateAPIView.as_view(), name='profile-update'),

    path('authors/create/', AuthorCreateAPIView.as_view()),
    path('authors/<int:pk>/update/', AuthorUpdateAPIView.as_view()),
    path('authors/<int:pk>/delete/', AuthorDeleteAPIView.as_view()),
    path('authors/', AuthorListAPIView.as_view()),

    path('category/create/', CategoryCreateAPIView.as_view()),
    path('category/<int:pk>/update/', CategoryUpdateAPIView.as_view()),
    path('category/<int:pk>/delete/', CategoryDeleteAPIView.as_view()),
    path('categories', CategoryListAPIView.as_view()),

    path('subcategory/create/', SubCategoryCreateAPIView.as_view()),
    path('subcategory/<int:pk>/update/', SubCategoryUpdateAPIView.as_view()),
    path('subcategory/<int:pk>/delete/', SubCategoryDeleteAPIView.as_view()),
    path('subcategories', SubCategoryListAPIView.as_view()),

    path('book/create/', BookCreateAPIView.as_view()),
    path('book/<int:pk>/update/', BookUpdateAPIView.as_view()),
    path('book/<int:pk>/delete/', BookDeleteAPIView.as_view()),

    path('books/', BookListAPIView.as_view(), name='book-list'),
    path('books/<int:pk>/', BookDetailAPIView.as_view(), name='book-detail'),

    path('borrow/', BorrowBookAPIView.as_view(), name='borrow-book'),
    path('return/<int:pk>/', ReturnBookAPIView.as_view(), name='return-book'),
    path('my-borrows/', MemberBorrowListAPIView.as_view(), name='member-borrows'),
    path('all-borrows/', WorkerBorrowListAPIView.as_view(), name='worker-borrows'),

]