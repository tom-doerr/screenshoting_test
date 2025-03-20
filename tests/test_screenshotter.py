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
    server = HTTPServer(("localhost", 8000), handler)
    thread = Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()
    yield
    server.shutdown()
    thread.join()


def test_screenshot_creation(local_test_server, tmp_path):
    """Test basic screenshot functionality with local test server"""
    # The local_test_server fixture is used implicitly by making the HTTP request
    assert local_test_server is None  # This is just to use the fixture parameter
    output_file = tmp_path / "screenshot.png"
    capture_screenshot("http://localhost:8000", str(output_file))

    assert output_file.exists(), "Screenshot file was not created"
    assert output_file.stat().st_size > 0, "Screenshot file is empty (0 bytes)"

def test_default_filename(local_test_server, tmp_path):
    """Test default filename generation"""
    with pytest.MonkeyPatch().context() as mp:
        mp.chdir(tmp_path)
        result_path = capture_screenshot("http://localhost:8000")
        assert os.path.exists(result_path), "Default file not created"
        assert result_path.startswith("screenshot_"), "Filename prefix mismatch"
        assert result_path.endswith(".png"), "File extension mismatch"
        assert datetime.strptime(result_path[11:-4], "%Y%m%d_%H%M%S"), "Timestamp format invalid"

def test_unreachable_url(tmp_path):
    """Test handling of unreachable URLs"""
    output_file = tmp_path / "unreachable.png"
    
    with pytest.raises(RuntimeError):
        capture_screenshot("http://localhost:12345", str(output_file))
        
    assert not output_file.exists(), "File should not be created for unreachable URL"


def test_invalid_url_handling(tmp_path):
    """Test proper handling of invalid URLs"""
    output_file = tmp_path / "invalid.png"

    with pytest.raises(ValueError):
        capture_screenshot("not_a_valid_url", str(output_file))

    assert not output_file.exists(), "Should not create file for invalid URL"
