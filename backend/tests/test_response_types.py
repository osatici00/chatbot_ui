import httpx
import pytest

# Base URL for the running mock API
BASE_URL = "http://localhost:8001/api/query"

# (query, expected_response_type)
TEST_CASES = [
    ("Show me a revenue chart by region", "chart"),
    ("Create a customer satisfaction trend line", "chart"),
    ("Display support ticket distribution pie chart", "chart"),
    ("Generate a scatter plot of order value vs satisfaction", "chart"),
    ("Analyze customer insights and provide summary", "text"),
    ("Export sales data to Excel spreadsheet", "file"),
    ("Check processing status of my request", "progress"),
]

@pytest.mark.parametrize("query, expected_type", TEST_CASES)
def test_example_queries(query: str, expected_type: str):
    """Ensure each example query returns the correct response_type."""
    payload = {
        "user_query": query,
        "user_email": "pytest@example.com"
    }
    response = httpx.post(BASE_URL, json=payload, timeout=15.0)
    assert response.status_code == 200, f"HTTP {response.status_code} for query: {query}"
    data = response.json()
    assert data["response_type"] == expected_type, (
        f"Expected {expected_type} for query '{query}', got {data['response_type']}"
    )
    
    # Additional sanity checks per type
    if expected_type == "chart":
        assert data.get("chart_data"), "chart_data missing for chart response"
    elif expected_type == "file":
        assert data.get("file_info"), "file_info missing for file response"
    elif expected_type == "progress":
        assert data.get("progress"), "progress missing for progress response"
    elif expected_type == "text":
        assert data.get("response_content"), "response_content missing for text response" 