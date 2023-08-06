from benderml.evaluator.confusion_matrix import ConfusionMatrix
from benderml.evaluator.correlation_matrix import CorrelationMatrix
from benderml.evaluator.feature_importance import XGBoostFeatureImportance
from benderml.evaluator.precision_recall import PrecisionRecall
from benderml.evaluator.predict_probability import ProbabilityForClassification
from benderml.evaluator.roc import RocCurve
from benderml.exporter.exporter import Exporter


class Evaluators:
    @staticmethod
    def roc_curve(exporter: Exporter = Exporter.in_memory()) -> RocCurve:
        return RocCurve(exporter)

    @staticmethod
    def confusion_matrix(exporter: Exporter = Exporter.in_memory()) -> ConfusionMatrix:
        return ConfusionMatrix(exporter)

    @staticmethod
    def correlation_matrix(exporter: Exporter = Exporter.in_memory()) -> CorrelationMatrix:
        return CorrelationMatrix(exporter)

    @staticmethod
    def probability_for(classification: str, exporter: Exporter = Exporter.in_memory()) -> ProbabilityForClassification:
        return ProbabilityForClassification(exporter, classification)

    @staticmethod
    def feature_importance(exporter: Exporter = Exporter.in_memory()) -> XGBoostFeatureImportance:
        return XGBoostFeatureImportance(exporter)

    @staticmethod
    def precision_recall(exporter: Exporter = Exporter.in_memory()) -> PrecisionRecall:
        return PrecisionRecall(exporter)
