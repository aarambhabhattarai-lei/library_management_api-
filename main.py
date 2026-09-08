from pyexpat import model
from fastapi import FastAPI, HTTPException, Response ,status     
from fastapi.params import Body, Depends
from pydantic import BaseModel
from typing import Optional
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from fastapi import FastAPI, HTTPException, Response, status, Query
from sqlalchemy import func
import models
from database import engine, SessionLocal ,get_db
from sqlalchemy.orm import Session
from datetime import datetime 
from dotenv import load_dotenv

import time
import os

load_dotenv()
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

class Books(BaseModel):
    title: str
    author : str
    genre : str
    published_year: Optional[int] = None
    available : bool = True



class Members(BaseModel):
   
    name: str
    email: str
    phone : int 



class BorrowedBooks(BaseModel):

    book_id :int
    member_id : int
    borrowed_date: Optional[int] = None
    returned_date: Optional[int] = None
while True:
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            cursor_factory=RealDictCursor
        )

        cursor = conn.cursor()

        print("Database connection was successful")
        break

    except Exception as error:
        print("Connecting to database failed:", error)
        time.sleep(2)



@app.get("/Books")
def get_books( db: Session = Depends(get_db)):
   books = db.query(models.Books).all()
   return {"message": "This is a GET request", "data": books}

@app.post("/AddBooks")
def add_books(book: Books, db: Session = Depends(get_db)):
    new_book=models.Books(**book.dict())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return {"message": "This is a POST request", "data": new_book}

@app.get("/INFO/{id}")
def get_book(id:int , db: Session = Depends(get_db)):
    book=db.query(models.Books).filter(models.Books.id==id).first()
    if not book:
        raise HTTPException(status_code=404, detail=f"Book with id {id} not found")
    return {"message": "This is a GET request", "data": book}

@app.put("/update/{id}")
def update_book(id:int , db: Session = Depends(get_db)):
    book=db.query(models.Books).filter(models.Books.id==id)
    books=book.first()
    if not books:
        raise HTTPException(status_code=404, detail=f"Book with id {id} not found") 
    update_book.update(Books.dict(),synchronize_session=False
    )
    db.commit()
    return {"message": "This is a PUT request", "data": book}

@app.delete("/delete/{id}")
def delete_book(id:int , db: Session = Depends(get_db)):
    book=db.query(models.Books).filter(models.Books.id==id)
    if not book:
        raise HTTPException(status_code=404, detail=f"Book with id {id} not found")
    db.delete(book)
    db.commit()
    return {"message": "This is a DELETE request", "data": book}

@app.get("/books/{title}")
def get_book(title: str, db: Session = Depends(get_db)):
    book = db.query(models.Books).filter(models.Books.title == title).first()

    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )

    return book

@app.post("/members")
def add_member(member: Members, db: Session = Depends(get_db)):

    new_member = models.Members(**member.dict())

    db.add(new_member)

    db.commit()

    db.refresh(new_member)

    return {"message": "This is a POST request", "data": new_member}


@app.get("/members")
def get_members(db: Session = Depends(get_db)):

    members = db.query(models.Members).all()

    return {"message": "This is a GET request", "data": members}


@app.get("/members/{id}")
def get_member(id: int, db: Session = Depends(get_db)):

    member = db.query(models.Members).filter(models.Members.id == id).first()

    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Member not found"
        )

    return {"message": "Member found", "data": member}


@app.put("/members/{id}")
def update_member(id: int, member: Members, db: Session = Depends(get_db)):

    update_member = db.query(models.Members).filter(
        models.Members.id == id
    ).first()

    if not update_member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Member not found"
        )

    update_member.update(member.dict(), synchronize_session=False)

    db.commit()

    db.refresh(update_member)

    return {"message": "Member updated successfully", "data": update_member}


@app.delete("/members/{id}")
def delete_member(id: int, db: Session = Depends(get_db)):

    member = db.query(models.Members).filter(
        models.Members.id == id
    ).first()

    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Member not found"
        )

    db.delete(member)

    db.commit()

    return {"message": "Member deleted successfully"}

@app.post("/borrow")
def borrow_book(borrowed_book: BorrowedBooks, db: Session = Depends(get_db)):
    new_borrowed_book = models.BorrowedBooks(**borrowed_book.dict())
    if new_borrowed_book.book_id == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )

    if new_borrowed_book.member_id == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Member not found"
        )

    if new_borrowed_book.avaiability == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book is not available"
        )

    db.add(new_borrowed_book)
    db.commit()
    db.refresh(new_borrowed_book)
    return {"message": "Book borrowed successfully", "data": new_borrowed_book}

@app.put("/borrow/{id}/return")
def return_book(id: int, db: Session = Depends(get_db)):
    borrow_book = db.query(models.BorrowedBooks).filter(models.BorrowedBooks.id == id).first()

    if not borrow_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Borrowed book not found"
        )

    borrow_book.returned_date = datetime.datetime.now()

    book = db.query(models.Books).filter(models.Books.id == borrow_book.book_id).first()
    book.available = True


    return {"message": "Book returned successfully"}

@app.get("/BorrowedBooks")
def get_books( db: Session = Depends(get_db)):
   books = db.query(models.BorrowedBooks).all()
   return {"message": "This is a GET request", "data": books}

@app.get("/books")
def get_books(
    search: str |None=None ,
    genre: str |None=None ,
    available: bool |None=None ,    
    page:int= Query(1, ge=1),
    limit:int= Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    Query = db.query(models.Books)

    if search:
        Query = Query.filter(models.Books.title.ilike(f"%{search}%"))

    if genre:
        Query = Query.filter(models.Books.genre == genre)

    if available is not None:
        Query = Query.filter(models.Books.available == available)

    Queryy = Query.order_by(models.Books.title)

    offset = (page - 1) * limit
    Queryy = Queryy.offset(offset).limit(limit).all()

    return {"message": "This is a GET request", "data": Queryy}