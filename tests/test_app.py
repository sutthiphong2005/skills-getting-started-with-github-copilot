import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


class TestActivitiesAPI:
    """Test cases for the Activities API endpoints"""

    def test_get_activities(self):
        """Test getting all activities"""
        # Arrange - No special setup needed

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        data = response.json()

        # Check that we get a dictionary with activities
        assert isinstance(data, dict)
        assert len(data) > 0

        # Check that each activity has the expected structure
        for activity_name, activity_data in data.items():
            assert "description" in activity_data
            assert "schedule" in activity_data
            assert "max_participants" in activity_data
            assert "participants" in activity_data
            assert isinstance(activity_data["participants"], list)

    def test_get_activities_specific_activity(self):
        """Test that specific activities are present"""
        # Arrange - No special setup needed

        # Act
        response = client.get("/activities")
        data = response.json()

        # Assert
        # Check for a known activity
        assert "Chess Club" in data
        chess_club = data["Chess Club"]
        assert chess_club["description"] == "Learn strategies and compete in chess tournaments"
        assert chess_club["max_participants"] == 12
        assert "michael@mergington.edu" in chess_club["participants"]

    def test_signup_successful(self):
        """Test successful signup for an activity"""
        # Arrange
        activity_name = "Chess Club"
        email = "test@example.com"

        # Get initial participant count
        response = client.get("/activities")
        initial_data = response.json()
        initial_count = len(initial_data[activity_name]["participants"])

        # Act
        response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert email in data["message"]
        assert activity_name in data["message"]

        # Verify the participant was added
        response = client.get("/activities")
        updated_data = response.json()
        assert email in updated_data[activity_name]["participants"]
        assert len(updated_data[activity_name]["participants"]) == initial_count + 1

    def test_signup_activity_not_found(self):
        """Test signup for non-existent activity"""
        # Arrange
        activity_name = "NonExistentActivity"
        email = "test@example.com"

        # Act
        response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "Activity not found" in data["detail"]

    def test_signup_already_signed_up(self):
        """Test signup when student is already signed up"""
        # Arrange
        activity_name = "Programming Class"
        email = "emma@mergington.edu"  # This email is already in the participants

        # Act
        response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "Student already signed up" in data["detail"]

    def test_unregister_successful(self):
        """Test successful unregister from an activity"""
        # Arrange
        activity_name = "Programming Class"
        email = "emma@mergington.edu"  # This email is in the participants

        # Get initial participant count
        response = client.get("/activities")
        initial_data = response.json()
        initial_count = len(initial_data[activity_name]["participants"])

        # Act
        response = client.delete(f"/activities/{activity_name}/unregister", params={"email": email})

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert email in data["message"]
        assert activity_name in data["message"]

        # Verify the participant was removed
        response = client.get("/activities")
        updated_data = response.json()
        assert email not in updated_data[activity_name]["participants"]
        assert len(updated_data[activity_name]["participants"]) == initial_count - 1

    def test_unregister_activity_not_found(self):
        """Test unregister from non-existent activity"""
        # Arrange
        activity_name = "NonExistentActivity"
        email = "test@example.com"

        # Act
        response = client.delete(f"/activities/{activity_name}/unregister", params={"email": email})

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "Activity not found" in data["detail"]

    def test_unregister_not_signed_up(self):
        """Test unregister when student is not signed up"""
        # Arrange
        activity_name = "Gym Class"
        email = "notsignedup@example.com"

        # Act
        response = client.delete(f"/activities/{activity_name}/unregister", params={"email": email})

        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "Student is not signed up" in data["detail"]

    def test_root_redirect(self):
        """Test that root endpoint redirects to static index"""
        # Arrange
        client_no_redirect = TestClient(app, follow_redirects=False)

        # Act
        response = client_no_redirect.get("/")

        # Assert
        assert response.status_code == 307  # Temporary redirect
        assert response.headers["location"] == "/static/index.html"