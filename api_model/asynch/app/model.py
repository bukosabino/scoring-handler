import asyncio
import typing as tp

from scoring_handler_utils import TemplateModel


class AsyncModel(TemplateModel):
    async def predict(self, input_data: tp.List[float]) -> float:
        # TODO: logging
        random_ms = self._get_random_model_time(
            min_time=0.04, max_time=0.05
        )  # TODO: settings
        await asyncio.sleep(random_ms)
        return random_ms
