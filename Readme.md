# 📚 Library Management API

A RESTful Library Management API built with **FastAPI**, **PostgreSQL**, and **SQLAlchemy ORM**.

This project provides APIs for managing books, members, and book borrowing/returning.

## 🚀 Features

### 📖 Books

* Create a book
* Get all books
* Get a book by ID
* Update a book
* Delete a book
* Search books by title
* Filter books by genre
* Filter books by availability
* Sort books
* Pagination

### 👤 Members

* Create a member
* Get all members
* Get a member by ID
* Update a member
* Delete a member

### 🔄 Borrowing

* Borrow a book
* Return a book
* Track borrowing history
* Check book availability

### 🛡️ Validation & Error Handling

* Request validation using Pydantic
* Proper HTTP status codes
* 404 errors for missing resources
* Validation for pagination parameters

## 🛠️ Technologies Used

* **Python**
* **FastAPI**
* **SQLAlchemy**
* **PostgreSQL**
* **Pydantic**
* **Uvicorn**
* **psycopg2**

## 📁 Project Structure

```text
Library-Management-API/
│
├── main.py
├── models.py
├── schemas.py
├── database.py
├── requirements.txt
├── .gitignore
└── README.md
```

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd Library-Management-API
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it:

**Windows:**

```bash
venv\Scripts\activate
```

**Linux/macOS:**

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 🗄️ Database Setup

Create a PostgreSQL database and configure the database connection in `database.py`.

Example:

```python
SQLALCHEMY_DATABASE_URL = "postgresql://username:password@localhost/database_name"
```

Make sure PostgreSQL is running before starting the API.

## ▶️ Running the API

Start the development server with:

```bash
uvicorn main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

## 📑 API Documentation

FastAPI automatically provides interactive API documentation.

### Swagger UI

```text
http://127.0.0.1:8000/docs
```

### ReDoc

```text
http://127.0.0.1:8000/redoc
```

You can use Swagger UI or **Postman** to test the API.

## 🔍 Example Book Queries

Get all books:

```text
GET /books
```

Search:

```text
GET /books?search=harry
```

Filter by genre:

```text
GET /books?genre=Fantasy
```

Filter available books:

```text
GET /books?available=true
```

Pagination:

```text
GET /books?page=2&limit=10
```

Combine multiple filters:

```text
GET /books?search=harry&genre=Fantasy&available=true&page=1&limit=10
```

## 📚 Database Tables

The project uses three main tables:

### Books

Stores information about books and their availability.

### Members

Stores library member information.

### Borrowed Books

Stores borrowing records, including:

* Book ID
* Member ID
* Borrowed date
* Returned date

A `NULL` `returned_at` value indicates that the book has not yet been returned.

## 🔄 Borrowing Flow

```text
Member
   │
   ▼
Borrow Book
   │
   ├── Create borrowing record
   └── Set book.available = False
   │
   ▼
Book is borrowed
   │
   ▼
Return Book
   │
   ├── Set returned_at
   └── Set book.available = True
```

## 🧪 Testing

The API can be tested using:

* Swagger UI
* Postman

Make sure the PostgreSQL database is running before testing database-related endpoints.

## ☁️ Deployment

The API can be deployed using platforms such as **Render**.

For deployment, configure the PostgreSQL connection string using environment variables rather than committing database credentials to GitHub.

## 🎯 Project Purpose

This project was built to practice:

* FastAPI
* REST APIs
* PostgreSQL
* SQLAlchemy ORM
* CRUD operations
* Pydantic schemas
* Query parameters
* Filtering and searching
* Sorting
* Pagination
* Database relationships
* API validation
* Error handling
* Backend deployment
