import ast
import os
import shutil
import sys
import unittest

import fastapi.testclient as tc

from app.main import app

sys.path.append(os.path.join("..", ".."))


client = tc.TestClient(app)


class AsyncModelApiTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        dir_path = os.path.dirname(os.path.realpath(__file__))
        cls.folder_output = os.path.join(dir_path, "output")
        if not os.path.exists(cls.folder_output):
            os.makedirs(cls.folder_output)

    @classmethod
    def tearDownClass(cls) -> None:
        if os.path.exists(cls.folder_output):
            shutil.rmtree(cls.folder_output)

    def test_healthcheck_api(self):
        expected_resp = "OK"
        resp = client.get("/api/v1/healthcheck")
        self.assertEqual(resp.status_code, 200)

        resp_text = ast.literal_eval(resp.text)
        resp_text = resp_text.get("status")
        self.assertEqual(resp_text, expected_resp)

    def test_predict_api(self):
        parameters = [
            {},
            {"profile": self.folder_output, "profile-type": "pyinstrument"},
            {"profile": self.folder_output, "profile-type": "yappi"},
        ]
        for params in parameters:
            with self.subTest(i=params):
                resp = client.post(
                    "/api/v1/ml/async/predict", json=[5.1, 3.5, 1.4, 0.2], params=params
                )
                self.assertEqual(resp.status_code, 200)

                resp_text = ast.literal_eval(resp.text)
                resp_text = resp_text.get("detail")
                output = float(resp_text)
                condition_between = 0.05 > output > 0.04  # TODO: settings values
                self.assertTrue(condition_between)

                print(output)
