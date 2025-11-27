# Multi-Container Blog Platform

A multi-container blog platform built with FastAPI, PostgreSQL, and Nginx. Demonstrates Docker Compose orchestration with container networking, persistent storage, and reverse proxy configuration.

## Features

- RESTful API endpoints for blog posts (CRUD operations)
- PostgreSQL database for persistent data storage
- Nginx reverse proxy for routing and load balancing
- Pydantic models for data validation
- FastAPI automatic interactive documentation
- Docker Compose for multi-container orchestration
- Volume persistence - data survives container restarts

## Architecture

The application consists of three services:

- **db**: PostgreSQL 15 database container
- **backend**: FastAPI application container
- **nginx**: Nginx reverse proxy container

All services communicate through Docker's internal networking.

## Project Structure
```
blog-platform/
├── docker-compose.yml          
├── backend/
│   ├── app.py                  
│   ├── models.py               
│   ├── requirements.txt        
│   └── Dockerfile              
├── nginx/
│   ├── nginx.conf             
│   └── Dockerfile             
└── README.md                  
```

## Prerequisites

- Docker
- Docker Compose

## Getting Started

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd blog-platform
```

### 2. Build and start all services
```bash
docker-compose up --build
```

The application will be accessible at `http://localhost`

### 3. Stop the services
```bash
docker-compose down
```

To stop and remove volumes (delete all data):
```bash
docker-compose down -v
```

## API Endpoints

### POST /posts/
Create a new blog post.

**Request body:**
```json
{
  "title": "Post Title",
  "content": "Post content here",
  "author": "Author Name"
}
```

### GET /posts/
Returns a list of all blog posts.

**Response:** Array of blog post objects

### GET /posts/{post_id}
Returns a specific blog post by ID.

**Parameters:** `post_id` (integer)

### PUT /posts/{post_id}
Updates a specific blog post.

**Parameters:** `post_id` (integer)

**Request body:**
```json
{
  "title": "Updated Title",
  "content": "Updated content",
  "author": "Author Name"
}
```

### DELETE /posts/{post_id}
Deletes a specific blog post.

**Parameters:** `post_id` (integer)

### GET /docs
FastAPI automatically generates interactive API documentation (Swagger UI).

**Access at:** http://localhost/docs

## Testing the API

### Create a post
```bash
curl -X POST http://localhost/posts/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My First Post",
    "content": "Hello Docker Compose!",
    "author": "DevOps Student"
  }'
```

### Get all posts
```bash
curl http://localhost/posts/
```

### Get a specific post
```bash
curl http://localhost/posts/1
```

### Update a post
```bash
curl -X PUT http://localhost/posts/1 \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated Title",
    "content": "Updated content",
    "author": "DevOps Student"
  }'
```

### Delete a post
```bash
curl -X DELETE http://localhost/posts/1
```

## Data Persistence

Blog post data is persisted using Docker volumes. The PostgreSQL data is stored in the `db_data` volume, which means:

- Data survives container restarts
- Data persists even when you run `docker-compose down`
- Data is only deleted when you explicitly remove the volume with `docker-compose down -v`

**Test persistence:**
```bash
# Create a post
curl -X POST http://localhost/posts/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Test", "content": "Testing persistence", "author": "Tester"}'

# Stop containers
docker-compose down

# Restart containers
docker-compose up -d

# Verify post still exists
curl http://localhost/posts/
```

## Technologies Used

- **FastAPI** - Modern, high-performance web framework for building APIs
- **Pydantic** - Data validation using Python type annotations
- **PostgreSQL** - Powerful open-source relational database
- **psycopg2** - PostgreSQL adapter for Python
- **Uvicorn** - Lightning-fast ASGI server
- **Nginx** - High-performance reverse proxy and web server
- **Docker** - Containerization platform
- **Docker Compose** - Multi-container application orchestration

## Configuration

### Environment Variables

Database configuration is set in `docker-compose.yml`:
```yaml
POSTGRES_USER: bloguser
POSTGRES_PASSWORD: blogpassword
POSTGRES_DB: blogdb
```

### Ports

- **80**: Nginx (main application entry point)
- **8000**: Backend API (optional direct access)
- **5432**: PostgreSQL (for database inspection)

## Troubleshooting

### View logs for all services
```bash
docker-compose logs
```

### View logs for specific service
```bash
docker-compose logs backend
docker-compose logs db
docker-compose logs nginx
```

### Follow logs in real-time
```bash
docker-compose logs -f backend
```

### Check running containers
```bash
docker-compose ps
```

### Restart a specific service
```bash
docker-compose restart backend
```

## LICENSE

MIT LICENSE