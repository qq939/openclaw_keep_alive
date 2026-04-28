import unittest
import sys
import time
import threading
import requests
from urllib.request import urlopen
from urllib.error import URLError

class TestKeepAliveControl(unittest.TestCase):
    BASE_URL = "http://localhost:7861"
    TIMEOUT = 5

    @classmethod
    def setUpClass(cls):
        from app import app
        cls.app = app
        cls.server = threading.Thread(target=lambda: app.run(host='0.0.0.0', port=7861), daemon=True)
        cls.server.start()
        time.sleep(2)

    def test_status_endpoint_returns_json(self):
        try:
            resp = urlopen(f"{self.BASE_URL}/status", timeout=self.TIMEOUT)
            data = resp.read().decode()
            self.assertIn("openclaw", data)
            self.assertIn("comfyui", data)
        except URLError:
            self.fail("Cannot connect to server")

    def test_openclaw_on_endpoint(self):
        try:
            resp = urlopen(f"{self.BASE_URL}/openclaw/on", timeout=self.TIMEOUT)
            data = resp.read().decode()
            self.assertIn("ON", data)
        except URLError:
            self.fail("Cannot connect to server")

    def test_openclaw_off_endpoint(self):
        try:
            resp = urlopen(f"{self.BASE_URL}/openclaw/off", timeout=self.TIMEOUT)
            data = resp.read().decode()
            self.assertIn("OFF", data)
        except URLError:
            self.fail("Cannot connect to server")

    def test_comfyui_on_endpoint(self):
        try:
            resp = urlopen(f"{self.BASE_URL}/comfyui/on", timeout=self.TIMEOUT)
            data = resp.read().decode()
            self.assertIn("ON", data)
        except URLError:
            self.fail("Cannot connect to server")

    def test_comfyui_off_endpoint(self):
        try:
            resp = urlopen(f"{self.BASE_URL}/comfyui/off", timeout=self.TIMEOUT)
            data = resp.read().decode()
            self.assertIn("OFF", data)
        except URLError:
            self.fail("Cannot connect to server")

    def test_homepage_has_html_structure(self):
        try:
            resp = urlopen(f"{self.BASE_URL}/", timeout=self.TIMEOUT)
            data = resp.read().decode()
            self.assertIn("<html", data.lower())
            self.assertIn("OpenClaw", data)
            self.assertIn("ComfyUI", data)
        except URLError:
            self.fail("Cannot connect to server")

if __name__ == "__main__":
    unittest.main(verbosity=2)