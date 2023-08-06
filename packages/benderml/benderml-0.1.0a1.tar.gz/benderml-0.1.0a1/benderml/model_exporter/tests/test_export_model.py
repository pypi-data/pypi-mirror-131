import pytest
from pandas import DataFrame

from benderml.importers import DataImporters
from benderml.model_exporters import ModelExporters
from benderml.split_strategies import SplitStrategies
from benderml.trainer.model_trainer import DecisionTreeClassifierTrainer

pytestmark = pytest.mark.asyncio


async def test_export_model_pipeline(date_df: DataFrame) -> None:

    await (
        DataImporters.literal(date_df)
        .split(SplitStrategies.ratio(1))
        .train(DecisionTreeClassifierTrainer(), input_features=['y_values'], target_feature='x_values')
        .export_model(ModelExporters.disk('test-exports/test_file.json'))
        .run()
    )
