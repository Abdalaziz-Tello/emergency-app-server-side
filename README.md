# Emergency Services API

A FastAPI-based REST API for managing emergency services.

## Local Development

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the development server:
```bash
uvicorn main:app --reload
```

## API Endpoints

- `POST /services/` - Create a new emergency service
- `GET /services/` - List all emergency services
- `GET /services/{service_id}` - Get a specific service
- `PUT /services/{service_id}` - Update a service's status
- `DELETE /services/{service_id}` - Delete a service

## Authentication

All endpoints except GET requests require authentication. Use the following credentials:
- Username: admin
- Password: admin123

## Deployment

This project is configured for deployment on Render. The `render.yaml` file contains the necessary configuration.

1. Push your code to a Git repository
2. Connect your repository to Render
3. Create a new Web Service
4. Select your repository
5. Render will automatically detect the configuration and deploy your application

## Environment Variables

- `SECRET_KEY`: Used for JWT token generation (automatically generated on Render)
- `PYTHON_VERSION`: Set to 3.9.0 