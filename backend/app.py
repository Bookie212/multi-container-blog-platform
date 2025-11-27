import psycopg2
import os
from psycopg2.extras import RealDictCursor
from fastapi import FastAPI
from models import BlogPost, BlogPostCreate
from typing import List, Dict

# Database connection
def connect_db():
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST", "db"),
            database=os.getenv("DB_NAME",    "blog_db"),
            user=os.getenv("DB_USER", "bloguser"),
            password=os.getenv("DB_PASSWORD", "blogpassword"),
            port=5432,
            cursor_factory=RealDictCursor
        )
        print("Database connection established")
        return conn
    except psycopg2.Error as e:
        print(f"Error connecting to database: {e}")
    return None

# Load data into database
def load_db(post: BlogPost):
    
    conn = connect_db()
    if not conn:  
        return None

    try:
      cursor = conn.cursor()

      cursor.execute("""
        INSERT INTO blog_posts (title, content, author)
        VALUES (%s, %s, %s)
        RETURNING *
      """, (post.title, post.content, post.author))

      result = cursor.fetchone()
      conn.commit()
      return result
    finally:
      cursor.close()
      conn.close()


# Get all data from database
def get_all_db():

    conn = connect_db()
    if not conn:  
        return []

    try:
      cursor = conn.cursor()

      cursor.execute("SELECT * FROM blog_posts;")
      posts = cursor.fetchall()
      return posts

    finally:
      cursor.close()
      conn.close()



app = FastAPI()

@app.on_event("startup")
def startup():
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("""
          CREATE TABLE IF NOT EXISTS blog_posts (
              id SERIAL PRIMARY KEY,
              title VARCHAR(255) NOT NULL,
              content TEXT NOT NULL,
              author VARCHAR(100) NOT NULL,
              created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
          );
        """)
        conn.commit()
        cursor.close()
        conn.close()

# Api endpoints

@app.get("/")
def read_root():
    return {"message": "Welcome to the Blog API"}

@app.post("/posts/", response_model=BlogPostCreate)
def create_post(post: BlogPostCreate):
    return load_db(post)

@app.get("/posts/", response_model=List[BlogPost])
def read_posts():
    return get_all_db()    

@app.get("/posts/{post_id}", response_model=BlogPost)
def read_post(post_id: int):
    conn = connect_db()
    if not conn:  
        return {"error": "Database connection failed"}
    try:
      cursor = conn.cursor()
      
      cursor.execute("SELECT * FROM blog_posts WHERE id = %s;", (post_id,))
      post = cursor.fetchone()
      return post
    finally:
      cursor.close()
      conn.close()

@app.put("/posts/{post_id}", response_model=BlogPost)
def update_post(post_id: int, post: BlogPost):
    conn = connect_db()
    if not conn:  
        return {"error": "Database connection failed"}
    try:
      cursor = conn.cursor()
          
      cursor.execute("""
        UPDATE blog_posts
        SET title = %s, content = %s, author = %s
        WHERE id = %s
        RETURNING *;
        """, (post.title, post.content, post.author, post_id))

      updates = cursor.fetchone()
      conn.commit()
      return updates
    finally:
      cursor.close()
      conn.close()

@app.delete("/posts/{post_id}")
def delete_post(post_id: int):
    conn = connect_db()
    if not conn:  
        return {"error": "Database connection failed"}
    try:
      cursor = conn.cursor()
            
      cursor.execute("DELETE FROM blog_posts WHERE id = %s;", (post_id,))
      conn.commit()
      return {"message": "Post deleted successfully"}
    finally:
      cursor.close()
      conn.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
