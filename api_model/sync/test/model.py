import os
import sys
import unittest

from app.model import SyncModel

sys.path.append(os.path.join("..", ".."))


class SyncModelTest(unittest.TestCase):
    def test_predict(self):
        input_data = [5.1, 3.5, 1.4, 0.2]
        dir_path = os.path.dirname(os.path.realpath(__file__))
        model_filepath = os.path.join(
            dir_path, "..", "artifacts", "model.pkl"
        )  # TODO: settings
        model = SyncModel(model_filepath=model_filepath)
        prediction = model.predict(input_data)
        self.assertTrue(0.04 <= prediction <= 0.05)
        print(prediction)
