from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from datetime import timedelta

from django.contrib.auth import authenticate
from django.utils import timezone

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser

from .serializers import (SignupSerializer, SigninSerializer, BorrowSerializer,
                          ProfileUpdateSerializer, BookSerializer, AuthorSerializer,
                          AdminBookSerializer, CategorySerializer, SubCategorySerializer)
from .models import (User, Borrow, Book, Author, Category, SubCategory)

# class SignupAPIView(APIView):
#     def post(self, request):
#         serializer = SignupSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
#             return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MemberSignupAPIView(APIView):

    @swagger_auto_schema(request_body=SignupSerializer)
    def post(self, request):
        request.data['role'] = 'member'
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Member created successfully"}, status=201)
        return Response(serializer.errors, status=400)


class WorkerSignupAPIView(APIView):

    @swagger_auto_schema(request_body=SignupSerializer)
    def post(self, request):
        request.data['role'] = 'worker'
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Worker created successfully"}, status=201)
        return Response(serializer.errors, status=400)


# class SigninAPIView(APIView):
#     def post(self, request):
#         serializer = SigninSerializer(data=request.data)
#         if serializer.is_valid():
#             username = serializer.validated_data['username']
#             password = serializer.validated_data['password']
#             user = authenticate(username=username, password=password)
#
#             if user:
#                 refresh = RefreshToken.for_user(user)
#                 return Response({
#                     'access': str(refresh.access_token),
#                     'refresh': str(refresh),
#                     'user': {
#                         'username': user.username,
#                         'role': user.role,
#                         'email': user.email
#                     }
#                 })
#             return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MemberSigninAPIView(APIView):

    @swagger_auto_schema(request_body=SigninSerializer)
    def post(self, request):
        serializer = SigninSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password']
            )
            if user and user.role == User.Role.MEMBER:
                refresh = RefreshToken.for_user(user)
                return Response({
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                    "user": {
                        "username": user.username,
                        "email": user.email,
                        "role": user.role
                    }
                }, status=200)
            return Response({"error": "Invalid credentials or not a member"}, status=401)
        return Response(serializer.errors, status=400)


class WorkerSigninAPIView(APIView):

    @swagger_auto_schema(request_body=SigninSerializer)
    def post(self, request):
        serializer = SigninSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password']
            )
            if user and user.role == User.Role.WORKER:
                refresh = RefreshToken.for_user(user)
                return Response({
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                    "user": {
                        "username": user.username,
                        "email": user.email,
                        "role": user.role
                    }
                }, status=200)
            return Response({"error": "Invalid credentials or not a worker"}, status=401)
        return Response(serializer.errors, status=400)


class UserProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "role": user.role,
        }, status=status.HTTP_200_OK)


class ProfileUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(
        request_body=ProfileUpdateSerializer,
        consumes=["multipart/form-data"],  # 🔥 Important
        operation_summary="Update profile with optional file upload"
    )
    def put(self, request):
        serializer = ProfileUpdateSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Profile updated successfully.'}, status=200)
        return Response(serializer.errors, status=400)


