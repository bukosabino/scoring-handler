import ast
import sys
import unittest

from app.main import app

# sys.path.append(os.path.join("..", ".."))


client = app.test_client()


class SyncScoringApiTest(unittest.TestCase):
    def test_healthcheck_api(self):
        expected_resp = "OK"
        resp = client.get("/api/v1/healthcheck")
        self.assertEqual(resp.status_code, 200)

        resp_text = resp.get_data(as_text=True)
        resp_text = ast.literal_eval(resp_text)
        resp_text = resp_text.get("status")
        self.assertEqual(resp_text, expected_resp)
