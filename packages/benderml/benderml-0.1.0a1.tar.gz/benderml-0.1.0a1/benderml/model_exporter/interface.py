from __future__ import annotations

from benderml.trainer.model_trainer import TrainedModel


class ModelExporter:
    async def export(self, model: TrainedModel) -> None:
        raise NotImplementedError()
