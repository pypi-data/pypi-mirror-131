from sklearn.metrics import RocCurveDisplay

from benderml.evaluator.interface import Evaluator
from benderml.exporter.exporter import Exporter
from benderml.split_strategy.split_strategy import TrainingDataSet
from benderml.trainer.model_trainer import TrainedModel


class RocCurve(Evaluator):

    exporter: Exporter

    def __init__(self, exporter: Exporter) -> None:
        self.exporter = exporter

    async def evaluate(self, model: TrainedModel, data_set: TrainingDataSet) -> None:
        display = RocCurveDisplay.from_estimator(
            model.estimator(), data_set.x_validate, data_set.y_validate.astype(float)
        )
        _ = display.ax_.set_title('Roc Curve')
        await self.exporter.store_figure(display.figure_)
