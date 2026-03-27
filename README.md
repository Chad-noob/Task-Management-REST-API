# Task Management REST API

This project is a simple REST API to manage tasks. It was built using **FastAPI** and **SQLite** for a backend assessment.

The API supports the required features:
- Create task
- Get all tasks
- Update task status
- Delete task

It also includes a few bonus features:
- User authentication
- Pagination
- Input validation
- Docker support

---

## Why I chose this stack

I used FastAPI because it is lightweight, easy to test, and automatically provides Swagger documentation.
I used SQLite because it is enough for a small assessment project and keeps setup simple for the evaluator.

-------------------------------------------------------------------------------------------------------------------------------------

## Project structure

```text
task-manager-api-humanized/
├── app/
│   ├── routes/
│   │   ├── auth_routes.py
│   │   └── task_routes.py
│   ├── database.py
│   ├── dependencies.py
│   ├── init_db.py
│   ├── main.py
│   ├── schemas.py
│   └── security.py
├── postman/
│   └── Task-Manager-API.postman_collection.json
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── README.md
├── requirements.txt
└── schema.sql
```

---

## Database schema

### `users`
Stores registered users.
- `id`
- `name`
- `email`
- `password_hash`
- `created_at`

### `sessions`
Stores active login tokens.
- `id`
- `user_id`
- `token`
- `created_at`

### `tasks`
Stores user tasks.
- `id`
- `user_id`
- `title`
- `description`
- `status`
- `created_at`

The SQL schema is available in [`schema.sql`](./schema.sql).

---

## API routes

### Authentication
- `POST /api/auth/register`
- `POST /api/auth/login`

### Tasks
- `POST /api/tasks`
- `GET /api/tasks`
- `PATCH /api/tasks/{task_id}/status`
- `DELETE /api/tasks/{task_id}`

---

## Setup steps

### 1) Clone the repository
```bash
git clone <your-github-repository-link>
cd task-manager-api-humanized
```

### 2) Create a virtual environment
```bash
python -m venv venv
```

### 3) Activate it
#### Windows
```bash
venv\Scripts\activate
```

#### Linux / macOS
```bash
source venv/bin/activate
```

### 4) Install dependencies
```bash
pip install -r requirements.txt
```

### 5) Create environment file
Create a file named `.env` and copy the values from `.env.example`.

Example:
```env
SECRET_KEY=my_custom_secret_key
DB_PATH=task_manager.db
```

### 6) Run the server
```bash
uvicorn app.main:app --reload
```

### 7) Open documentation
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

---

## Docker run

### Build image
```bash
docker build -t task-manager-api .
```

### Run container
```bash
docker run -p 8000:8000 --env-file .env task-manager-api
```

### Or with docker compose
```bash
docker-compose up --build
```

---

## Sample request bodies

### Register
```json
{
  "name": "Melvin George",
  "email": "melvin@example.com",
  "password": "password123"
}
```

### Login
```json
{
  "email": "melvin@example.com",
  "password": "password123"
}
```

### Create task
```json
{
  "title": "Finish backend assessment",
  "description": "Complete CRUD routes and documentation",
  "status": "pending"
}
```

### Update task status
```json
{
  "status": "completed"
}
```

---

## Curl commands

### Register a user
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Melvin George",
    "email": "melvin@example.com",
    "password": "password123"
  }'
```

### Login
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "melvin@example.com",
    "password": "password123"
  }'
```

### Create a task
```bash
curl -X POST http://localhost:8000/api/tasks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "title": "Finish backend assessment",
    "description": "Complete CRUD routes and documentation",
    "status": "pending"
  }'
```

### Get all tasks
```bash
curl -X GET "http://localhost:8000/api/tasks?page=1&limit=5" \
  -H "Authorization: Bearer <token>"
```

### Update task status
```bash
curl -X PATCH http://localhost:8000/api/tasks/1/status \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "status": "completed"
  }'
```

### Delete task
```bash
curl -X DELETE http://localhost:8000/api/tasks/1 \
  -H "Authorization: Bearer <token>"
```

---

## Error handling

Examples of handled cases:
- invalid request body
- missing token
- wrong login credentials
- duplicate email during registration
- task not found

The API returns JSON responses in a consistent format so it is easier to test in Postman.

---

## Suggested Git commit flow

You should avoid a single huge commit. A better submission history would be:

```bash
git init
git add .
git commit -m "Initial project setup with FastAPI and SQLite"
git add .
git commit -m "Added authentication routes and password hashing"
git add .
git commit -m "Implemented task CRUD operations with pagination"
git add .
git commit -m "Added Docker support and README documentation"
```

---

## Possible future improvements

If this project were extended further, I would add:
- due dates
- task priority
- logout / token expiry
- search by title
- unit tests