# ------------------------
# CRUD Views for Author
# ------------------------
class AuthorCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=AuthorSerializer)
    def post(self, request):
        if request.user.role != request.user.Role.WORKER:
            return Response({'error': 'Only workers can create authors.'}, status=403)
        serializer = AuthorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class AuthorUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=AuthorSerializer)
    def put(self, request, pk):
        if request.user.role != request.user.Role.WORKER:
            return Response({'error': 'Only workers can update authors.'}, status=403)
        try:
            author = Author.objects.get(pk=pk)
        except Author.DoesNotExist:
            return Response({'error': 'Author not found'}, status=404)

        serializer = AuthorSerializer(author, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


class AuthorDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        if request.user.role != request.user.Role.WORKER:
            return Response({'error': 'Only workers can delete authors.'}, status=403)
        try:
            author = Author.objects.get(pk=pk)
            author.delete()
            return Response({'message': 'Author deleted'}, status=204)
        except Author.DoesNotExist:
            return Response({'error': 'Author not found'}, status=404)

# ------------------------
# CRUD Views for Category
# ------------------------
class CategoryCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=CategorySerializer)
    def post(self, request):
        if request.user.role != request.user.Role.WORKER:
            return Response({'error': 'Only workers can create categories.'}, status=403)
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class CategoryUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=CategorySerializer)
    def put(self, request, pk):
        if request.user.role != request.user.Role.WORKER:
            return Response({'error': 'Only workers can update categories.'}, status=403)
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response({'error': 'Category not found'}, status=404)

        serializer = CategorySerializer(category, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


class CategoryDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        if request.user.role != request.user.Role.WORKER:
            return Response({'error': 'Only workers can delete categories.'}, status=403)
        try:
            category = Category.objects.get(pk=pk)
            category.delete()
            return Response({'message': 'Category deleted'}, status=204)
        except Category.DoesNotExist:
            return Response({'error': 'Category not found'}, status=404)

# ------------------------
# CRUD Views for SubCategory
# ------------------------
class SubCategoryCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=SubCategorySerializer)
    def post(self, request):
        if request.user.role != request.user.Role.WORKER:
            return Response({'error': 'Only workers can create subcategories.'}, status=403)
        serializer = SubCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class SubCategoryUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=SubCategorySerializer)
    def put(self, request, pk):
        if request.user.role != request.user.Role.WORKER:
            return Response({'error': 'Only workers can update subcategories.'}, status=403)
        try:
            subcategory = SubCategory.objects.get(pk=pk)
        except SubCategory.DoesNotExist:
            return Response({'error': 'SubCategory not found'}, status=404)

        serializer = SubCategorySerializer(subcategory, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


class SubCategoryDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        if request.user.role != request.user.Role.WORKER:
            return Response({'error': 'Only workers can delete subcategories.'}, status=403)
        try:
            subcategory = SubCategory.objects.get(pk=pk)
            subcategory.delete()
            return Response({'message': 'SubCategory deleted'}, status=204)
        except SubCategory.DoesNotExist:
            return Response({'error': 'SubCategory not found'}, status=404)

# ------------------------
# CRUD Views for Book
# ------------------------
class BookCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(request_body=AdminBookSerializer)
    def post(self, request):
        if request.user.role != request.user.Role.WORKER:
            return Response({'error': 'Only workers can create books.'}, status=403)
        serializer = AdminBookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class BookUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=AdminBookSerializer)
    def put(self, request, pk):
        if request.user.role != request.user.Role.WORKER:
            return Response({'error': 'Only workers can update books.'}, status=403)
        try:
            book = Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            return Response({'error': 'Book not found'}, status=404)

        serializer = AdminBookSerializer(book, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


class BookDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        if request.user.role != request.user.Role.WORKER:
            return Response({'error': 'Only workers can delete books.'}, status=403)
        try:
            book = Book.objects.get(pk=pk)
            book.delete()
            return Response({'message': 'Book deleted'}, status=204)
        except Book.DoesNotExist:
            return Response({'error': 'Book not found'}, status=404)


class BookListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        books = Book.objects.all()

        # Optional filters
        category_name = request.query_params.get('category')
        author_name = request.query_params.get('author')
        available = request.query_params.get('available') == 'true'

        if category_name:
            books = books.filter(category__name__icontains=category_name)

        if author_name:
            books = books.filter(author__last_name__icontains=author_name)

        if available:
            books = books.filter(available_copies__gt=0)

        serialized = BookSerializer(books, many=True)
        return Response(serialized.data, status=200)


class BookDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            book = Book.objects.get(id=pk)
        except Book.DoesNotExist:
            return Response({'error': 'Book not found.'}, status=404)

        serialized = BookSerializer(book)
        return Response(serialized.data, status=200)


class BorrowBookAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['book'],
            properties={
                'book': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of the book to borrow')
            }
        ),
        operation_summary="Borrow a book",
        operation_description="Allows a member to borrow a book by providing the book ID.",
        responses={
            201: BorrowSerializer,
            400: "Invalid request or no copies available",
            403: "Only members can borrow books",
            404: "Book not found"
        }
    )
    def post(self, request):
        user = request.user
        if not user.role == user.Role.MEMBER:
            return Response({'error': 'Only members can borrow books.'}, status=403)

        book_id = request.data.get('book')
        try:
            book = Book.objects.get(id=book_id)
            if book.available_copies < 1:
                return Response({'error': 'No copies available.'}, status=400)
        except Book.DoesNotExist:
            return Response({'error': 'Book not found.'}, status=404)

        due_date = timezone.now().date() + timedelta(days=14)  # 2 weeks
        borrow = Borrow.objects.create(
            member=user,
            book=book,
            due_date=due_date
        )
        book.available_copies -= 1
        book.save()

        return Response(BorrowSerializer(borrow).data, status=201)


