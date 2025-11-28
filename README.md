# Multi-Container Blog Platform

[![CI/CD Pipeline](https://github.com/bookie212/multi-container-blog-platform/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/bookie212/multi-container-blog-platform/actions/workflows/ci-cd.yml)

A production-ready multi-container blog platform built with FastAPI, PostgreSQL, and Nginx. Features automated CI/CD pipeline with GitHub Actions, comprehensive testing, and Docker orchestration.

## Features

- **RESTful API** - Full CRUD operations for blog posts
- **Database** - PostgreSQL with persistent storage
- **Reverse Proxy** - Nginx for routing and load balancing
- **Data Validation** - Pydantic models with automatic validation
- **API Documentation** - Auto-generated interactive docs with Swagger UI
- **Containerization** - Multi-container orchestration with Docker Compose
- **CI/CD Pipeline** - Automated testing and deployment with GitHub Actions
- **Automated Testing** - pytest with FastAPI TestClient
- **Container Registry** - Automated builds pushed to Docker Hub

## Architecture

The application consists of three services:
```
┌─────────────┐
│   Client    │
└──────┬──────┘
       │ HTTP
       ▼
┌─────────────┐
│    Nginx    │  (Reverse Proxy)
│   Port 80   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Backend   │  (FastAPI)
│  Port 8000  │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ PostgreSQL  │  (Database)
│  Port 5432  │
└─────────────┘
```

All services communicate through Docker's internal networking with persistent data storage.

## Project Structure
```
multi-container-blog-platform/
├── .github/
│   └── workflows/
│       └── ci-cd.yml           
├── backend/
│   ├── tests/
│   │   ├── __init__.py
│   │   └── test_api.py         
│   ├── app.py                  
│   ├── models.py               
│   ├── requirements.txt        
│   └── Dockerfile              
├── nginx/
│   ├── nginx.conf              
│   └── Dockerfile             
├── docker-compose.yml          
├── .gitignore
└── README.md
```

## Prerequisites

- Docker
- Docker Compose
- Git

## Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/bookie212/multi-container-blog-platform.git
cd multi-container-blog-platform
```

### 2. Build and start all services
```bash
docker-compose up --build
```

The application will be accessible at `http://localhost`

### 3. Access the API documentation

Visit `http://localhost/docs` for interactive API documentation

### 4. Stop the services
```bash
docker-compose down
```

To stop and remove volumes (delete all data):
```bash
docker-compose down -v
```

## Running with Pre-built Images

You can also run the application using pre-built images from Docker Hub:
```bash
# Pull the latest images
docker pull bookie212/my-backend:latest
docker pull bookie212/my-nginx:latest

# Run with docker-compose
docker-compose up
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

**Response:** `201 Created`
```json
{
  "id": 1,
  "title": "Post Title",
  "content": "Post content here",
  "author": "Author Name",
  "created_at": "2024-11-26T12:00:00"
}
```

### GET /posts/
Returns a list of all blog posts.

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "title": "Post Title",
    "content": "Post content here",
    "author": "Author Name",
    "created_at": "2024-11-26T12:00:00"
  }
]
```

### GET /posts/{post_id}
Returns a specific blog post by ID.

**Parameters:** `post_id` (integer)

**Response:** `200 OK` or `404 Not Found`

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

**Response:** `200 OK` or `404 Not Found`

### DELETE /posts/{post_id}
Deletes a specific blog post.

**Parameters:** `post_id` (integer)

**Response:** `200 OK` with `{"message": "Post deleted successfully"}`

### GET /docs
FastAPI automatically generates interactive API documentation (Swagger UI).

**Access at:** http://localhost/docs

## Testing the API

### Using curl

#### Create a post
```bash
curl -X POST http://localhost/posts/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My First Post",
    "content": "Hello Docker Compose!",
    "author": "DevOps Student"
  }'
```

#### Get all posts
```bash
curl http://localhost/posts/
```

#### Get a specific post
```bash
curl http://localhost/posts/1
```

#### Update a post
```bash
curl -X PUT http://localhost/posts/1 \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated Title",
    "content": "Updated content",
    "author": "DevOps Student"
  }'
```

#### Delete a post
```bash
curl -X DELETE http://localhost/posts/1
```

## Running Tests

### Run tests locally
```bash
# Make sure containers are running
docker-compose up -d

# Install dependencies
cd backend
pip install -r requirements.txt

# Run tests
pytest tests/
```

### Tests run automatically

Tests are automatically executed on every push to the repository via GitHub Actions. Check the Actions tab for results.

## CI/CD Pipeline

This project uses GitHub Actions for continuous integration and deployment:

### Workflow Triggers
- Push to `master` branch
- Pull requests to `master` branch

### Pipeline Stages

1. **Test**
   - Sets up Python 3.12 environment
   - Spins up PostgreSQL test database
   - Installs dependencies
   - Runs pytest test suite
   
2. **Build and Push** (only if tests pass)
   - Builds Docker images for backend and nginx
   - Tags images with `latest` and commit SHA
   - Pushes images to Docker Hub
   - Makes images publicly available

### View Pipeline Status

Check the [Actions tab](https://github.com/bookie212/multi-container-blog-platform/actions) to see pipeline runs and results.

## Data Persistence

Blog post data is persisted using Docker volumes. The PostgreSQL data is stored in the `db_data` volume:

- ✅ Data survives container restarts
- ✅ Data persists when running `docker-compose down`
- ❌ Data is deleted with `docker-compose down -v`

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

### Backend
- **FastAPI** - Modern, high-performance web framework for building APIs
- **Pydantic** - Data validation using Python type annotations
- **PostgreSQL** - Powerful open-source relational database
- **psycopg2** - PostgreSQL adapter for Python
- **Uvicorn** - Lightning-fast ASGI server
- **pytest** - Testing framework
- **httpx** - HTTP client for testing

### Infrastructure
- **Nginx** - High-performance reverse proxy and web server
- **Docker** - Containerization platform
- **Docker Compose** - Multi-container application orchestration
- **GitHub Actions** - CI/CD automation
- **Docker Hub** - Container registry

## Configuration

### Environment Variables

The application uses environment variables for flexible configuration:

**In docker-compose.yml:**
```yaml
environment:
  POSTGRES_USER: bloguser
  POSTGRES_PASSWORD: blogpassword
  POSTGRES_DB: blogdb
```

**In CI/CD (GitHub Actions):**
- `DB_HOST`: Database hostname (localhost for tests, db for docker-compose)
- `DB_NAME`: Database name
- `DB_USER`: Database username
- `DB_PASSWORD`: Database password
- `DB_PORT`: Database port

### Ports

- **80**: Nginx (main application entry point)
- **8000**: Backend API (direct access, optional)
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

### Database connection issues

If you see "could not translate host name" errors:
- Ensure `DB_HOST` environment variable is set correctly
- For local development: use `localhost`
- For Docker Compose: use `db`

### CI/CD pipeline failures

1. Check the Actions tab for detailed error logs
2. Verify Docker Hub credentials are set in GitHub Secrets
3. Ensure all tests pass locally before pushing

## Future Enhancements

Potential improvements for this project:

- [ ] Add authentication and authorization (JWT tokens)
- [ ] Implement rate limiting
- [ ] Add Prometheus and Grafana for monitoring
- [ ] Deploy to cloud platform (AWS, DigitalOcean, GCP)
- [ ] Add Redis caching layer
- [ ] Implement database migrations with Alembic
- [ ] Add comprehensive logging with ELK stack
- [ ] Set up Kubernetes deployment
- [ ] Add end-to-end tests with Selenium
- [ ] Implement blue-green deployment strategy

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

Bukola - [@bookey082](https://twitter.com/bookey082)

Project Link: [https://github.com/bookie212/multi-container-blog-platform]

---

⭐ Star this repository if you found it helpful!