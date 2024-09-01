# Flask API Project

This project is a Flask-based API that can be used for basic as well as enterprise-level APIs. It follows best practices and SOLID principles to ensure modularity and scalability.

## Prerequisites

- Python 3.9 or later
- pip (Python package installer)

## Setup

1. Clone the repository:
   ```
   git clone <repository-url>
   cd my_flask_api
   ```

2. Create a virtual environment:
   ```
   python3.9 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   Create a `.env` file in the root directory and add the following:
   ```
   SECRET_KEY=your-secret-key
   DATABASE_URL=sqlite:///app.db
   JWT_SECRET_KEY=your-jwt-secret-key
   ```

5. Initialize the database:
   ```
   flask db init
   flask db migrate
   flask db upgrade
   ```

6. Run the application:
   ```
   python run.py
   DEBUG=True python run.py
   ```

## Project Structure

- `app/`: Main application package
  - `models/`: Database models
  - `routes/`: API endpoints
  - `schemas/`: Serialization/deserialization schemas
  - `services/`: Business logic
  - `utils/`: Utility functions
- `tests/`: Unit and integration tests
- `config.py`: Configuration settings
- `run.py`: Application entry point

## API Endpoints

- `/register` (POST): Register a new user
- `/login` (POST): Authenticate a user and receive a JWT token

## Authentication

This project uses JWT (JSON Web Tokens) for authentication. To access protected routes, include the JWT token in the Authorization header as a Bearer token:

```
Authorization: Bearer <your-jwt-token>
```

## Testing

Run tests using pytest:
```
pytest
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License.