# class BorrowBookAPIView(APIView):
#     permission_classes = [IsAuthenticated]
#
#     def post(self, request):
#         user = request.user
#         if user.role != user.Role.MEMBER:
#             return Response({'error': 'Only members can borrow books.'}, status=403)
#
#         book_id = request.data.get('book')
#         try:
#             book = Book.objects.get(id=book_id)
#         except Book.DoesNotExist:
#             return Response({'error': 'Book not found.'}, status=404)
#
#         if book.available_copies < 1:
#             return Response({'error': 'No copies available.'}, status=400)
#
#         already_borrowed = Borrow.objects.filter(member=user, book=book, returned=False).exists()
#         if already_borrowed:
#             return Response({'error': 'You already borrowed this book.'}, status=400)
#
#         due_date = timezone.now().date() + timedelta(days=14)
#         borrow = Borrow.objects.create(member=user, book=book, due_date=due_date)
#         book.available_copies -= 1
#         book.save()
#
#         return Response(BorrowSerializer(borrow).data, status=201)


class ReturnBookAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Return a borrowed book",
        operation_description="Marks the borrow record as returned and updates book availability.",
        responses={200: openapi.Response("Success"), 404: "Not Found"},
        request_body=None
    )
    def post(self, request, pk):  # pk = Borrow ID
        try:
            borrow = Borrow.objects.get(id=pk, member=request.user, returned=False)
        except Borrow.DoesNotExist:
            return Response({'error': 'Borrow record not found or already returned.'}, status=404)

        borrow.return_date = timezone.now().date()
        borrow.returned = True
        borrow.save()

        book = borrow.book
        book.available_copies += 1
        book.save()

        return Response({'message': 'Book returned successfully.'}, status=200)


class MemberBorrowListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != request.user.Role.MEMBER:
            return Response({'error': 'Only members can view this.'}, status=403)

        borrows = Borrow.objects.filter(member=request.user)

        # Optional filters
        returned = request.query_params.get('returned')
        if returned == 'true':
            borrows = borrows.filter(returned=True)
        elif returned == 'false':
            borrows = borrows.filter(returned=False)

        overdue = request.query_params.get('overdue')
        if overdue == 'true':
            borrows = borrows.filter(returned=False, due_date__lt=timezone.now().date())

        serializer = BorrowSerializer(borrows, many=True)
        return Response(serializer.data, status=200)


class WorkerBorrowListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if user.role != user.Role.WORKER:
            return Response({'error': 'Only workers can view borrow records.'}, status=403)

        borrows = Borrow.objects.all()

        # Filter by returned status
        returned = request.query_params.get('returned')
        if returned == 'true':
            borrows = borrows.filter(returned=True)
        elif returned == 'false':
            borrows = borrows.filter(returned=False)

        # Filter by active status (alias for returned=false)
        only_active = request.query_params.get('active')
        if only_active == 'true':
            borrows = borrows.filter(returned=False)

        # Filter by member username
        member_username = request.query_params.get('member')
        if member_username:
            borrows = borrows.filter(member__username=member_username)

        # Filter by overdue
        overdue = request.query_params.get('overdue')
        if overdue == 'true':
            borrows = borrows.filter(returned=False, due_date__lt=timezone.now().date())

        serializer = BorrowSerializer(borrows, many=True)
        return Response(serializer.data, status=200)

