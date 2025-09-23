# Mergington High School Activities

A comprehensive web application that enables teachers to manage student extracurricular activities at Mergington High School. The system provides an intuitive interface for viewing activities, advanced filtering capabilities, and secure teacher authentication for student registration management.

## Features

### For Students and Visitors
- **Browse Activities**: View all available extracurricular activities with detailed descriptions, schedules, and enrollment information
- **Advanced Search**: Search activities by name, description, or any text content
- **Smart Filtering**: Filter activities by:
  - Category (Sports, Arts, Academic, Community, Technology)
  - Day of the week (Monday through Sunday)
  - Time slots (Before School, After School, Weekend)
- **Real-time Information**: See current enrollment counts, available spots, and participant lists
- **Responsive Design**: Modern, mobile-friendly interface with activity cards and color-coded categories

### For Teachers
- **Secure Authentication**: Teacher login system with username/password protection
- **Student Registration**: Register students for activities on their behalf
- **Session Management**: Persistent login sessions with automatic validation
- **Role-based Access**: Teacher-specific features and permissions

### Technical Features
- **REST API**: Comprehensive FastAPI backend with automatic documentation
- **Database Integration**: MongoDB for persistent data storage
- **Real-time Updates**: Dynamic content loading and filtering
- **Interactive Documentation**: Built-in API documentation at `/docs` endpoint

## Architecture

- **Frontend**: HTML, CSS, and JavaScript with modern responsive design
- **Backend**: Python FastAPI framework with MongoDB integration
- **Authentication**: Secure teacher login with Argon2 password hashing
- **API**: RESTful endpoints for activities and authentication management

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/activities` | Get all activities with optional day/time filtering |
| POST | `/activities/{activity_name}/signup` | Register a student for an activity |
| POST | `/auth/login` | Teacher authentication |
| GET | `/auth/check-session` | Validate teacher session |
| GET | `/docs` | Interactive API documentation |

## Development Guide

For detailed setup and development instructions, please refer to our [Development Guide](../docs/how-to-develop.md).
