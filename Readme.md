# Blog API

A modern blog API service built with FastAPI and Prisma. Provides core blogging features as REST APIs including user authentication, post management, comments, likes, and file uploads.

## Key Features

- 🔐 **User Management**: JWT-based authentication, role-based authorization (ADMIN, AUTHOR, USER)
- 📝 **Posts**: CRUD operations, category classification, search, pagination
- 💬 **Comments**: Post-specific comment management
- 👍 **Likes**: Post like/dislike functionality
- 📁 **Files**: AWS S3-based file upload and management

## Tech Stack

- **Backend**: FastAPI, Python 3.11+
- **ORM**: Prisma
- **Database**: PostgreSQL
- **Storage**: AWS S3
- **Cache**: Redis
- **Authentication**: JWT

## Installation & Setup

1. Clone Repository
```bash
git clone https://github.com/yourusername/blog-api.git
cd blog-api
```

2. Set Up Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

3. Configure Environment Variables
```bash
cp .env.example .env
# Edit .env file with your configurations
```

4. Database Migration
```bash
prisma db push
```

5. Run Server
```bash
uvicorn main:app --reload
```

## API Documentation

Access the API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc


## Contributing

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request