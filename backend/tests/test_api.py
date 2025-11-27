import pytest
import psycopg2
from fastapi.testclient import TestClient
from app import app

# Replace with your actual test DB credentials
DB_CONFIG = {
    "host": "localhost",
    "database": "your_test_db",
    "user": "your_db_user",
    "password": "your_db_password"
}

def get_db_connection():
    conn = psycopg2.connect(**DB_CONFIG)
    return conn

@pytest.fixture(scope="session", autouse=True)
def setup_db():
    conn = get_db_connection()
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
    yield
    cursor.close()
    conn.close()

client = TestClient(app)

def test_read_root():
  response = client.get("/")
  assert response.status_code == 200
  assert response.json() == {"message": "Welcome to the Blog API"}


def test_get_posts():
  response = client.get("/posts/")
  assert response.status_code == 200
  assert isinstance(response.json(), list)

def test_get_post():
  post_id = 1
  response = client.get(f"/posts/{post_id}")
  assert response.status_code in [200, 404]


def test_post_posts():
  data = {
    "title": "Test Post",
    "content": "This is a test",
    "author": "Bookie"
  }
  response = client.post("/posts/", json=data)
  assert response.status_code == 201 or response.status_code == 200

def test_put_posts():
  post_id = 1
  data = {
    "title": "Updateed Post Test",
    "content": "Updated Test Blog",
    "author": "Bookie"
  }
  response = client.put(f"/posts/{post_id}", json=data)
  assert response.status_code in [200, 404]

def test_delete_posts():
  post_id = 1
  response = client.delete(f"/posts/{post_id}")
  assert response.status_code in [200, 404]
  if response.status_code == 200:
    assert response.json() == {"message": "Post deleted successfully"}

