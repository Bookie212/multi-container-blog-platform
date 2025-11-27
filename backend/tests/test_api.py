from fastapi.testclient import TestClient
from app import app

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

