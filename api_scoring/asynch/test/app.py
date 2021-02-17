import ast
import unittest

import fastapi.testclient as tc

from app.main import app

# sys.path.append(os.path.join("..", ".."))


client = tc.TestClient(app)


class AsyncScoringApiTest(unittest.TestCase):
    def test_healthcheck_api(self):
        expected_resp = "OK"
        resp = client.get("/api/v1/healthcheck")

        self.assertEqual(resp.status_code, 200)

        resp_text = ast.literal_eval(resp.text)
        resp_text = resp_text.get("status")
        self.assertEqual(resp_text, expected_resp)
