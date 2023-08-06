import matplotlib.pyplot as plt
from xgboost import plot_importance

from benderml.evaluator.interface import Evaluator
from benderml.exporter.exporter import Exporter
from benderml.split_strategy.split_strategy import TrainingDataSet
from benderml.trainer.model_trainer import TrainedModel, TrainedXGBoostModel


class XGBoostFeatureImportance(Evaluator):

    exporter: Exporter

    def __init__(self, exporter: Exporter) -> None:
        self.exporter = exporter

    async def evaluate(self, model: TrainedModel, data_set: TrainingDataSet) -> None:
        if isinstance(model, TrainedXGBoostModel) is False:
            raise Exception('Only supporting feature importance for XGBoost models')

        fig, ax = plt.subplots(1, 1, figsize=(20, 10))
        plot_importance(model.model, ax=ax)
        await self.exporter.store_figure(fig)
