import json
import pytest
import azure.functions as func
from HttpTrigger import main


class TestHttpTrigger:
    """Test cases for the HTTP trigger function."""

    def test_http_trigger_with_name_in_query(self):
        """Test HTTP trigger with name parameter in query string."""
        # Construct a mock HTTP request
        req = func.HttpRequest(
            method='GET',
            body=b'',
            url='/api/HttpTrigger',
            params={'name': 'Azure'}
        )

        # Call the function
        response = main(req)

        # Assert response
        assert response.status_code == 200
        response_data = json.loads(response.get_body().decode())
        assert response_data['status'] == 'success'
        assert 'Azure' in response_data['message']
        assert 'Hello, Azure' in response_data['message']

    def test_http_trigger_with_name_in_body(self):
        """Test HTTP trigger with name parameter in request body."""
        # Construct a mock HTTP request with JSON body
        req = func.HttpRequest(
            method='POST',
            body=json.dumps({'name': 'DevOps'}).encode('utf-8'),
            url='/api/HttpTrigger',
            params={}
        )

        # Call the function
        response = main(req)

        # Assert response
        assert response.status_code == 200
        response_data = json.loads(response.get_body().decode())
        assert response_data['status'] == 'success'
        assert 'DevOps' in response_data['message']
        assert 'Hello, DevOps' in response_data['message']

    def test_http_trigger_without_name(self):
        """Test HTTP trigger without name parameter."""
        # Construct a mock HTTP request without name parameter
        req = func.HttpRequest(
            method='GET',
            body=b'',
            url='/api/HttpTrigger',
            params={}
        )

        # Call the function
        response = main(req)

        # Assert response
        assert response.status_code == 400
        response_data = json.loads(response.get_body().decode())
        assert response_data['status'] == 'error'
        assert 'Please pass a name' in response_data['message']

    def test_http_trigger_empty_name_in_query(self):
        """Test HTTP trigger with empty name parameter."""
        # Construct a mock HTTP request with empty name
        req = func.HttpRequest(
            method='GET',
            body=b'',
            url='/api/HttpTrigger',
            params={'name': ''}
        )

        # Call the function
        response = main(req)

        # Assert response (empty string is falsy, should return 400)
        assert response.status_code == 400
        response_data = json.loads(response.get_body().decode())
        assert response_data['status'] == 'error'

    def test_http_trigger_special_characters_in_name(self):
        """Test HTTP trigger with special characters in name."""
        # Construct a mock HTTP request with special characters
        special_name = "Test User <script>alert('xss')</script>"
        req = func.HttpRequest(
            method='GET',
            body=b'',
            url='/api/HttpTrigger',
            params={'name': special_name}
        )

        # Call the function
        response = main(req)

        # Assert response
        assert response.status_code == 200
        response_data = json.loads(response.get_body().decode())
        assert response_data['status'] == 'success'
        assert special_name in response_data['message']

    def test_http_trigger_post_method(self):
        """Test HTTP trigger with POST method."""
        # Construct a mock POST request
        req = func.HttpRequest(
            method='POST',
            body=json.dumps({'name': 'TestUser'}).encode('utf-8'),
            url='/api/HttpTrigger',
            params={}
        )

        # Call the function
        response = main(req)

        # Assert response
        assert response.status_code == 200
        assert response.mimetype == 'application/json'

    def test_http_trigger_get_method(self):
        """Test HTTP trigger with GET method."""
        # Construct a mock GET request
        req = func.HttpRequest(
            method='GET',
            body=b'',
            url='/api/HttpTrigger',
            params={'name': 'TestUser'}
        )

        # Call the function
        response = main(req)

        # Assert response
        assert response.status_code == 200
        assert response.mimetype == 'application/json'

    def test_http_trigger_invalid_json_body(self):
        """Test HTTP trigger with invalid JSON in body."""
        # Construct a mock request with invalid JSON
        req = func.HttpRequest(
            method='POST',
            body=b'invalid json{',
            url='/api/HttpTrigger',
            params={}
        )

        # Call the function
        response = main(req)

        # Assert response (should handle invalid JSON gracefully)
        assert response.status_code == 400
