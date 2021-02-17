import time
import typing as tp

from scoring_handler_utils import TemplateModel


class SyncModel(TemplateModel):
    def predict(self, input_data: tp.List[float]) -> float:
        # TODO: logging
        random_ms = self._get_random_model_time(min_time=0.04, max_time=0.05)
        time.sleep(random_ms)
        return random_ms
