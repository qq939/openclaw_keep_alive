import unittest
import sys
import time
import threading
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

    def test_control_on_endpoint(self):
        try:
            resp = urlopen(f"{self.BASE_URL}/control/on", timeout=self.TIMEOUT)
            data = resp.read().decode()
            self.assertIn("ON", data)
        except URLError:
            self.fail("Cannot connect to server")

    def test_control_off_endpoint(self):
        try:
            resp = urlopen(f"{self.BASE_URL}/control/off", timeout=self.TIMEOUT)
            data = resp.read().decode()
            self.assertIn("OFF", data)
        except URLError:
            self.fail("Cannot connect to server")

    def test_control_toggle_endpoint(self):
        try:
            resp = urlopen(f"{self.BASE_URL}/control/toggle", timeout=self.TIMEOUT)
            data = resp.read().decode()
            self.assertTrue("ON" in data or "OFF" in data)
        except URLError:
            self.fail("Cannot connect to server")

    def test_status_includes_control(self):
        try:
            resp = urlopen(f"{self.BASE_URL}/status", timeout=self.TIMEOUT)
            data = resp.read().decode()
            self.assertIn("control", data)
        except URLError:
            self.fail("Cannot connect to server")

if __name__ == "__main__":
    unittest.main(verbosity=2)