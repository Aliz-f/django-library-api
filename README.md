# 📚 Django Library Management API

A RESTful API for managing a digital library system, built with Django 5.2 and Django REST Framework. The application supports two types of users — **members** and **workers (admins)** — and provides fully documented CRUD functionality for books, authors, categories, and subcategories.

> 🔐 Authentication is handled via **JWT**, and all endpoints are documented using **Swagger UI** (`drf-yasg`).

---

## 🚀 Features

- JWT-based authentication
- Member and worker roles
- Profile management and image upload
- Book borrowing and return system
- Admin-only CRUD for:
  - Authors
  - Categories and Subcategories
  - Books
- Filtered book listing by category, author, or availability
- Swagger documentation for all endpoints

---

## 🛠 Tech Stack

- Python 3.11+
- Django 5.2
- Django REST Framework
- SimpleJWT
- drf-yasg (for Swagger UI)

---

## 📦 Installation

```bash
# Clone the repo
$ git clone https://github.com/yourusername/django-library-api.git
$ cd django-library-api

# Create and activate a virtual environment
$ python -m venv env
$ source env/bin/activate  # On Windows: env\Scripts\activate

# Install dependencies
$ pip install -r requirements.txt

# Run migrations
$ python manage.py migrate

# Create superuser (optional)
$ python manage.py createsuperuser

# Run the server
$ python manage.py runserver
```

---

## 📚 API Endpoints

### 🔐 Authentication
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/member/signup/` | POST | Register as a member |
| `/api/admin/signup/` | POST | Register as a worker (admin) |
| `/api/member/signin/` | POST | Login as a member (returns JWT) |
| `/api/admin/signin/` | POST | Login as a worker (returns JWT) |

### 👤 Profile
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/profile/` | GET | View current user's profile |
| `/api/profile/update/` | PUT | Update profile details & picture |

### 🖋️ Author Management *(admin only)*
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/authors/create/` | POST | Create a new author |
| `/api/authors/<id>/update/` | PUT | Update an author |
| `/api/authors/<id>/delete/` | DELETE | Delete an author |

### 🗂️ Category & Subcategory *(admin only)*
| Category |
|----------|
| `/api/category/create/` – POST |
| `/api/category/<id>/update/` – PUT |
| `/api/category/<id>/delete/` – DELETE |

| SubCategory |
|-------------|
| `/api/subcategory/create/` – POST |
| `/api/subcategory/<id>/update/` – PUT |
| `/api/subcategory/<id>/delete/` – DELETE |

### 📘 Book Management *(admin only)*
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/book/create/` | POST | Create a new book |
| `/api/book/<id>/update/` | PUT | Update a book |
| `/api/book/<id>/delete/` | DELETE | Delete a book |

### 📚 Book Browsing (members and workers)
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/books/` | GET | List all books (filterable by category, author, availability) |
| `/api/books/<id>/` | GET | View a book’s detail |

### 🔄 Borrowing System (members only)
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/borrow/` | POST | Borrow a book |
| `/api/return/<id>/` | POST | Return a borrowed book |
| `/api/my-borrows/` | GET | View member’s borrowing history |

### 🧑‍💼 Borrow Admin (workers only)
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/all-borrows/` | GET | View all borrowing records with filters |

---

## 🔎 API Documentation

Once the server is running, go to:

```
http://127.0.0.1:8000/swagger/
```

There you'll find a full Swagger UI interface with:
- Example requests
- JWT auth support
- Model schemas

---

## 📂 Media and Static Files

Ensure these are set in `settings.py`:
```python
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
```

These are exposed in `urls.py`:
```python
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
```

---

## 🤝 Contributing
Pull requests are welcome! Open an issue to discuss ideas.

---

## 📄 License
This project is licensed under the MIT License.
