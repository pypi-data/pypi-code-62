import re
from abc import ABCMeta, abstractmethod
from typing import Any, Dict, List

import lightgbm
import xgboost

from sktmls import ModelRegistry, MLSENV


class MLSModelError(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class MLSModel(metaclass=ABCMeta):
    """
    MLS 모델 레지스트리에 등록되는 최상위 클래스입니다.
    """

    def __init__(self, model_name: str, model_version: str):
        assert type(model_name) == str
        assert type(model_version) == str

        if not bool(re.search("^[A-Za-z0-9_]+_model$", model_name)):
            raise MLSModelError(
                "model_name should follow naming rule. MUST be in alphabet, number, underscore and endwiths '_model'"
            )

        if not bool(re.search("^[A-Za-z0-9_]+$", model_version)):
            raise MLSModelError("model_name should follow naming rule. MUST be in alphabet, number, underscore")

        self.model = None
        self.model_name = model_name
        self.model_version = model_version
        self.model_lib = None
        self.model_lib_version = None
        self.features = None

    def save(self, env: MLSENV = None, force: bool = False) -> None:
        """
        모델 바이너리(model.joblib)와 정보(model.json)를 MLS 모델 레지스트리에 등록합니다.

        `sktmls.ModelRegistry.save`와 동일하게 동작합니다.

        ## Args

        - env: (`sktmls.MLSENV`) 접근할 MLS 환경 (`sktmls.MLSENV.DEV`|`sktmls.MLSENV.STG`|`sktmls.MLSENV.PRD`) (기본값: `sktmls.MLSENV.STG`)
        - force: (bool) 이미 모델 레지스트리에 등록된 경우 덮어 쓸 것인지 여부 (기본값: `False`)
        """
        model_registry = ModelRegistry(env=env)
        model_registry.save(self, force)

    @abstractmethod
    def predict(self, x: List[Any]) -> Dict[str, Any]:
        pass


class MLSLightGBMModel(MLSModel):
    """
    MLS 모델 레지스트리에 등록되는 LightGBM 기반 상위 클래스입니다.
    """

    def __init__(self, model, model_name: str, model_version: str, features: List[str] = None):
        super().__init__(model_name, model_version)
        self.model = model
        self.model_lib = "lightgbm"
        self.model_lib_version = lightgbm.__version__

        if not features:
            self.features = self.model.feature_name()
        else:
            if len(features) < len(self.model.feature_name()):
                raise MLSModelError("`features`가 유효하지 않습니다.")
            else:
                self.features = features


class MLSXGBoostModel(MLSModel):
    """
    MLS 모델 레지스트리에 등록되는 XGBoost 기반 상위 클래스입니다.
    """

    def __init__(self, model, model_name: str, model_version: str, features: List[str]):
        super().__init__(model_name, model_version)
        self.model = model
        self.model_lib = "xgboost"
        self.model_lib_version = xgboost.__version__

        if (
            all(isinstance(s, str) for s in features)
            and len(features) >= len(self.model.feature_importances_)
            and type(features) == list
        ):
            self.features = features
        else:
            raise MLSModelError("`features`가 유효하지 않습니다.")


class MLSRuleModel(MLSModel):
    """
    MLS 모델 레지스트리에 등록되는 Rule 기반 상위 클래스입니다.
    """

    def __init__(self, model_name: str, model_version: str, features: List[str]):
        super().__init__(model_name, model_version)
        self.model_lib = "rule"
        self.model_lib_version = "N/A"

        if features:
            self.features = features
        else:
            raise MLSModelError("`features`가 없습니다.")
