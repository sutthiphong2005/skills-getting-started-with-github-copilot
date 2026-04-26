# Backend Tests

This directory contains tests for the FastAPI backend application.

## Setup

First, install the dependencies:

```bash
pip install -r requirements.txt
```

## Test Structure

The tests follow the AAA (Arrange-Act-Assert) testing pattern:

- **Arrange**: Set up test data and preconditions
- **Act**: Execute the code being tested
- **Assert**: Verify the results and behavior

- `test_app.py`: Tests for the main API endpoints including:
  - GET `/activities` - Retrieve all activities
  - POST `/activities/{activity_name}/signup` - Sign up for activities
  - DELETE `/activities/{activity_name}/unregister` - Unregister from activities
  - GET `/` - Root endpoint redirect

## Running Tests

To run the tests:

```bash
pytest tests/
```

Or with verbose output:

```bash
pytest tests/ -v
```

## Test Coverage

The tests cover:
- Successful operations for all endpoints
- Error handling for invalid activities
- Validation of duplicate signups/unregisters
- Proper HTTP status codes and response formats
- Data integrity after operations