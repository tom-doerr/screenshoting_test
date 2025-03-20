import sys
import os
import pytest
sys.path.append(os.getcwd())  # Add project root to path
from http.server import SimpleHTTPRequestHandler, HTTPServer
from threading import Thread
from screenshotter import capture_screenshot

@pytest.fixture(scope="module", name="local_test_server")
def fixture_test_server():
    # Start a simple HTTP server for testing
    handler = SimpleHTTPRequestHandler
    server = HTTPServer(('localhost', 8000), handler)
    thread = Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()
    yield
    server.shutdown()
    thread.join()

def test_screenshot_creation(local_test_server, tmp_path):
    """Test basic screenshot functionality with local test server"""
    output_file = tmp_path / "screenshot.png"
    capture_screenshot('http://localhost:8000', str(output_file))
    
    assert output_file.exists(), "Screenshot file was not created"
    assert output_file.stat().st_size > 0, "Screenshot file is empty"

def test_invalid_url_handling(tmp_path):
    """Test proper handling of invalid URLs"""
    output_file = tmp_path / "invalid.png"
    
    with pytest.raises(Exception):
        capture_screenshot('not_a_valid_url', str(output_file))

    assert not output_file.exists(), "Should not create file for invalid URL"
