# Mergington High School Activities Management System

A comprehensive web application for managing extracurricular activities at Mergington High School. The system provides a modern FastAPI-based backend with MongoDB database and an interactive frontend for viewing, filtering, and managing student registrations for various school activities.

## Features

### For Students and Visitors
- **Browse Activities**: View all available extracurricular activities with detailed information
- **Advanced Filtering**: Filter activities by:
  - Day of the week (Monday through Friday)
  - Time range (morning/afternoon sessions)
  - Activity categories (Sports, Arts, Academic, Community, Technology)
  - Text search across activity names and descriptions
- **Activity Details**: View comprehensive information including:
  - Activity descriptions and schedules
  - Meeting times and days
  - Current enrollment and capacity limits
  - Participant lists

### For Teachers (Authenticated Users)
- **Student Registration**: Sign up students for activities using their email addresses
- **Student Management**: Remove students from activities when needed
- **Secure Authentication**: Login system with hashed password storage

### System Features
- **RESTful API**: Complete API with interactive documentation
- **Real-time Updates**: Dynamic frontend that updates without page reloads
- **Responsive Design**: Works on desktop and mobile devices
- **Data Persistence**: MongoDB database with sample data initialization

## Technology Stack

### Backend
- **FastAPI**: Modern Python web framework for building APIs
- **MongoDB**: NoSQL database for storing activities and user data
- **PyMongo**: MongoDB driver for Python
- **Argon2 & SHA-256**: Password hashing (mixed implementation)
- **Uvicorn**: ASGI server for running the FastAPI application

### Frontend
- **HTML5**: Semantic markup with accessibility features
- **CSS3**: Modern styling with responsive design
- **JavaScript**: Interactive user interface with API integration
- **Native Web APIs**: Fetch API for HTTP requests, DOM manipulation

### Development Tools
- **Python 3.8+**: Required runtime environment
- **VS Code**: Recommended development environment with debugging support
- **GitHub Codespaces**: Pre-configured development environment

## Installation and Setup

### Prerequisites
- Python 3.8 or higher
- **MongoDB instance** (local or cloud) - **Required**
- Git for version control

### Quick Start

1. **Install Dependencies**
   ```bash
   cd src
   pip install -r requirements.txt
   ```

2. **Start MongoDB** (**Required**)
   Ensure MongoDB is running on `localhost:27017` (default configuration)
   
   **Option A: Local MongoDB Installation**
   ```bash
   # Ubuntu/Debian
   sudo apt install mongodb
   sudo systemctl start mongodb
   
   # macOS (with Homebrew)
   brew install mongodb/brew/mongodb-community
   brew services start mongodb/brew/mongodb-community
   
   # Windows - Download from https://www.mongodb.com/try/download/community
   ```
   
   **Option B: MongoDB Docker Container**
   ```bash
   docker run -d -p 27017:27017 --name mongodb mongo:latest
   ```
   
   **Option C: MongoDB Cloud (Atlas)**
   - Create a free cluster at https://www.mongodb.com/cloud/atlas
   - Update the connection string in `backend/database.py`

3. **Run the Application**
   ```bash
   # From the project root directory (not src/)
   python -m uvicorn src.app:app --reload --host 0.0.0.0 --port 8000
   ```

4. **Access the Application**
   - Web Interface: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - Alternative API Docs: http://localhost:8000/redoc

### Development Environment (GitHub Codespaces)

This project is optimized for GitHub Codespaces, which provides MongoDB out of the box. For the best development experience:

1. Open the repository in GitHub Codespaces
2. Use the pre-configured VS Code launch configuration "Launch Mergington WebApp"
3. Press F5 to start debugging

### Database Setup

The application automatically initializes the MongoDB database with sample data on first run, including:
- **8 Sample Activities**: Chess Club, Programming Class, Morning Fitness, Soccer Team, Basketball Team, Art Club, Drama Club, Math Club
- **Teacher Accounts**: Pre-configured authentication accounts for testing

**Sample Teacher Accounts**:
- Username: `mrodriguez`, Password: `art123` (Ms. Rodriguez)
- Username: `mchen`, Password: `chess456` (Mr. Chen)  
- Username: `principal`, Password: `admin789` (Principal Martinez)

> **Note**: There is currently an authentication inconsistency in the codebase where initial passwords are hashed with Argon2 but login verification uses SHA-256. This may prevent successful login with the sample accounts above until resolved.

## API Documentation

### Activities Endpoints

| Method | Endpoint | Description | Authentication |
|--------|----------|-------------|----------------|
| `GET` | `/activities/` | Get all activities with optional filtering | None |
| `GET` | `/activities/days` | Get list of days with scheduled activities | None |
| `POST` | `/activities/{activity_name}/signup` | Register a student for an activity | Teacher Required |
| `POST` | `/activities/{activity_name}/unregister` | Remove a student from an activity | Teacher Required |

### Authentication Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/auth/login` | Teacher login with username/password |
| `GET` | `/auth/check-session` | Validate existing session |

### Query Parameters

**Activity Filtering (`GET /activities/`)**:
- `day`: Filter by day of week (e.g., "Monday", "Tuesday")
- `start_time`: Filter by minimum start time (24-hour format, e.g., "14:30")
- `end_time`: Filter by maximum end time (24-hour format, e.g., "17:00")

**Example Requests**:
```bash
# Get all Monday activities
GET /activities/?day=Monday

# Get activities starting after 3 PM
GET /activities/?start_time=15:00

# Get morning activities (before 8 AM)
GET /activities/?end_time=08:00
```

## Usage Examples

### Teacher Authentication
Teachers can log in using the login button in the web interface. Sample teacher accounts are created automatically for testing purposes, but there is currently an authentication issue that may prevent successful login (see Database Setup section above).

### Student Registration
Once authenticated (when the authentication issue is resolved), teachers can:
1. Browse available activities
2. Click "Sign Up" on any activity card
3. Enter the student's email address
4. Submit the registration

### Activity Filtering
Users can filter activities using:
- **Search Bar**: Type keywords to search activity names and descriptions
- **Day Filter**: Select specific days of the week
- **Time Filter**: Choose morning (6 AM - 8 AM) or afternoon (3 PM - 6 PM) sessions
- **Category Badges**: Click colored badges to filter by activity type

## Project Structure

```
src/
├── app.py                 # FastAPI application entry point
├── requirements.txt       # Python dependencies
├── README.md             # This documentation file
├── backend/              # Backend API logic
│   ├── __init__.py
│   ├── database.py       # MongoDB connection and data models
│   └── routers/          # API route handlers
│       ├── activities.py # Activity management endpoints
│       └── auth.py       # Authentication endpoints
└── static/               # Frontend files
    ├── index.html        # Main web interface
    ├── styles.css        # Application styling
    └── app.js            # Frontend JavaScript logic
```

## Development Guide

For detailed setup and development instructions, please refer to our [Development Guide](../docs/how-to-develop.md).

## Data Models

### Activity Model
```json
{
  "_id": "Activity Name",
  "description": "Detailed description of the activity",
  "schedule": "Human-readable schedule string",
  "schedule_details": {
    "days": ["Monday", "Wednesday"],
    "start_time": "15:15",
    "end_time": "16:45"
  },
  "max_participants": 20,
  "participants": ["student1@mergington.edu", "student2@mergington.edu"]
}
```

### Teacher Model
```json
{
  "_id": "username",
  "username": "teacher_username",
  "display_name": "Teacher Full Name",
  "role": "Teacher",
  "password": "hashed_password"
}
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly using the development setup
5. Submit a pull request with clear documentation

## License

This project is part of the GitHub Skills learning program and is intended for educational purposes.
